import json
import os
from pathlib import Path


import numpy as np

from compute_f import split_ts_seq, compute_step_positions
from io_f import read_data_file
from visualize_f import visualize_trajectory, visualize_heatmap, save_figure_to_html

path_data_folder = "./data/site1/floor1/path_data_files"
floor_plan_filename = "./data/site1/floor1/floor_image.png"
floor_info_filename = "./data/site1/floor1/floor_info.json"

path_image_save_folder = "./data/site1/floor1/path_images"
magn_image_save_folder = "./data/site1/floor1/magn_images"
wifi_image_save_folder = "./data/site1/floor1/wifi_images"
ibeacon_image_save_folder = "./data/site1/floor1/ibeacon_images"


def calibrate_magnetic_wifi_ibeacon_to_position(path_file_list):
    mwi_datas = {}
    for path_filename in path_file_list:
        print(f'Processing {path_filename}...')
        path_datas = read_data_file(path_filename)
        acce_datas = path_datas.acce
        magn_datas = path_datas.magn
        ahrs_datas = path_datas.ahrs
        wifi_datas = path_datas.wifi
        ibeacon_datas = path_datas.ibeacon
        posi_datas = path_datas.waypoint

        step_gt_positions = compute_step_positions(acce_datas, ahrs_datas, posi_datas)
        # visualize_trajectory(posi_datas[:, 1:3], floor_plan_filename, width_meter, height_meter, title='Ground Truth', show=True)
        # visualize_trajectory(step_gt_positions[:, 1:3], floor_plan_filename, width_meter, height_meter, title='Step Ground Truth', show=True)

        if wifi_datas.size != 0:
            sep_tss = np.unique(wifi_datas[:, 0].astype(int))
            wifi_datas_list = split_ts_seq(wifi_datas, sep_tss)
            for wifi_ds in wifi_datas_list:
                diff = np.abs(step_gt_positions[:, 0] - float(wifi_ds[0, 0]))
                index = np.argmin(diff)
                target_xy_key = tuple(step_gt_positions[index, 1:3])
                if target_xy_key in mwi_datas:
                    mwi_datas[target_xy_key]['wifi'] = np.append(mwi_datas[target_xy_key]['wifi'], wifi_ds, axis=0)
                else:
                    mwi_datas[target_xy_key] = {
                        'magnetic': np.zeros((0, 4)),
                        'wifi': wifi_ds,
                        'ibeacon': np.zeros((0, 3))
                    }

        if ibeacon_datas.size != 0:
            sep_tss = np.unique(ibeacon_datas[:, 0].astype(int))
            ibeacon_datas_list = split_ts_seq(ibeacon_datas, sep_tss)
            for ibeacon_ds in ibeacon_datas_list:
                diff = np.abs(step_gt_positions[:, 0] - float(ibeacon_ds[0, 0]))
                index = np.argmin(diff)
                target_xy_key = tuple(step_gt_positions[index, 1:3])
                if target_xy_key in mwi_datas:
                    mwi_datas[target_xy_key]['ibeacon'] = np.append(mwi_datas[target_xy_key]['ibeacon'], ibeacon_ds, axis=0)
                else:
                    mwi_datas[target_xy_key] = {
                        'magnetic': np.zeros((0, 4)),
                        'wifi': np.zeros((0, 5)),
                        'ibeacon': ibeacon_ds
                    }

        sep_tss = np.unique(magn_datas[:, 0].astype(int))
        magn_datas_list = split_ts_seq(magn_datas, sep_tss)
        for magn_ds in magn_datas_list:
            diff = np.abs(step_gt_positions[:, 0] - float(magn_ds[0, 0]))
            index = np.argmin(diff)
            target_xy_key = tuple(step_gt_positions[index, 1:3])
            if target_xy_key in mwi_datas:
                mwi_datas[target_xy_key]['magnetic'] = np.append(mwi_datas[target_xy_key]['magnetic'], magn_ds, axis=0)
            else:
                mwi_datas[target_xy_key] = {
                    'magnetic': magn_ds,
                    'wifi': np.zeros((0, 5)),
                    'ibeacon': np.zeros((0, 3))
                }

        print('fff')

    return mwi_datas


