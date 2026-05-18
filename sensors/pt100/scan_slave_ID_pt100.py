from pymodbus.client import ModbusSerialClient


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
    print("Searching for PT100 sensor...")
    found = False

    for slave_id in range(1, 248):
        print(f"Trying address {slave_id}/247...", end="\r")
        try:
            result = client.read_holding_registers(
                address=0x0000,
                count=1,
                device_id=slave_id  # device_id= pour pymodbus 3.13
            )

            if hasattr(result, "registers"):
                raw_temp = result.registers[0]

                # Gestion températures négatives (complément à 2)
                if raw_temp > 32767:
                    temp = (raw_temp - 65536) / 10.0
                else:
                    temp = raw_temp / 10.0

                print(f"\nSensor found at address: {slave_id} — Temperature: {temp:.1f} °C")
                found = True
                break

        except Exception:
            pass

    if not found:
        print("\nNo sensor found")

finally:
    client.close()