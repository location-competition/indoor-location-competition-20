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
6. 可视化本楼层不同地点扫到wifi个数的分布情况。

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

data/site1/F1 为包含F1楼层的所有数据的文件夹

data/site1/F1/path_data_files 为包含F1的所有原始数据文件的文件夹

data/site1/F1/floor_image.png 为F1的楼层地图

data/site1/F1/floor_info.json 为包含F1地图尺寸信息的文件

data/site1/F1/geojson_map.json 为F1的地图的geojson文件

data/site1/F1/path_images 为生成的F1的所有path真值轨迹图的存储位置

data/site1/F1/magn_images 为生成的F1的地磁信号强度分布图的存储位置、

data/site1/F1/wifi_images 为生成的F1的所有Wi-Fi AP信号强度分布图的存储位置

data/site1/F1/ibeacon_images 为生成的F1的所有iBeacon信号强度分布图的存储位置

## 数据文件说明（*.txt）

| Unix Timestamp\(ms\) | Data Type                                           | Column3                                  | Column4           | Column4      | Column5          | Column6             | Column7           | Column8           | Column9                                |
|----------------------|-----------------------------------------------------|------------------------------------------|-------------------|--------------|------------------|---------------------|-------------------|-------------------|----------------------------------------|
| 1574659531598        | TYPE\_WAYPOINT                                      | 196\.41757                               | 117\.84907        |              |                  |                     |                   |                   |                                        |
|                      | The position that collector labels on the map       | Coordinate x                             | Coordiante y      |              |                  |                     |                   |                   |                                        |
|                      |                                                     |                                          |                   |              |                  |                     |                   |                   |                                        |
| 1574659531695        | TYPE\_ACCELEROMETER                                 | \-1\.7085724                             | \-0\.274765       | 16\.657166   | 2                |                     |                   |                   |                                        |
|                      | Android Sensor\.TYPE\_ACCELEROMETER                 | X axis                                   | Y axis            | Z axis       | accuracy         |                     |                   |                   |                                        |
| 1574659531695        | TYPE\_GYROSCOPE                                     | \-0\.3021698                             | 0\.2773285        | 0\.107543945 | 3                |                     |                   |                   |                                        |
|                      | Android Sensor\.TYPE\_GYROSCOPE                     | X axis                                   | Y axis            | Z axis       | accuracy         |                     |                   |                   |                                        |
| 1574659531695        | TYPE\_MAGNETIC\_FIELD                               | 20\.181274                               | 16\.209412        | \-32\.22046  | 3                |                     |                   |                   |                                        |
|                      | Android Sensor\.TYPE\_MAGNETIC\_FIELD               | X axis                                   | Y axis            | Z axis       | accuracy         |                     |                   |                   |                                        |
| 1574659531695        | TYPE\_ROTATION\_VECTOR                              | \-0\.00855688                            | 0\.051367603      | 0\.362504    | 3                |                     |                   |                   |                                        |
|                      | Android Sensor\.TYPE\_ROTATION\_VECTOR              | X axis                                   | Y axis            | Z axis       | accuracy         |                     |                   |                   |                                        |
|                      |                                                     |                                          |                   |              |                  |                     |                   |                   |                                        |
| 1574659531695        | TYPE\_ACCELEROMETER\_UNCALIBRATED                   | \-1\.7085724                             | \-0\.274765       | 16\.657166   | 0\.0             | 0\.0                | 0\.0              | 3                 |                                        |
|                      | Android Sensor\.TYPE\_ACCELEROMETER\_UNCALIBRATED   | X axis                                   | Y axis            | Z axis       | X axis           | Y axis              | Z axis            | accuracy          |                                        |
| 1574659531695        | TYPE\_GYROSCOPE\_UNCALIBRATED                       | \-0\.42333984                            | 0\.20202637       | 0\.09623718  | \-7\.9345703E\-4 | 3\.2043457E\-4      | 4\.119873E\-4     | 3                 |                                        |
|                      | Android Sensor\.TYPE\_GYROSCOPE\_UNCALIBRATED       | X axis                                   | Y axis            | Z axis       | X axis           | Y axis              | Z axis            | accuracy          |                                        |
| 1574659531695        | TYPE\_MAGNETIC\_FIELD\_UNCALIBRATED                 | \-29\.830933                             | \-26\.36261       | \-300\.3006  | \-50\.012207     | \-42\.57202         | \-268\.08014      | 3                 |                                        |
|                      | Android Sensor\.TYPE\_MAGNETIC\_FIELD\_UNCALIBRATED | X axis                                   | Y axis            | Z axis       | X axis           | Y axis              | Z axis            | accuracy          |                                        |
|                      |                                                     |                                          |                   |              |                  |                     |                   |                   |                                        |
| 1574659533190        | TYPE\_WIFI                                          | intime\_free                             | 0e:74:9c:a7:b2:e4 | \-43         | 5805             | 1574659532305       |                   |                   |                                        |
|                      | Wi\-Fi data                                         | ssid                                     | bssid             | RSSI         | frequency        | last seen timestamp |                   |                   |                                        |
|                      |                                                     |                                          |                   |              |                  |                     |                   |                   |                                        |
| 1574659532751        | TYPE\_BEACON                                        | FDA50693\-A4E2\-4FB1\-AFCF\-C6EB07647825 | 10073             | 61418        | \-65             | \-82                | 5\.50634293288929 | 6B:11:4C:D1:29:F2 | 1574659532751                          |
|                      | iBeacon data                                        | UUID                                     | MajorID           | MinorID      | Tx Power         | RSSI                | distance          | mac address       | same with UNIX timestamp, padding data |


