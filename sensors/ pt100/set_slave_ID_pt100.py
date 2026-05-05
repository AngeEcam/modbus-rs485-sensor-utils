import logging
from pymodbus.client import ModbusSerialClient

logging.disable(logging.CRITICAL)

PORT = "/dev/tty.usbserial-A5069RR4"
OLD_ID = 3
NEW_ID = 4

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
    # 0x00FD = Slave address
    # 0x00FE = Baudrate (3 = 9600)
    result = client.write_registers(
        address=0x00FD,
        values=[NEW_ID, 3],
        device_id=OLD_ID
    )

    if hasattr(result, "isError") and result.isError():
        print("Write error:", result)
    else:
        print("Address successfully changed!")
        print("Power cycle the module (OFF → ON) to apply the new address.")

except Exception as e:
    print(f"Exception: {e}")

finally:
    client.close()