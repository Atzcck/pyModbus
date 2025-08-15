from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Slot
from modbus_worker import ModbusWorker

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modbus GUI Monitor")

        self.status_label = QLabel("Status: Disconnected")
        self.coils_label = QLabel("Coils: -")
        self.registers_label = QLabel("Registers: -")
        self.write_button = QPushButton("Write Coil 0 / Register 0")

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.coils_label)
        layout.addWidget(self.registers_label)
        layout.addWidget(self.write_button)
        self.setLayout(layout)

        # Start Modbus worker thread
        self.worker = ModbusWorker()
        self.worker.status_changed.connect(self.update_status)
        self.worker.data_received.connect(self.update_data)
        self.worker.start()

        self.write_button.clicked.connect(self.write_values)

    @Slot(str)
    def update_status(self, status):
        self.status_label.setText(f"Status: {status}")

    @Slot(dict)
    def update_data(self, data):
        self.coils_label.setText(f"Coils: {data['coils']}")
        self.registers_label.setText(f"Registers: {data['registers']}")

    def write_values(self):
        # You can write values directly here (blocking, quick demo)
        from pymodbus.client import ModbusTcpClient
        client = ModbusTcpClient("127.0.0.1", port=5020)
        if client.connect():
            client.write_coil(0, True, device_id=1)
            client.write_register(0, 999, device_id=1)
            client.close()

    def closeEvent(self, event):
        self.worker.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()