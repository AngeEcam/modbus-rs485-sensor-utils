from pymodbus.client import ModbusSerialClient

PORT = "/dev/tty.usbserial-A5069RR4"

client = ModbusSerialClient(
    port=PORT,
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=1,
)

if not client.connect():
    print("Connexion impossible")
    exit()

print("Scan des adresses 1 → 5\n")

devices = {}   # dictionnaire résultat

for SLAVE_ID in range(1, 6):

    print(f"--- Test adresse {SLAVE_ID} ---")

    detected = False

    # ===== PT100 =====
    try:
        result = client.read_holding_registers(
            address=0x0000,
            count=4,
            device_id=SLAVE_ID
        )

        if hasattr(result, "registers"):
            print("PT100 détecté")
            devices[SLAVE_ID] = "PT100" 
            detected = True

    except:
        pass

    # ===== STHP =====
    if not detected:
        try:
            result = client.read_input_registers(
                address=0x0000,
                count=4,
                device_id=SLAVE_ID
            )

            if hasattr(result, "registers"):
                print("STHP détecté")
                devices[SLAVE_ID] = "STHP"   # ajout
                detected = True

        except:
            pass

    if not detected:
        print("Aucun capteur")

    print()

client.close()

print("Scan terminé\n")

# Résumé final
print("Capteurs détectés :")
print(devices)