def extract_wifi_rssi(mwi_datas):
    wifi_rssi = {}
    for position_key in mwi_datas:
        print(f'Position: {position_key}')

        wifi_data = mwi_datas[position_key]['wifi']
        for wifi_d in wifi_data:
            bssid = wifi_d[2]
            rssi = int(wifi_d[3])

            if bssid in wifi_rssi:
                position_rssi = wifi_rssi[bssid]
                if position_key in position_rssi:
                    old_rssi = position_rssi[position_key][0]
                    old_count = position_rssi[position_key][1]
                    position_rssi[position_key][0] = (old_rssi * old_count + rssi) / (old_count + 1)
                    position_rssi[position_key][1] = old_count + 1
                else:
                    position_rssi[position_key] = np.array([rssi, 1])
            else:
                position_rssi = {}
                position_rssi[position_key] = np.array([rssi, 1])

            wifi_rssi[bssid] = position_rssi

    return wifi_rssi


def extract_ibeacon_rssi(mwi_datas):
    ibeacon_rssi = {}
    for position_key in mwi_datas:
        print(f'Position: {position_key}')

        ibeacon_data = mwi_datas[position_key]['ibeacon']
        for ibeacon_d in ibeacon_data:
            ummid = ibeacon_d[1]
            rssi = int(ibeacon_d[2])

            if ummid in ibeacon_rssi:
                position_rssi = ibeacon_rssi[ummid]
                if position_key in position_rssi:
                    old_rssi = position_rssi[position_key][0]
                    old_count = position_rssi[position_key][1]
                    position_rssi[position_key][0] = (old_rssi * old_count + rssi) / (old_count + 1)
                    position_rssi[position_key][1] = old_count + 1
                else:
                    position_rssi[position_key] = np.array([rssi, 1])
            else:
                position_rssi = {}
                position_rssi[position_key] = np.array([rssi, 1])

            ibeacon_rssi[ummid] = position_rssi

    return ibeacon_rssi


if __name__ == "__main__":
    if not Path(path_image_save_folder).is_dir():
        Path(path_image_save_folder).mkdir()
    if not Path(magn_image_save_folder).is_dir():
        Path(magn_image_save_folder).mkdir()
    if not Path(wifi_image_save_folder).is_dir():
        Path(wifi_image_save_folder).mkdir()
    if not Path(ibeacon_image_save_folder).is_dir():
        Path(ibeacon_image_save_folder).mkdir()

    with open(floor_info_filename) as f:
        floor_info = json.load(f)
    width_meter = floor_info["map_info"]["width"]
    height_meter = floor_info["map_info"]["height"]

    path_filenames = list(Path(path_data_folder).resolve().glob("*.txt"))

    # visualize ground truth positions
    # for path_filename in path_filenames:
    #     path_data = read_data_file(path_filename)
    #     path_id = path_filename.name.split(".")[0]
    #     fig = visualize_trajectory(path_data.waypoint[:, 1:3], floor_plan_filename, width_meter, height_meter, title=path_id, show=False)
    #     html_filename = f'{path_image_save_folder}/{path_id}.html'
    #     html_filename = str(Path(html_filename).resolve())
    #     save_figure_to_html(fig, html_filename)

    # visualize magnetic, wifi, ibeacon
    mwi_datas = calibrate_magnetic_wifi_ibeacon_to_position(path_filenames)

    # visualize_trajectory(np.array(list(mwi_datas.keys())), floor_plan_filename, width_meter, height_meter, title='Step Ground Truth', show=True)

    wifi_rssi = extract_wifi_rssi(mwi_datas)

    # print all wifi bssid
    print(f'This floor has {len(wifi_rssi.keys())} wifi aps')
    # target_wifi_ap = input(f"Please input target wifi ap bssid:\nExample: {list(wifi_rssi.keys())[0:10]}")
    position_rssi = wifi_rssi['1e:74:9c:a7:b2:e4']
    heat_positions = np.array(list(wifi_rssi['1e:74:9c:a7:b2:e4'].keys()))
    heat_values = np.array(list(wifi_rssi['1e:74:9c:a7:b2:e4'].values()))[:, 0]
    visualize_heatmap(heat_positions, heat_values, floor_plan_filename, width_meter, height_meter)
    # ibeacon_rssi = extract_ibeacon_rssi(mwi_datas)

    print('fff')
