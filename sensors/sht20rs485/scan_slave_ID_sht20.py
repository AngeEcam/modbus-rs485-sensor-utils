from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException

PORT = "/dev/tty.usbserial-A5069RR4"

client = ModbusSerialClient(
    port=PORT,
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=0.5,
    retries=0,
)

if not client.connect():
    print("Connexion impossible")
    exit()

try:
    print("Searching for sensor...")

    found = False

    for slave_id in range(1, 248):
        try:
            result = client.read_input_registers(
                address=0x0001,
                count=1,
                device_id=slave_id
            )

            if hasattr(result, "registers"):
                print(f"Sensor found at address: {slave_id}")
                found = True
                break

        except ModbusIOException:
            pass
        except Exception:
            pass

    if not found:
        print("No sensor found")

finally:
    client.close()