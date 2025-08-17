import asyncio
import json
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
import httpx
import websockets


API_BASE = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws"


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Super Agent - PyQt6")
        self.resize(900, 600)

        self.prompt = QtWidgets.QTextEdit()
        self.output = QtWidgets.QTextEdit()
        self.output.setReadOnly(True)

        self.provider = QtWidgets.QComboBox()
        self.provider.addItems(["ollama", "openai", "gemini", "anthropic"]) 

        self.model = QtWidgets.QLineEdit()
        self.model.setPlaceholderText("Optional model name")

        self.run_btn = QtWidgets.QPushButton("Complete")
        self.run_btn.clicked.connect(self.on_complete)

        self.status = QtWidgets.QLabel("Ready")

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QLabel("Provider"), 0, 0)
        layout.addWidget(self.provider, 0, 1)
        layout.addWidget(QtWidgets.QLabel("Model"), 0, 2)
        layout.addWidget(self.model, 0, 3)
        layout.addWidget(self.run_btn, 0, 4)
        layout.addWidget(QtWidgets.QLabel("Prompt"), 1, 0, 1, 5)
        layout.addWidget(self.prompt, 2, 0, 1, 5)
        layout.addWidget(QtWidgets.QLabel("Output"), 3, 0, 1, 5)
        layout.addWidget(self.output, 4, 0, 1, 5)
        layout.addWidget(self.status, 5, 0, 1, 5)

        # start websocket in background
        self.ws_task = asyncio.create_task(self.ws_listener())

    async def ws_listener(self):
        try:
            async with websockets.connect(WS_URL) as ws:
                await ws.send("pyqt6-client-connected")
                async for msg in ws:
                    self.output.append(f"[ws] {msg}")
        except Exception as exc:
            self.output.append(f"[ws-error] {exc}")

    def on_complete(self):
        asyncio.create_task(self._complete())

    async def _complete(self):
        self.status.setText("Running...")
        payload = {
            "prompt": self.prompt.toPlainText(),
            "provider": self.provider.currentText(),
            "model": self.model.text() or None,
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{API_BASE}/api/ai/complete", json=payload, timeout=60)
                data = resp.json()
                self.output.setPlainText(data.get("text", ""))
        except Exception as exc:
            self.output.setPlainText(str(exc))
        finally:
            self.status.setText("Done")


def qt_async_run():
    app = QtWidgets.QApplication(sys.argv)
    loop = asyncio.new_event_loop()

    QtCore.QTimer.singleShot(0, lambda: asyncio.set_event_loop(loop))

    w = MainWindow()
    w.show()

    def run_loop():
        loop.run_forever()

    thread = QtCore.QThread()
    thread.run = run_loop
    thread.start()

    ret = app.exec()
    loop.call_soon_threadsafe(loop.stop)
    thread.quit()
    thread.wait()
    sys.exit(ret)


if __name__ == "__main__":
    qt_async_run()