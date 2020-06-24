import numpy as np
import plotly.graph_objs as go

from io_f import read_data_file


def save_figure_to_html(fig, filename):
    fig.write_html(filename)


def add_floor_plan(fig, image, width_meter, height_meter):
    fig.update_layout(images=[
        go.layout.Image(
            source=image,
            xref="x",
            yref="y",
            x=0,
            y=height_meter,
            sizex=width_meter,
            sizey=height_meter,
            sizing="contain",
            opacity=1,
            layer="below",
        )
    ])
    return fig


def configure_fig_shape_plotly(fig, width_meter, height_meter, title=None):
    fig.update_xaxes(autorange=False, range=[0, width_meter])
    fig.update_yaxes(autorange=False, range=[0, height_meter], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        title=go.layout.Title(
            text=title or "No title.",
            xref="paper",
            x=0,
        ),
        autosize=True,
        width=900,
        height=200 + 900 * height_meter / width_meter,
        template="plotly_white",
    )
    return fig


def add_position(fig, position, anno=False, line_name='positions', base_color='rgba(4, 174, 4, 0.5)'):
    # trajectory = np.array(trajectory)

    size_list = [6] * len(position)
    size_list[0] = 10
    size_list[-1] = 10

    color_list = [base_color] * len(position)
    color_list[0] = 'rgba(12, 5, 235, 1)'
    color_list[-1] = 'rgba(235, 5, 5, 1)'

    recorded_points_info = {}
    if anno:
        text_list = []
        for i in range(len(position)):
            if str(position[i]) in recorded_points_info.keys():
                recorded_points_info[str(position[i])] += 1
            else:
                recorded_points_info[str(position[i])] = 0
            text_list.append("        " * recorded_points_info[str(position[i])] + f'{i}')
        text_list[0] = 'Start Point: 0'
        text_list[-1] = f'End Point: {len(position) - 1}'
    else:
        text_list = [''] * len(position)
        text_list[0] = 'Start Point'
        text_list[-1] = 'End Point'

    fig.add_trace(
        go.Scattergl(
            x=position[:, 0],
            y=position[:, 1],
            mode='markers + lines + text',
            marker=dict(size=size_list, color=color_list),
            line=dict(shape='linear', color='rgb(100, 10, 100)', width=2, dash='dot'),
            text=text_list,
            textposition="top center",
            name=line_name,
        ))
    return fig


def save_path_image(path_file, image, width_meter, height_meter, path_trace_save_folder, title=None):
    gt_positions = read_data_file(path_file).waypoint
    if gt_positions.size > 0:
        gt_positions = gt_positions[:, 1:3]
    gt_fig = go.Figure()
    gt_fig = add_floor_plan(gt_fig, image, width_meter, height_meter)
    gt_fig = add_position(gt_fig, gt_positions, anno=True)
    gt_fig = configure_fig_shape_plotly(gt_fig, width_meter, height_meter, title=title)
    path_id = path_file.split("/")[-1].split(".")[0]
    gt_fig.write_html(f'{path_trace_save_folder}/{path_id}.html')  # save fig
    return None


def visualize_ground_truth(gt_position, floor_plan, width_meter, height_meter, title=None, show=False):
    fig = go.Figure()
    fig = add_floor_plan(fig, floor_plan, width_meter, height_meter)
    fig = add_position(fig, gt_position, anno=True)
    fig = configure_fig_shape_plotly(fig, width_meter, height_meter, title=title)

    if show:
        fig.show()

    return fig


def gen_heatmap(posi_info_list, save_folder, title, image, height_meter, width_meter, colorbar_name="colorbar", show=True, simplify=True):
    if simplify:
        uniqued_list = []
        recorded_positions = []
        for posi in posi_info_list:
            if posi[1:3] in recorded_positions:
                continue
            uniqued_list.append(posi)
            recorded_positions.append(posi[1:3])
        posi_info_list = uniqued_list

    position_info_list = np.array(posi_info_list)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=position_info_list[:, 1],
                   y=position_info_list[:, 2],
                   mode='markers',
                   marker=dict(size=7,
                               color=position_info_list[:, 3].astype(float),
                               colorbar=dict(title=colorbar_name),
                               colorscale="Rainbow"),
                   text=position_info_list[:, 3].astype(float),
                   name=title))
    fig = add_floor_plan(fig, image, height_meter, width_meter)
    fig = configure_fig_shape_plotly(fig, width_meter, height_meter, title=title)
    fig.write_html(f'{save_folder}/{title}.html')
    if show:
        fig.show()
    return None
