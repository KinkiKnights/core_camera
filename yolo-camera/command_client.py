import websocket
import threading

class CommandClientBlock:
    def sendPiData(self, target):
        self.ws.send(str(target));

    def getCameraID(self):
        return self.camera_id

    def on_message(self, ws, message):
        self.camera_id = int(message)
        print(f"Received: {self.camera_id}")

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):
        print("Connection opened")
    def run(self):
        self.ws = websocket.WebSocketApp(
            self.address, 
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        # ブロッキング実行
        self.ws.run_forever()
    def __init__(self, address):
        self.address = address
        self.target = 127
        self.camera_id = 0
