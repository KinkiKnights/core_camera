import asyncio
import websockets

# グローバル変数に設定されたものを随時送信・更新
targets = []
camera_id = 1

async def websocket_handler(websocket):
    global targets
    print("WebSocket 接続完了")

    try:
        # クライアントに定期的に camera_id を送信するタスクを作成
        async def send_camera_id():
            while True:
                await websocket.send(str(camera_id))
                await asyncio.sleep(0.1)  # 0.1秒待機

        # メッセージ受信と camera_id 送信を並行して実行
        send_task = asyncio.create_task(send_camera_id())
        async for message in websocket:
            print(f"受信データ: {message}")
            try:
                targets = list(map(int, message.split(',')))
            except ValueError:
                print("数値変換エラー")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket 切断")
    finally:
        # タスクが終了したらキャンセルする
        send_task.cancel()

async def ws_wait():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8100):
        print("WebSocket start listen (ws://0.0.0.0:8100)")
        await asyncio.Future()

# メインループを開始
asyncio.run(ws_wait())