# RS485 Modbus Sensor Toolkit — XY-MD04 (SHT40)

Python tools to interact with a temperature/humidity sensor via RS485 Modbus RTU.

---

## Hardware Requirements

- XY-MD04 temperature/humidity sensor (built-in SHT40, metal waterproof probe)
- USB → RS485 adapter (USB hub if USB-C only port)
- A/B connection cable to the sensor

### Wiring

| Wire   | Connection  |
|--------|-------------|
| Red    | VCC (5–28V) |
| Black  | GND         |
| Yellow | RS485-A     |
| White  | RS485-B     |

---

## Installation

### 1. Install dependencies

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

pip install pymodbus pyserial
```

### 2. Identify the serial port

Plug in the USB→RS485 adapter, then:

```bash
ls /dev/tty.usbserial-*   # macOS
ls /dev/ttyUSB*            # Linux
```

Windows: open **Device Manager → Ports (COM & LPT)**, the port appears as `COM3`, `COM4`, etc.

Update the `PORT` variable in each script accordingly:

```python
PORT = "/dev/tty.usbserial-A5069RR4"  # macOS
PORT = "/dev/ttyUSB0"                  # Linux
PORT = "COM3"                          # Windows
```

---

## Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. Scan the bus      →  scan_slave_ID_xymd04.py    │
│     Finds the Slave ID address of the sensor        │
│                                                     │
│  2. Read sensor data  →  read_values_xymd04.py      │
│     Uses the Slave ID found to read T/H             │
│                                                     │
│  3. (Optional) Change Slave ID                      │
│                       →  set_slave_ID_xymd04.py     │
│     If multiple sensors share the same bus          │
└─────────────────────────────────────────────────────┘
```

---

## Step 1 — Scan the bus (`scan_slave_ID_xymd04.py`)

```bash
python scan_slave_ID_xymd04.py
```

**Expected output:**
```
Searching for XY-MD04 sensor...
Sensor found at address: 1 — Temperature: 22.5 °C
```

> The scan may take a few seconds (0.5s timeout per address).  
> Note the Slave ID found — it will be used in the next step.

---

## Step 2 — Read sensor data (`read_values_xymd04.py`)

Update `SLAVE_ID` in the script with the value found during the scan, then:

```bash
python read_values_xymd04.py
```

**Expected output:**
```
Raw registers: [225, 677]
Temperature : 22.5 °C
Humidity    : 67.7 %
```

### Register mapping (function code 0x04 — Read Input Registers)

| Register | Parameter   | Divisor | Unit |
|----------|-------------|---------|------|
| 0x0001   | Temperature | /10     | °C   |
| 0x0002   | Humidity    | /10     | %RH  |

> Negative temperatures use two's complement: if raw > 32767 → temp = (raw − 65536) / 10  
> Both registers can be read in a single request: start at **0x0001**, count **2**.

---

## Step 3 — Change Slave ID (`set_slave_ID_xymd04.py`) *(optional)*

Update `OLD_ID` and `NEW_ID` in the script, then:

```bash
python set_slave_ID_xymd04.py
```

**Expected output:**
```
Changing address 1 → 2
Address successfully changed!
Power cycle the sensor (OFF → ON) to apply the new address.
```

> After changing the address, power cycle the sensor (OFF → ON), then run `scan_slave_ID_xymd04.py` again to confirm the new address.

### ⚠️ Important — write both registers simultaneously

Registers `0x0101` (Slave address) and `0x0102` (Baudrate) are adjacent. Always use `write_registers` to write both at once and avoid accidental baudrate changes:

```python
client.write_registers(
    address=0x0101,
    values=[NEW_ID, 0x2580],  # 0x0101 = new address, 0x0102 = baudrate (0x2580 = 9600)
    device_id=OLD_ID
)
```

> Note: unlike some other modules, the XY-MD04 baudrate register uses the **actual decimal value** (e.g. 9600 = `0x2580`), not an index.

### Configuration registers (function code 0x06 / 0x10)

| Register | Parameter             | Default | Range / Settings                                    |
|----------|-----------------------|---------|-----------------------------------------------------|
| 0x0101   | Slave address         | 1       | 1 to 247                                            |
| 0x0102   | Baud rate             | 9600    | 9600 / 14400 / 19200 / 38400 / 56000 / 57600 / 115200 |
| 0x0103   | Temperature offset    | 0       | −10.0 to +10.0 (/10)                               |
| 0x0104   | Humidity offset       | 0       | −10.0 to +10.0 (/10)                               |

---

## Sensor Specifications

| Parameter             | Value                  |
|-----------------------|------------------------|
| Built-in sensor       | SHT40                  |
| Temperature range     | −40°C to 120°C         |
| Temperature accuracy  | ±0.3°C                 |
| Temperature resolution| 0.1°C                  |
| Humidity range        | 0% to 100% RH          |
| Humidity accuracy     | ±3% RH                 |
| Humidity resolution   | 0.1% RH                |
| Supply voltage        | 5V – 28V DC            |
| Probe material        | Metal waterproof        |

---

## RS485 Configuration

| Parameter | Value      |
|-----------|------------|
| Baudrate  | 9600       |
| Data bits | 8          |
| Parity    | None       |
| Stop bits | 1          |
| Protocol  | Modbus RTU |

---

## Function codes summary

| Code | Operation                      |
|------|--------------------------------|
| 0x03 | Read Holding Registers (config)|
| 0x04 | Read Input Registers (data)    |
| 0x06 | Write Single Register          |
| 0x10 | Write Multiple Registers       |