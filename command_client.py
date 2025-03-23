import asyncio
import websockets
import datetime

class CommandClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.camera_id = 0;
        asyncio.run(self.run())

    async def receive_cameraid(self):
        """ROS2側サーバから受信したカメラIDを格納"""
        while True:
            if self.websocket:
                cmd = await self.websocket.recv()
                self.camera_id = int(cmd);
                print(f"Get new Camera ID from ROS2: {cmd}")
            else:
                await asyncio.sleep(1)

    async def run(self):
        """WebSocket接続を確立し、受信を実行する"""
        self.websocket = await websockets.connect(self.uri)
        await self.receive_cameraid()


    async def _sendPiDataAsync(self, targets):
        """外部から呼び出された際に、指定された時刻データを送信する"""
        if self.websocket:
            await self.websocket.send(f"{targets.join(',')}")
        else:
            print("WebSocket is not connected.")
    """
    以降、モジュール外からの呼び出しを想定した関数
    """
    def getPiData(self):
        return self.camera_id
    
    def sendPiData(self, targets):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # イベントループが実行されていない場合
            loop = None

        if loop and loop.is_running():
            # イベントループが実行中の場合は、タスクとしてスケジュール
            loop.create_task(self._sendPiDataAsync(targets))
 