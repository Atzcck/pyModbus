# modbus_server.py
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging

# Optional: enable logging for debugging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


class ModbusServer:
    def __init__(self, host="127.0.0.1", port=5020):
        self.host = host
        self.port = port

        # Create Modbus datastore (holding registers, coils, etc.)
        # Here: holding registers [0-99] initialized with value 0

        device_context = ModbusDeviceContext(
            di=ModbusSequentialDataBlock(0, [0]*100),
            co=ModbusSequentialDataBlock(0, [0]*100),
            hr=ModbusSequentialDataBlock(0, [0]*100),
            ir=ModbusSequentialDataBlock(0, [0]*100),
        )
         # Use device IDs instead of slave(s)
        self.context = ModbusServerContext(devices= {1: device_context}, single= False,)

    def start(self):
        """Start the Modbus TCP server (blocking)."""
        log.info(f"Starting Modbus TCP server on {self.host}:{self.port}")
        StartTcpServer(self.context, address=(self.host, self.port))