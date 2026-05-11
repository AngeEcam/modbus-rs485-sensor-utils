import logging
from pymodbus.client import ModbusSerialClient

logging.disable(logging.CRITICAL)

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
    print("Connection failed")
    exit()

try:
    print("Searching for XY-MD04 sensor...")
    found = False

    for slave_id in range(0, 248):
        print(f"Trying address {slave_id}/247...", end="\r")
        try:
            result = client.read_input_registers(
                address=0x0001,
                count=1,
                device_id=slave_id
            )
            if hasattr(result, "registers"):
                raw = result.registers[0]
                temp = (raw - 65536) / 10.0 if raw > 32767 else raw / 10.0
                print(f"\nSensor found at address: {slave_id} — Temperature: {temp:.1f} °C")
                found = True
                break

        except Exception:
            pass

    if not found:
        print("\nNo sensor found")

finally:
    client.close()