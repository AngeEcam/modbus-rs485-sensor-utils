from pymodbus.client import ModbusSerialClient

PORT = "/dev/tty.usbserial-A5069RR4"
OLD_ID = 7
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

    result = client.write_register(
        address=0x0101,
        value=NEW_ID,
        device_id=OLD_ID
    )

    if hasattr(result, "isError") and result.isError():
        print("Write error:", result)
    else:
        print("Address successfully changed!")
        print("Power cycle the sensor (OFF → ON) to apply the new address.")

finally:
    client.close()