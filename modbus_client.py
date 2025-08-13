from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=5020)

if client.connect():
    print("Connected to Modbus server.")

    # Write a coil (True/False)
    client.write_coil(0, True)
    result = client.read_coils(address=0, count=5, device_id=1, no_response_expected=False)
    print("Coils:", result.bits)

    # Write a holding register (integer value)
    client.write_register(0, 123)
    result = client.read_holding_registers(address=0, count=5, device_id=1, no_response_expected= False)
    print("Holding Registers:", result.registers)

    client.close()
else:
    print("Failed to connect.")