第一列为Unix时间戳，单位为毫秒
对于sensor类型的数据，这个时间戳是SensorEvent.timestamp对齐到UNIX时间戳后的数值。
对于其他类型的数据，这个时间戳是程序运行时UNIX系统时间戳。

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
对于类型为TYPE_WAYPOINT的，第3列至第4列分别指X轴、Y轴坐标，单位为米。

对于类型为TYPE_ACCELEROMETER、TYPE_ACCELEROMETER、TYPE_GYROSCOPE、TYPE_ROTATION_VECTOR的，第3列至第5列分别为X、Y和Z轴的数据，亦即安卓操作系统回调onSensorChanged()返回的SensorEvent.values[0-2]的内容，第6列为此时的传感器精度，SensorEvent.accuracy。
对于类型为TYPE_ACCELEROMETER_UNCALIBRATED、TYPE_GYROSCOPE_UNCALIBRATED、TYPE_MAGNETIC_FIELD_UNCALIBRATED的，第3至第8列为安卓操作系统回调onSensorChanged()返回的SensorEvent.values[0-5]的内容，第9列为此时的传感器精度，SensorEvent.accuracy。
参考：https://developer.android.com/guide/topics/sensors

对于类型为TYPE_WIFI的，第3列为ssid，第4列为bssid，第5列为RSSI，第6列为Wi-Fi AP的frequency，第7列为last seen timestamp。
参考：https://developer.android.com/reference/android/net/wifi/ScanResult.html

对于类型为TYPE_BEACON的，实际指的是iBeacon数据。调用安卓接口为ScanRecord.getBytes()。然后根据iBeacon协议做了解析，解析代码：
val major = ((scanRecord[startByte + 20].toInt() and 0xff) * 0x100 + (scanRecord[startByte + 21].toInt() and 0xff))
val minor = ((scanRecord[startByte + 22].toInt() and 0xff) * 0x100 + (scanRecord[startByte + 23].toInt() and 0xff))
val txPower = scanRecord[startByte + 24]
第3列为UUID，第4列为major ID，第5列为minor ID，第6列为接收到的功率，第7列为RSSI，第8列为distance，第9列为mac，第10列与第1列系统时间戳相同，没有实际意义。
distance的计算公式为：
```
private static double calculateDistance(int txPower, double rssi) {
  if (rssi == 0) {
    return -1.0; // if we cannot determine distance, return -1.
  }
  double ratio = rssi*1.0/txPower;
  if (ratio < 1.0) {
    return Math.pow(ratio,10);
  }
  else {
    double accuracy =  (0.89976)*Math.pow(ratio,7.7095) + 0.111;
    return accuracy;
  }
}
```
参考：https://developer.android.com/reference/android/bluetooth/le/ScanRecord
