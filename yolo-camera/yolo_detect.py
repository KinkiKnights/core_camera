from ultralytics import YOLO
"""
画像認識実装
"""
class YoloDetection():
    def __init__(self, port):
        # YOLOv8 モデルの読み込み
        self.model = YOLO('/home/kk/core-camera/yolo-camera/best-3-26-epochs=500.pt') # モデル .pt までのフルパス(/home/kk~)を入力
        self.port = port
        self.targets= [];
#モデルはこのファイルと同じディレクトリに保存することをお勧めする
    def sort_by_nearest_to_half(self, arr):
        # 0.5 との距離を基準に並び替え
        return sorted(arr, key=lambda x: abs(x - 0.5))

    def sendPiData(self, data):
        print("======Damage Panel Pos======")
        print(data)
        self.targets= data;

    def getTargets(self):
        return self.targets

    def run(self):
        # カメラ映像のリアルタイム推論 (source=でカメラ入力)
        for results in self.model.predict(source=self.port, show=False, stream=True):
            # 画像サイズ（高さ, 幅）を取得
            imageHeight, imageWidth = results.orig_shape[:2]

            # オブジェクト名とクラス情報
            names = results.names
            classes = results.boxes.cls
            boxes = results.boxes
            ObjectInfo = [] # 配列を定義
            
            # 検出結果のループ処理
            for box, cls in zip(boxes, classes):
                num_objects = len(boxes) # 検出された物体の数

                # クラス番号0(person)のみの場合
                #if int(cls) == 0:
                name = names[int(cls)]
                x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
                # X軸の物体中心位置
                ObjectXAxisCenter = (x1 + x2) / 2
                # 画像の左端からの割合
                PercentFromLeft = (ObjectXAxisCenter / imageWidth) 
                # 検出情報の表示
                print(f"Object: {name}, imageWidth={imageWidth}, PercentFromLeft={PercentFromLeft}")
                ObjectInfo.append(PercentFromLeft)# 配列に追加
                sortedObjectInfo = self.sort_by_nearest_to_half(ObjectInfo) # 0.5 との距離を基準に並び替え
                self.sendPiData(ObjectInfo) # データを送信