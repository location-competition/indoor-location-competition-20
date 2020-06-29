import numpy as np
import plotly.graph_objs as go
from PIL import Image


def save_figure_to_html(fig, filename):
    fig.write_html(filename)


def add_floor_plan(fig, floor_plan_filename, width_meter, height_meter):
    floor_plan = Image.open(floor_plan_filename)

    fig.update_layout(images=[
        go.layout.Image(
            source=floor_plan,
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


def configure_fig_shape(fig, width_meter, height_meter, title=None):
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


def visualize_trajectory(trajectory, floor_plan_filename, width_meter, height_meter, title=None, show=False):
    fig = go.Figure()

    # add trajectory
    size_list = [6] * trajectory.shape[0]
    size_list[0] = 10
    size_list[-1] = 10

    color_list = ['rgba(4, 174, 4, 0.5)'] * trajectory.shape[0]
    color_list[0] = 'rgba(12, 5, 235, 1)'
    color_list[-1] = 'rgba(235, 5, 5, 1)'

    position_count = {}
    text_list = []
    for i in range(trajectory.shape[0]):
        if str(trajectory[i]) in position_count:
            position_count[str(trajectory[i])] += 1
        else:
            position_count[str(trajectory[i])] = 0
        text_list.append('        ' * position_count[str(trajectory[i])] + f'{i}')
    text_list[0] = 'Start Point: 0'
    text_list[-1] = f'End Point: {trajectory.shape[0] - 1}'

    fig.add_trace(
        go.Scattergl(
            x=trajectory[:, 0],
            y=trajectory[:, 1],
            mode='markers + lines + text',
            marker=dict(size=size_list, color=color_list),
            line=dict(shape='linear', color='rgb(100, 10, 100)', width=2, dash='dot'),
            text=text_list,
            textposition="top center",
            name='trajectory',
        ))

    # add floor plan
    floor_plan = Image.open(floor_plan_filename)
    fig.update_layout(images=[
        go.layout.Image(
            source=floor_plan,
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

    # configure
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
    fig = configure_fig_shape(fig, width_meter, height_meter, title=title)
    fig.write_html(f'{save_folder}/{title}.html')
    if show:
        fig.show()
    return None
