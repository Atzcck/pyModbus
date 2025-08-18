from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("192.168.2.30", port=502)

if client.connect():
    print("Connected to Modbus server.")

    # Write a coil (True/False)
    client.write_coil(0, True)
    client.write_coil(1, True)
    client.write_coil(2, True)
    client.write_coil(3, True)
    client.write_coil(4, True)
    result = client.read_coils(address=5, count=5, device_id=1)
    print("Coils:", result.bits)

    # Write a holding register (integer value)
    #client.write_register(0, 123)
    #client.write_register(1, 123)
    #client.write_register(2, 123)
    #client.write_register(3, 123)
    #client.write_register(4, 123)
    mbuslist = [10, 20, 30, 40, 50]
    client.write_registers(0, values= mbuslist, device_id=1 )

    result = client.read_holding_registers(address=5, count=5, device_id=1)
    print("Holding Registers:", result.registers)

    client.close()
else:
    print("Failed to connect.")