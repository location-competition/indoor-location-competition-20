# 文件使用说明

## 功能运行脚本
### man.py
文件说明：首部路径参数配置可按需自行更改。

功能1：生成并保存路径轨迹图片（全部轨迹）

功能2：从原始文件中提取各类数据并处理生成分布热力图（展示wifi、ibeacon的id列表，生成并保存选定的wifi、ibeacon的信号分布图以及楼层的磁力强度分布图）

## 功能模块文件
### compute_f.py
文件说明：包含数据计算、处理的相关函数
### io_f.py
文件说明：包含文件读取、数据整理的相关函数
### visualize_f.py
文件说明：包含数据可视化的相关函数

## data文件夹
文件说明：包含原始数据并作为默认的数据存储位置

示例：

data/site1 为包含site1场馆所有楼层的所有数据的文件夹

data/site1/floor1 为包含floor1楼层的所有数据的文件夹

data/site1/floor1/ibeacon_images 为生成的floor1的所有ibeacon信号强度分布图的存储位置

data/site1/floor1/path_data_files 为包含floor1的所有原始数据文件的文件夹

data/site1/floor1/path_images 为生成的floor1的所有path轨迹图的存储位置

data/site1/floor1/wifi_images 为生成的floor1的所有wifi信号强度分布图的存储位置

data/site1/floor1/floor_image.png 为floor1的楼层地图

data/site1/floor1/floor_info.json 为包含floor1地图尺寸信息的文件

data/site1/floor1/geojson_map.json 为floor1的地图的geojson文件