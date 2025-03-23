from ultralytics import YOLO

# YOLOv8 モデルの読み込み
model = YOLO('yolov8n.pt')

# カメラ映像のリアルタイム推論 (video_path=0 でカメラ入力)
for results in model.predict(source=0, show=True, stream=True):
    # 画像サイズ（高さ, 幅）を取得
    imageHeight, imageWidth = results.orig_shape[:2]

    # オブジェクト名とクラス情報
    names = results.names
    classes = results.boxes.cls
    boxes = results.boxes

    # 検出結果のループ処理
    for box, cls in zip(boxes, classes):
        name = names[int(cls)]
        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]

        # X軸の物体中心位置
        ObjectXAxisCenter = (x1 + x2) / 2

        # 画像の左端からの割合
        PercentFromLeft = (ObjectXAxisCenter / imageWidth) 

        # 検出情報の表示
        print(f"Object: {name}, imageWidth={imageWidth}, PercentFromLeft={PercentFromLeft:.2f}")
        
