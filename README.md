# 文件使用说明

## 功能运行脚本
### main.py
文件说明：首部路径参数配置可按需自行更改。

功能1：
1. 提取本楼层所有采集数据文件的真值点，并可视化。

功能2：
1. 根据PDR及真值点，计算出所有的步点位置，并将地磁、wifi、iBeacon数据配准到所有的步点位置上。
2. 可视化本楼层所有的步点位置。
3. 可视化本楼层地磁强度分布。
4. 根据输入的wifi的bssid（命令行提示'Please input target wifi ap bssid:'），可视化该wifi ap的RSSI强度分布。
5. 根据输入的iBeacon的UUID_MajorID_MinorID（命令行提示'Please input target ibeacon UUID_MajorID_MinorID:'），可视化该iBeacon的RSSI强度分布。

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

data/site1/floor1/path_data_files 为包含floor1的所有原始数据文件的文件夹

data/site1/floor1/floor_image.png 为floor1的楼层地图

data/site1/floor1/floor_info.json 为包含floor1地图尺寸信息的文件

data/site1/floor1/geojson_map.json 为floor1的地图的geojson文件

data/site1/floor1/path_images 为生成的floor1的所有path真值轨迹图的存储位置

data/site1/floor1/magn_images 为生成的floor1的地磁信号强度分布图的存储位置、

data/site1/floor1/wifi_images 为生成的floor1的所有Wi-Fi AP信号强度分布图的存储位置

data/site1/floor1/ibeacon_images 为生成的floor1的所有iBeacon信号强度分布图的存储位置

## 数据文件说明（*.txt）

示例：
1574659531598	TYPE_WAYPOINT	196.41757	117.84907

1574659531695	TYPE_ACCELEROMETER	-1.7085724	-0.274765	16.657166	2
1574659531695	TYPE_MAGNETIC_FIELD	20.181274	16.209412	-32.22046	3
1574659531695	TYPE_GYROSCOPE	-0.3021698	0.2773285	0.107543945	3
1574659531695	TYPE_ROTATION_VECTOR	-0.00855688	0.051367603	0.362504	3
1574659531695	TYPE_MAGNETIC_FIELD_UNCALIBRATED	-29.830933	-26.36261	-300.3006	-50.012207	-42.57202	-268.08014	3
1574659531695	TYPE_GYROSCOPE_UNCALIBRATED	-0.42333984	0.20202637	0.09623718	-7.9345703E-4	3.2043457E-4	4.119873E-4	3
1574659531695	TYPE_ACCELEROMETER_UNCALIBRATED	-1.7085724	-0.274765	16.657166	0.0	0.0	0.0	3
1574659531715	TYPE_ACCELEROMETER	-1.9306335	-0.44595337	17.409546	2
1574659531715	TYPE_MAGNETIC_FIELD	20.874023	17.596436	-34.231567	3
1574659531715	TYPE_GYROSCOPE	-0.10083008	0.3487091	0.0846405	3
1574659531715	TYPE_ROTATION_VECTOR	-0.020168738	0.051000558	0.37465692	3
1574659531715	TYPE_MAGNETIC_FIELD_UNCALIBRATED	-29.138184	-24.975586	-302.3117	-50.012207	-42.57202	-268.08014	3
1574659531715	TYPE_GYROSCOPE_UNCALIBRATED	-0.20974731	0.32878113	0.100494385	-7.9345703E-4	3.2043457E-4	4.119873E-4	3
1574659531715	TYPE_ACCELEROMETER_UNCALIBRATED	-1.9306335	-0.44595337	17.409546	0.0	0.0	0.0	3

1574659533190	TYPE_WIFI	cloud time_license_5	1e:74:9c:a7:b2:e4	-43	5805	1574659532307
1574659533190	TYPE_WIFI	intime_lease	12:74:9c:a7:b2:e4	-43	5805	1574659532306
1574659533190	TYPE_WIFI	intime_pos	06:74:9c:a7:b2:e4	-43	5805	1574659532303
1574659533190	TYPE_WIFI	intime_office	0a:74:9c:a7:b2:e4	-43	5805	1574659532304
1574659533190	TYPE_WIFI	intime_free	0e:74:9c:a7:b2:e4	-43	5805	1574659532305
1574659533190	TYPE_WIFI		16:74:9c:a7:b2:e4	-43	5805	1574659532296

1574659532741	TYPE_BEACON	9195B3AD-A9D0-4500-85FF-9FB0F65A5201	0	0	-56	-91	38.10374756210322	E0:78:A3:3E:98:F8	1574659532741
1574659532751	TYPE_BEACON	FDA50693-A4E2-4FB1-AFCF-C6EB07647825	10073	61418	-65	-82	5.50634293288929	6B:11:4C:D1:29:F2	1574659532751
1574659533256	TYPE_BEACON	9195B3AD-A9D0-4500-85FF-9FB0F65A5201	0	0	-56	-83	18.800756409797202	E0:78:A3:3E:96:93	1574659533256
1574659533430	TYPE_BEACON	FDA50693-A4E2-4FB1-AFCF-C6EB07647825	10073	61418	-65	-82	5.50634293288929	75:16:C4:11:0F:E6	1574659533430

第一列为手机操作系统Unix时间戳，单位为毫秒

第二列为数据类型
TYPE_ACCELEROMETER 为加速度计数据
TYPE_MAGNETIC_FIELD 为磁力计数据
TYPE_GYROSCOPE 为陀螺仪数据
TYPE_ROTATION_VECTOR 为旋转矢量数据
TYPE_MAGNETIC_FIELD_UNCALIBRATED 为未校准磁力计数据
TYPE_GYROSCOPE_UNCALIBRATED 为未校准陀螺仪数据
TYPE_ACCELEROMETER_UNCALIBRATED	为未校准加速度计数据
TYPE_WIFI 为Wi-Fi数据
TYPE_BEACON 为iBeacon类型数据
TYPE_WAYPOINT 为真值坐标数据

第三列开始为数据内容
对于类型为TYPE_ACCELEROMETER、TYPE_ACCELEROMETER、TYPE_GYROSCOPE、TYPE_ROTATION_VECTOR的，第3列至第5列分别为X、Y和Z轴的数据，亦即安卓操作系统回调onSensorChanged()返回的SensorEvent.values[0-2]的内容，第6列为此时的传感器精度，亦即安卓操作系统回调onAccuracyChanged返回的内容。

对于类型为TYPE_ACCELEROMETER_UNCALIBRATED、TYPE_GYROSCOPE_UNCALIBRATED、TYPE_MAGNETIC_FIELD_UNCALIBRATED的，第3至第8列为安卓操作系统回调onSensorChanged()返回的SensorEvent.values[0-5]的内容，第9列为此时的传感器精度，亦即安卓操作系统回调onAccuracyChanged返回的内容。

更多可以参考https://developer.android.com/guide/topics/sensors

对于类型为TYPE_WIFI的，第3列为ssid，第4列为bssid，第5列为RSSI，第6列表明该Wi-Fi AP是2.5GHz或是5GHz，第7列为last seen timestamp。关于last seen timestamp可以参考https://developer.android.com/reference/android/net/wifi/ScanResult.html#timestamp

对于类型为TYPE_BEACON的，实际指的是iBeacon数据。第3列为UUID，第4列为major ID，第5列为minor ID，第6列为接收到的功率，第7列为RSSI，第8列为distance，第9列为mac，第10列与第1列系统时间戳相同，没有实际意义。

对于类型为TYPE_WAYPOINT的，第3列至第4列分别指X轴、Y轴坐标，单位为米。
