import cv2
import time
from ultralytics import YOLO
from command_client import CommandClientBlock
from yolo_detect import YoloDetection
import asyncio
import threading

"""
Websocketクライアント起動
"""
client = CommandClientBlock("ws://192.168.4.1:8100")
def WsRun():
    global client
    client.run()
ws_thread = threading.Thread(target=WsRun)
ws_thread.daemon = True
ws_thread.start()

"""
Yolo起動
"""
yolo_det = YoloDetection(2)
def YoloRun():
    global yolo_det
    yolo_det.run()
yolo_thread = threading.Thread(target=YoloRun)
yolo_thread.daemon = True
yolo_thread.start()

"""
カメラ初期化
"""
# 設定
camera_indice = [0, 4]  # 使用するカメラのインデックス
resolutions = (640, 480)
screen_size = (1920, 1080)  # 画面の解像度
window_name = 'Camera Switcher'

cap1 = cv2.VideoCapture(camera_indice[0])  # カメラ1
if not cap1.isOpened():
    print("カメラ1を開けませんでした")
    exit()
cap2 = cv2.VideoCapture(camera_indice[1])  # カメラ2
if not cap2.isOpened():
    print("カメラ2を開けませんでした")
    exit()

#  ウィンドウの設定
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

"""
メイン処理
"""
while True:
    cam_id = client.getCameraID()

    if cam_id == 0:
        ret, frame = cap1.read()
    else:
        ret, frame = cap2.read()
    if not ret:
        print("フレームを取得できませんでした")
        print("new Frame")
        # フレームを画面サイズにリサイズ
    resized_frame = cv2.resize(frame, screen_size, interpolation=cv2.INTER_LINEAR)

    if (cam_id == 0):
        # クロスヘア表示をオーバーレイ
        cv2.line(resized_frame, (0, screen_size[1] // 2),
                (screen_size[0], screen_size[1] // 2), (0, 0, 255), 2)
        cv2.line(resized_frame, (screen_size[0] // 2, 0), 
                (screen_size[0] // 2, screen_size[1]), (0, 0, 255), 2)
        
        # カメラから見える，「機体を中心とした円弧」を描画(ただしカメラは視野角60°で機体中心の高さ20cmの位置に取り付けられており、円弧は床面にあるものとする)
        # 画面の中心座標を取得
        center_x = screen_size[0] // 2
        center_y = screen_size[1] // 2
        # 円弧の中心座標を取得
        arc_center_x = center_x
        arc_center_y = center_y + 20 * screen_size[1] // 1080
        # 円弧の半径を取得
        arc_radius = screen_size[1] // 2
        # 円弧の開始角度と終了角度を取得
        arc_start_angle = 180 - 30
        arc_end_angle = 180 + 30
        # 円弧を描画
        cv2.ellipse(resized_frame, (arc_center_x, arc_center_y), (arc_radius, arc_radius), 0, arc_start_angle, arc_end_angle, (0, 255, 0), 2)

        # 画面左下，右下の両方から消失点までの線を描画(消失点はx座標が画面の中心，y座標が画面の上端から1/3の位置にあるものとする)
        # 消失点の座標を取得
        vanishing_point_x = center_x
        vanishing_point_y = screen_size[1] // 3
        # 画面左下から消失点までの線を描画
        cv2.line(resized_frame, (0, screen_size[1]), (vanishing_point_x, vanishing_point_y), (255, 0, 0), 2)
        # 画面右下から消失点までの線を描画
        cv2.line(resized_frame, (screen_size[0], screen_size[1]), (vanishing_point_x, vanishing_point_y), (255, 0, 0), 2)
    cv2.imshow(window_name, resized_frame)

    # キー入力を待つ(デバッグ用)
    key = cv2.waitKey(1) & 0xFF
    # キーに応じてカメラを切り替え
    if key == ord('1'):
        cam_id = 0                
        print(f"カメラ{cam_id}に切り替えました")
    elif key == ord('2'):
        cam_id = 1                
        print(f"カメラ{cam_id}に切り替えました")
    elif key == ord('0'):
        
        cap1.release()
        cap2.release()
        exit()
        
    # ここから検出値送信
    targets = yolo_det.getTargets();
    if (len(targets) < 1):
        target = 127
    else:
        target = int(targets[0] * 255)
    if (target < 0):
        target = 0
    elif (target > 255):
        target = 255
    client.sendPiData(target)