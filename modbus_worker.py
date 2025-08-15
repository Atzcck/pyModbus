from PySide6.QtCore import QThread, Signal
from pymodbus.client import ModbusTcpClient
import time

class ModbusWorker(QThread):
    data_received = Signal(dict)       # Emits {'coils': [...], 'registers': [...]}
    status_changed = Signal(str)       # Emits connection status messages

    def __init__(self, host="127.0.0.1", port=5020, device_id=1):
        super().__init__()
        self.host = host
        self.port = port
        self.device_id = device_id
        self.running = True

    def run(self):
        client = ModbusTcpClient(self.host, port=self.port)
        while self.running:
            if not client.connect():
                self.status_changed.emit("Disconnected, retrying...")
                time.sleep(2)
                continue

            self.status_changed.emit("Connected")
            try:
                coils = client.read_coils(address=0, count=10, device_id=self.device_id)
                hr = client.read_holding_registers(address=0, count=10, device_id=self.device_id)

                if not coils.isError() and not hr.isError():
                    self.data_received.emit({
                        "coils": coils.bits,
                        "registers": hr.registers
                    })
            except Exception as e:
                self.status_changed.emit(f"Error: {e}")

            time.sleep(1)  # Poll every second

        client.close()

    def stop(self):
        self.running = False
        self.wait()