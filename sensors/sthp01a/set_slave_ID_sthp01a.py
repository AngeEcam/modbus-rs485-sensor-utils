from pymodbus.client import ModbusSerialClient

PORT = "/dev/tty.usbserial-A5069RR4"
OLD_ID = 2
NEW_ID = 1

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
    print(f"Changement adresse {OLD_ID} → {NEW_ID}")

    result = client.write_register(
        address=0x0200,
        value=NEW_ID,
        device_id=OLD_ID
    )

    if hasattr(result, "isError") and result.isError():
        print("Erreur écriture :", result)
    else:
        print("Adresse modifiée avec succès !")

finally:
    client.close()