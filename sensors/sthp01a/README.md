# RS485 Modbus Sensor Toolkit

Python tools to interact with a temperature/humidity/pressure sensor via RS485 Modbus RTU.

---

## Hardware Requirements

- RS485 sensor (STHP01A)
- USB → RS485 adapter (USB hub if USB-C only port)
- A/B connection cable to the sensor

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
ls /dev/tty.usbserial-*    # macOS
ls /dev/ttyUSB*            # Linux
```

Windows: open **Device Manager → Ports (COM & LPT)**, the port appears as `COM3`, `COM4`, etc.

Update the `PORT` variable in each script accordingly:

```python
PORT = "/dev/tty.usbserial-A5069RR4"   # macOS
PORT = "/dev/ttyUSB0"                  # Linux
PORT = "COM3"                          # Windows
```

---

## Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. Scan the bus      →  scan_bus.py                │
│     Finds the Slave ID address of the sensor        │
│                                                     │
│  2. Read sensor data  →  read_sensor.py             │
│     Uses the Slave ID found to read T/H/P           │
│                                                     │
│  3. (Optional) Change Slave ID  →  change_id.py     │
│     If multiple sensors share the same bus          │
└─────────────────────────────────────────────────────┘
```

---

## Step 1 — Scan the bus (`scan_bus.py`)

If you don't know the Modbus address of your sensor, this script queries all addresses from 1 to 247.

```bash
python scan_bus.py
```

**Expected output:**
```
Searching for sensor...
Sensor found at address: 1
```

> The scan may take a few seconds (0.5s timeout per address).  
> Note the Slave ID found — it will be used in the next step.

---

## Step 2 — Read sensor data (`read_sensor.py`)

Update `SLAVE_ID` in the script with the value found during the scan, then:

```bash
python read_sensor.py
```

**Expected output:**
```
Raw registers: [2265, 3924, 809, 10194]
Temperature : 22.65 °C
Humidity    : 39.24 %
Pressure    : 1019.4 hPa
```

### Register mapping

| Register | Index | Parameter   | Divisor | Unit |
|----------|-------|-------------|---------|------|
| 0x0000   | [0]   | Temperature | /100    | °C   |
| 0x0001   | [1]   | Humidity    | /100    | %RH  |
| 0x0002   | [2]   | (reserved)  | —       | —    |
| 0x0003   | [3]   | Pressure    | /10     | hPa  |

---

## Step 3 — Change Slave ID (`change_id.py`) *(optional)*

Useful if you have multiple sensors on the same RS485 bus and need to differentiate them. Each sensor must have a unique address (1–247).

Update `OLD_ID` (current address) and `NEW_ID` (desired new address) in the script, then:

```bash
python change_id.py
```

**Expected output:**
```
Changing address 2 → 1
Address successfully changed!
```

> After changing the address, power cycle the sensor (OFF → ON), then run `scan_bus.py` again to confirm the new address.

---

## RS485 Configuration

| Parameter | Value      |
|-----------|------------|
| Baudrate  | 9600       |
| Data bits | 8          |
| Parity    | None       |
| Stop bits | 1          |
| Protocol  | Modbus RTU |