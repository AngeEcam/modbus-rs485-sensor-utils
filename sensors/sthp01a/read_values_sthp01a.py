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
    print("Connexion impossible au port série")
    exit()

try:
    result = client.read_input_registers(address=0x0000, count=4, device_id=SLAVE_ID)

    if hasattr(result, 'isError') and result.isError():
        print("Erreur Modbus :", result)
    elif hasattr(result, 'registers'):
        registers = result.registers
        print("Registres bruts :", registers)

        temperature = registers[0] / 100
        humidity    = registers[1] / 100
        pressure    = registers[3] / 10

        print(f"Température : {temperature:.2f} °C")
        print(f"Humidité    : {humidity:.2f} %")
        print(f"Pression    : {pressure:.1f} hPa")
    else:
        print("Réponse inattendue :", result)

except Exception as e:
    print(f"Exception : {e}")

finally:
    client.close()