import logging
from pymodbus.client import ModbusSerialClient

logging.disable(logging.CRITICAL)

PORT = "/dev/tty.usbserial-A5069RR4"
OLD_ID = 1
NEW_ID = 2

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
    print(f"Changing address {OLD_ID} → {NEW_ID}")

    # Write address AND baudrate together to avoid offset side effect
    # 0x0101 = Slave address
    # 0x0102 = Baudrate (9600 = 0x2580)
    result = client.write_registers(
        address=0x0101,
        values=[NEW_ID, 0x2580],  # 0x2580 = 9600
        device_id=OLD_ID
    )

    if hasattr(result, "isError") and result.isError():
        print("Write error:", result)
    else:
        print("Address successfully changed!")
        print("Power cycle the sensor (OFF → ON) to apply the new address.")

except Exception as e:
    print(f"Exception: {e}")

finally:
    client.close()