import asyncio
import websockets

class CommandClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.camera_id = 0
        self.is_running = False
        self.targets = []  # 送信するデータを保持する変数
        self.send_task = None  # データ送信タスクを保持する変数

    async def receive_cameraid(self):
        """ROS2側サーバから受信したカメラIDを格納"""
        try:
            async for cmd in self.websocket:
                self.camera_id = int(cmd)
                print(f"Get new Camera ID from ROS2: {cmd}")
        except websockets.ConnectionClosed:
            print("Connection closed. Reconnecting...")
            await self.reconnect()

    async def connect(self):
        """WebSocket接続を確立する"""
        while True:
            try:
                print(f"Connecting to {self.uri}...")
                self.websocket = await websockets.connect(self.uri)
                print("Connected!")
                break  # 接続成功したらループを抜ける
            except (websockets.ConnectionClosed, ConnectionRefusedError, OSError) as e:
                print(f"Connection failed: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)  # 5秒待機して再接続

    async def reconnect(self):
        """再接続を行う"""
        if self.websocket:
            await self.websocket.close()
        await self.connect()
        await self.receive_cameraid()

    async def run(self):
        """WebSocket接続を確立し、受信を実行する"""
        self.is_running = True
        await self.connect()
        await self.receive_cameraid()

    async def _sendPiDataAsync(self):
        """0.1秒ごとにデータを送信する"""
        while self.is_running:
            if self.websocket and self.targets:
                try:
                    await self.websocket.send(f"{','.join(self.targets)}")
                    print(f"Sent data: {self.targets}")
                except websockets.ConnectionClosed:
                    print("Connection closed during send. Reconnecting...")
                    await self.reconnect()
            await asyncio.sleep(0.1)  # 0.1秒待機

    def getPiData(self):
        """カメラIDを取得する"""
        return self.camera_id

    def sendPiData(self, targets):
        """送信するデータを更新し、送信タスクを開始する"""
        self.targets = targets  # クラス内の変数を更新
        if not self.send_task:  # 送信タスクが未開始の場合
            self.send_task = asyncio.create_task(self._sendPiDataAsync())
