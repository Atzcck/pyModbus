# test_server.py
from modbus_server import ModbusServer

if __name__ == "__main__":
    server = ModbusServer(host="127.0.0.1", port=5020)
    server.start()  # Blocking call