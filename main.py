import json
import os
from pathlib import Path

import numpy as np

from compute_f import compute_steps, compute_headings, compute_positions, \
    compute_step_heading, compute_stride_length, correct_positions
from io_f import read_data_file
from visualize_f import visualize_ground_truth, save_figure_to_html, save_path_image, gen_heatmap
from PIL import Image

path_data_folder = "./data/site1/floor1/path_data_files"
floor_plan_filename = "./data/site1/floor1/floor_image.png"
floor_info_filename = "./data/site1/floor1/floor_info.json"

path_image_save_folder = "./data/site1/floor1/path_images"
magn_image_save_folder = "./data/site1/floor1/magn_images"
wifi_image_save_folder = "./data/site1/floor1/wifi_images"
ibeacon_image_save_folder = "./data/site1/floor1/ibeacon_images"


# def ground_truth_visualization(path_filenames, image, width_meter, height_meter):
#     for path_filename in path_filenames:
#         path_id = path_filename.split('/')[-1].split('.')[0]
#         save_path_image(path_filename, image, width_meter, height_meter, path_image_save_folder, title=path_id)


def visualize_data_distribution(path_file_list, image, height_meter, width_meter):
    total_wifi_info = {}
    total_ibeacon_info = {}
    total_magn_info = []
    for path_filename in path_file_list:
        path_datas = read_data_file(path_filename)
        path_acce_datas = path_datas.acce
        path_magn_datas = path_datas.magn
        path_ahrs_datas = path_datas.ahrs
        path_wifi_datas = path_datas.wifi
        path_ibeacon_datas = path_datas.ibeacon
        path_posi_datas = path_datas.waypoint

        step_timestamps, step_indexs, step_acce_max_mins = compute_steps(path_acce_datas)
        headings = compute_headings(path_ahrs_datas)
        stride_lengths = compute_stride_length(step_acce_max_mins)
        step_headings = compute_step_heading(step_timestamps, headings)
        pdr_positions = compute_positions(path_posi_datas[0, 1:3], stride_lengths, step_headings)[0]
        gt_positions = correct_positions(pdr_positions, path_posi_datas)[:, :3]

        for wifi_data in path_wifi_datas:
            bssid = wifi_data[2]
            rssi = wifi_data[3]
            dif = abs(gt_positions[:, 0] - float(wifi_data[0]))
            position_of_min = np.argmin(dif)
            posi = gt_positions[position_of_min, :3]
            if bssid not in total_wifi_info.keys():
                total_wifi_info[bssid] = [[posi[0], posi[1], posi[2], rssi]]
            else:
                total_wifi_info[bssid].append([posi[0], posi[1], posi[2], rssi])

        for ibeacon_data in path_ibeacon_datas:
            ummid = ibeacon_data[1]
            rssi = ibeacon_data[3]
            dif = abs(gt_positions[:, 0] - float(ibeacon_data[0]))
            position_of_min = np.argmin(dif)
            posi = gt_positions[position_of_min, :3]
            if ummid not in total_ibeacon_info.keys():
                total_ibeacon_info[ummid] = [[posi[0], posi[1], posi[2], rssi]]
            else:
                total_ibeacon_info[ummid].append([posi[0], posi[1], posi[2], rssi])

        strength_info = np.sqrt(np.sum(path_magn_datas[:, 1:4] ** 2, 1))
        for i, magn_data in enumerate(path_magn_datas):
            strength = strength_info[i]
            dif = abs(gt_positions[:, 0] - float(magn_data[0]))
            position_of_min = np.argmin(dif)
            posi = gt_positions[position_of_min, :3]
            total_magn_info.append([posi[0], posi[1], posi[2], strength])

    print('wifi ap bssids:\n', list(total_wifi_info.keys()))
    target_wifi_ap = input("Please input target wifi ap bssid:\n")
    gen_heatmap(total_wifi_info[target_wifi_ap], wifi_image_save_folder, f'wifi_{target_wifi_ap}', image, height_meter, width_meter, colorbar_name="rssi")

    print('ibeacon ap ummids:\n', list(total_ibeacon_info.keys()))
    target_ibeacon_ap = input("Please input target ibeacon ap ummid:\n")
    gen_heatmap(total_ibeacon_info[target_ibeacon_ap], ibeacon_image_save_folder, f'ibeacon_{target_ibeacon_ap}', image, height_meter, width_meter, colorbar_name="rssi")

    gen_heatmap(total_magn_info, magn_image_save_folder, f'magn_heatmap', image, height_meter, width_meter, colorbar_name="magn_strength")


if __name__ == "__main__":
    floor_plan = Image.open(floor_plan_filename)

    with open(floor_info_filename) as f:
        floor_info = json.load(f)
    width_meter = floor_info["map_info"]["width"]
    height_meter = floor_info["map_info"]["height"]

    path_filenames = list(Path(path_data_folder).resolve().glob("*.txt"))
    # path_filenames = [str(p_f) for p_f in path_filenames]
    # ground_truth_visualization(path_filenames, floor_plan, width_meter, height_meter)

    if not Path(path_image_save_folder).is_dir():
        Path(path_image_save_folder).mkdir()
    if not Path(magn_image_save_folder).is_dir():
        Path(magn_image_save_folder).mkdir()
    if not Path(wifi_image_save_folder).is_dir():
        Path(wifi_image_save_folder).mkdir()
    if not Path(ibeacon_image_save_folder).is_dir():
        Path(ibeacon_image_save_folder).mkdir()

    # visualize ground truth positions
    for path_filename in path_filenames:
        path_data = read_data_file(path_filename)
        path_id = path_filename.name.split(".")[0]
        fig = visualize_ground_truth(path_data.waypoint[:, 1:3], floor_plan, width_meter, height_meter, title=path_id, show=False)
        html_filename = f'{path_image_save_folder}/{path_id}.html'
        html_filename = str(Path(html_filename).resolve())
        save_figure_to_html(fig, html_filename)

    # ground_truth_visualization(path_filenames, floor_plan, height_meter, width_meter)
    visualize_data_distribution(path_filenames, floor_plan, height_meter, width_meter)
