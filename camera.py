import cv2
from command_client import CommandClient


class CameraSwitcher:
    def __init__(self, camera_indices, resolutions, screen_size, window_name):
        """
        初期化
        :param camera_indices: 使用するカメラのインデックスリスト（例: [0, 2]）
        :param resolutions: 解像度の設定（例: {'low': (640, 480), 'high': (1280, 720)}）
        :param screen_size: 画面の解像度（例: (1920, 1080)）
        :param window_name: ウィンドウの名前（例: 'Camera Switcher'）
        """
        self.camera_indices = camera_indices
        self.resolutions = resolutions
        self.screen_size = screen_size
        self.window_name = window_name
        self.caps = [cv2.VideoCapture(idx) for idx in camera_indices]
        self.current_camera = 0  # 現在表示中のカメラのインデックス
        self.last_id = 0  # 最後に受信したカメラID

        # カメラが開けなかった場合のエラーハンドリング
        for i, cap in enumerate(self.caps):
            if not cap.isOpened():
                print(f"カメラ{i}を開けませんでした")
                self.release_resources()
                exit()

        # ウィンドウの設定
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def switch_camera(self, camera_index, resolution_key):
        """
        カメラを切り替える
        :param camera_index: 切り替えるカメラのインデックス
        :param resolution_key: 解像度のキー（例: 'low' または 'high'）
        """
        if 0 <= camera_index < len(self.caps):
            self.current_camera = camera_index
            width, height = self.resolutions[resolution_key]
            self.caps[camera_index].set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.caps[camera_index].set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            print(f"カメラ{camera_index + 1} {resolution_key}に切り替えました")

    def update_from_server(self, new_id):
        """
        サーバから受信したIDに基づいてカメラを切り替える
        :param new_id: サーバから受信した新しいカメラID
        """
        if self.last_id != new_id:
            self.last_id = new_id
            if new_id == 1:
                self.switch_camera(0, 'low')
            elif new_id == 2:
                self.switch_camera(0, 'high')
            elif new_id == 4:
                self.switch_camera(1, 'low')
            elif new_id == 5:
                self.switch_camera(1, 'high')

    def run(self):
        """メインループを実行する"""
        while True:
            # 現在のカメラからフレームを取得
            ret, frame = self.caps[self.current_camera].read()
            if not ret:
                print("フレームを取得できませんでした")
                break

            # フレームを画面サイズにリサイズ
            resized_frame = cv2.resize(frame, self.screen_size, interpolation=cv2.INTER_LINEAR)

            # フレームを表示
            cv2.imshow(self.window_name, resized_frame)

            # キー入力を待つ
            key = cv2.waitKey(1) & 0xFF

            # キーに応じてカメラを切り替え
            if key == ord('1'):
                self.switch_camera(0, 'low')
            elif key == ord('2'):
                self.switch_camera(0, 'high')
            elif key == ord('4'):
                self.switch_camera(1, 'low')
            elif key == ord('5'):
                self.switch_camera(1, 'high')
            elif key == ord('q'):  # 'q'キーで終了
                break

        # リソースを解放
        self.release_resources()

    def release_resources(self):
        """リソースを解放する"""
        for cap in self.caps:
            cap.release()
        cv2.destroyAllWindows()


# 設定
CAMERA_INDICES = [0, 2]  # 使用するカメラのインデックス
RESOLUTIONS = {
    'low': (640, 480),   # 低画質
    'high': (1280, 720)  # 高画質
}
SCREEN_SIZE = (1920, 1080)  # 画面の解像度
WINDOW_NAME = 'Camera Switcher'

# CommandClientの初期化
client = CommandClient("ws://192.168.4.2:8100")

# CameraSwitcherの初期化
switcher = CameraSwitcher(CAMERA_INDICES, RESOLUTIONS, SCREEN_SIZE, WINDOW_NAME)

def CameraRun():
    # メインループ
    try:
        while True:
            # サーバからカメラIDを取得
            new_id = client.getPiData()
            switcher.update_from_server(new_id)

            # カメラ表示を更新
            switcher.run()
    except KeyboardInterrupt:
        print("プログラムを終了します")

async def ComandClientStart():
    client = CommandClient("ws://192.168.4.1:8100")
    await client.run()

cam_thread = threading.Thread(target=CameraRun)
cam_thread.daemon = True
cam_thread.start()
# イベントループを実行
asyncio.run(_ComandClientStart())
