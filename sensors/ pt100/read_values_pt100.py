from pymodbus.client import ModbusSerialClient

PORT = "/dev/tty.usbserial-A5069RR4"
SLAVE_ID = 0

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
    # 4 canaux PT100 — registres 0x0000 à 0x0003
    result = client.read_holding_registers(
        address=0x0000,
        count=4,
        device_id=SLAVE_ID
    )

    if hasattr(result, "registers"):
        registers = result.registers
        print("Raw registers:", registers)

        for i, raw in enumerate(registers):
            # Complément à 2 pour températures négatives
            if raw > 32767:
                temp = (raw - 65536) / 10.0
            else:
                temp = raw / 10.0
            print(f"Channel {i+1} — Temperature: {temp:.1f} °C")
    else:
        print("Modbus error:", result)

except Exception as e:
    print(f"Exception: {e}")

finally:
    client.close()