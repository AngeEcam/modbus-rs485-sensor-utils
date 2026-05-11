import logging
from pymodbus.client import ModbusSerialClient

logging.disable(logging.CRITICAL)

PORT = "/dev/tty.usbserial-A5069RR4"
SLAVE_ID = 1

client = ModbusSerialClient(
    port=PORT,
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=2,
)

if not client.connect():
    print("Connection failed")
    exit()

try:
    # Read temperature + humidity in one request
    # 0x0001 = temperature, 0x0002 = humidity
    result = client.read_input_registers(
        address=0x0001,
        count=2,
        device_id=SLAVE_ID
    )

    if hasattr(result, "registers"):
        registers = result.registers
        print("Raw registers:", registers)

        # Negative temperatures via two's complement
        raw_temp = registers[0]
        if raw_temp > 32767:
            temperature = (raw_temp - 65536) / 10.0
        else:
            temperature = raw_temp / 10.0

        humidity = registers[1] / 10.0

        print(f"Temperature : {temperature:.1f} °C")
        print(f"Humidity    : {humidity:.1f} %")
    else:
        print("Modbus error:", result)

except Exception as e:
    print(f"Exception: {e}")

finally:
    client.close()