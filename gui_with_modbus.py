# gui_with_modbus.py
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QThread, QObject
from modbus_server import ModbusServer

class ModbusWorker(QObject):
    def __init__(self):
        super().__init__()
        self.server = ModbusServer()

    def run(self):
        self.server.start()  # Blocking inside thread


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 with ModbusTCP Server")

        layout = QVBoxLayout(self)
        self.status_label = QLabel("Server stopped")
        start_button = QPushButton("Start Modbus Server")

        start_button.clicked.connect(self.start_server)

        layout.addWidget(self.status_label)
        layout.addWidget(start_button)

    def start_server(self):
        self.thread = QThread()
        self.worker = ModbusWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        self.status_label.setText("Server running...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())