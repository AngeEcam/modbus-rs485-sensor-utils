import logging
from pymodbus.client import ModbusSerialClient

logging.disable(logging.CRITICAL)

PORT = "/dev/tty.usbserial-A5069RR4"
SLAVE_ID = 3

client = ModbusSerialClient(
    port=PORT,
    baudrate=2400,  # baudrate actuel du module
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=2,
)

if not client.connect():
    print("Connection failed")
    exit()

try:
    # Remettre baudrate à 9600 (valeur 3)
    result = client.write_register(
        address=0x00FE,
        value=3,
        device_id=SLAVE_ID
    )
    print("Baudrate reset to 9600:", result)
    print("Power cycle the module (OFF → ON) to apply.")

except Exception as e:
    print(f"Exception: {e}")

finally:
    client.close()