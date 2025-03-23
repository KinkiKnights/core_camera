# 設計
## camera.py
カメラ用PC上で動作する。
YoloV8の処理とカメラの画面表示、カメラの切り替えを行う。
直接指令を送ることができないため、制御用ラズパイから制御情報を受け取る

## command_client.py
制御用ラズパイとのデータの送受信をWebSocketで行うモジュール
Websocketsのクライアントとしてふるまう

## ros2_camera_commander.py
制御用ラズパイ上で動作する。WebSocketysサーバー
カメラ切り替え番号のSubscription・送信と認識されたターゲット情報の受信・Publishを行う。
現状、Webscoketsサーバー部分のみ実装。
ROS2のパッケージ化が必要# core_camera
