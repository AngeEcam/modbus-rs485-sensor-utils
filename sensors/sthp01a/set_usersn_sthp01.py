from pymodbus.client import ModbusSerialClient

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
    print("Connexion impossible")
    exit()

try:
    print("Ecriture USERSN...")

    values = [0x0101, 0x0000, 0x0000, 0x0000]

    result = client.write_registers(
        address=0x0220,
        values=values,
        device_id=SLAVE_ID
    )

    if hasattr(result, "isError") and result.isError():
        print("Erreur écriture :", result)
    else:
        print("USERSN écrit avec succès !")

finally:
    client.close()