import cv2
from command_client import CommandClient

client = CommandClient("ws://localhost:8100")
last_id = client.getPiData()

# # カメラデバイスを開く
cap1 = cv2.VideoCapture(0)  # カメラ1
if not cap1.isOpened():
    print("カメラ1を開けませんでした")
    exit()
cap2 = cv2.VideoCapture(2)  # カメラ2
if not cap2.isOpened():
    print("カメラ2を開けませんでした")
    exit()

# 解像度の設定（低画質と高画質）
resolutions = {
    'low': (640, 480),   # 低画質: 640x480
    'high': (1280, 720)  # 高画質: 1280x720
}

# 画面の解像度を取得
screen_width = 1920  # 画面の幅（例: 1920x1080）
screen_height = 1080  # 画面の高さ

# ウィンドウの名前を設定
window_name = 'Camera Switcher'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 現在表示中のカメラを表す変数
current_camera = 1  # 1: カメラ1, 2: カメラ2

while True:
    # 現在のカメラからフレームを取得
    if current_camera == 1:
        ret, frame = cap1.read()
    else:
        ret, frame = cap2.read()

    if not ret:
        print("フレームを取得できませんでした")
        break

    # カメラ画像を画面サイズにリサイズ
    resized_frame = cv2.resize(frame, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)

    # フレームを表示
    cv2.imshow(window_name, resized_frame)

    # キー入力を待つ
    key = cv2.waitKey(1) & 0xFF

    # '1,2'キーを押すとカメラ1に切り替え
    if key == ord('1'):
        current_camera = 1
        cap1.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["low"][0])
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["low"][1])
        print("カメラ1 Lowに切り替えました")
    elif key == ord('2'):
        current_camera = 1
        cap1.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["high"][0])
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["high"][1])
        print("カメラ1 Highに切り替えました")

    # '4,5'キーを押すとカメラ2に切り替え
    elif key == ord('4'):
        current_camera = 2
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["low"][0])
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["low"][1])
        print("カメラ2 Lowに切り替えました")
    elif key == ord('5'):
        current_camera = 2
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["high"][0])
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["high"][1])
        print("カメラ2 Highに切り替えました")
    
    # サーバから受信したIDが更新されていれば切り替え
    now_id = client.getPiData()
    if (last_id != now_id):
        if now_id == 1:
            last_id = now_id
            current_camera = 1
            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["low"][0])
            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["low"][1])
            print("カメラ1 Lowに切り替えました")
        elif n_idow == 2:
            last_id = now_id
            current_camera = 1
            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["high"][0])
            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["high"][1])
            print("カメラ1 Highに切り替えました")

        # '4,5'キーを押すとカメラ2に切り替え
        elif n_idow == 4:
            last_id = now_id
            current_camera = 2
            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["low"][0])
            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["low"][1])
            print("カメラ2 Lowに切り替えました")
        elif n_idow == 5:
            last_id = now_id
            current_camera = 2
            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions["high"][0])
            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions["high"][1])
            print("カメラ2 Highに切り替えました")


    # 'q'キーを押すとループを抜ける
    elif key == ord('q'):
        break

# リソースを解放
cap1.release()
cap2.release()
cv2.destroyAllWindows()