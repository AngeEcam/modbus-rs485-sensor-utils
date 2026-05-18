# RS485 Modbus Sensor Toolkit — PT100 RTD (PTA8C04)

Python tools to interact with a 4-channel PT100 RTD temperature module via RS485 Modbus RTU.

---

## Hardware Requirements

- PT100 RTD module — 4 channels (PTA8C04, 24V or 12V)
- USB → RS485 adapter (USB hub if USB-C only port)
- A/B connection cable to the sensor
- PT100 probe(s) connected to channel(s) P1+/P1−, P2+/P2−, etc.

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
│  1. Scan the bus      →  scan_slave_ID_pt100.py     │
│     Finds the Slave ID address of the module        │
│                                                     │
│  2. Read sensor data  →  read_values_pt100.py       │
│     Uses the Slave ID found to read temperature(s)  │
│                                                     │
│  3. (Optional) Change Slave ID                      │
│                       →  set_slave_ID_pt100.py      │
│     If multiple modules share the same bus          │
└─────────────────────────────────────────────────────┘
```

---

## Step 1 — Scan the bus (`scan_slave_ID_pt100.py`)

```bash
python scan_slave_ID_pt100.py
```

**Expected output:**
```
Searching for PT100 sensor...
Sensor found at address: 1 — Temperature: 21.2 °C
```

> The scan may take a few seconds (0.5s timeout per address).  
> Note the Slave ID found — it will be used in the next step.

---

## Step 2 — Read sensor data (`read_values_pt100.py`)

Update `SLAVE_ID` in the script with the value found during the scan, then:

```bash
python read_values_pt100.py
```

**Expected output:**
```
Raw registers: [212, 64597, 64598, 64597]
Channel 1 — Temperature: 21.2 °C
Channel 2 — No sensor connected
Channel 3 — No sensor connected
Channel 4 — No sensor connected
```

### Register mapping (function code 0x03 — Read Holding Registers)

| Register | Channel | Type            | Divisor | Unit |
|----------|---------|-----------------|---------|------|
| 0x0000   | CH1     | Signed 16-bit   | /10     | °C   |
| 0x0001   | CH2     | Signed 16-bit   | /10     | °C   |
| 0x0002   | CH3     | Signed 16-bit   | /10     | °C   |
| 0x0003   | CH4     | Signed 16-bit   | /10     | °C   |
| 0x0004   | CH1     | Unsigned 16-bit | —       | Ω (raw resistance) |
| 0x0005   | CH2     | Unsigned 16-bit | —       | Ω (raw resistance) |
| 0x0006   | CH3     | Unsigned 16-bit | —       | Ω (raw resistance) |
| 0x0007   | CH4     | Unsigned 16-bit | —       | Ω (raw resistance) |

> Unconnected channels return a value around **−43.5 °C** (module error value).  
> Negative temperatures use two's complement: if raw > 32767 → temp = (raw − 65536) / 10

---

## Step 3 — Change Slave ID (`set_slave_ID_pt100.py`) *(optional)*

Update `OLD_ID` and `NEW_ID` in the script, then:

```bash
python set_slave_ID_pt100.py
```

**Expected output:**
```
Changing address 1 → 2
Address successfully changed!
Power cycle the module (OFF → ON) to apply the new address.
```

> After changing the address, power cycle the module (OFF → ON), then run `scan_slave_ID_pt100.py` again to confirm the new address.

### Important — pymodbus offset side effect

On this module, registers `0x00FD` (Slave address) and `0x00FE` (Baudrate) are adjacent. Due to a pymodbus offset behaviour, writing to `0x00FD` alone can accidentally overwrite `0x00FE` and change the baudrate, making the module unreachable.

**Always use `write_registers` to write both registers simultaneously:**

```python
client.write_registers(
    address=0x00FD,
    values=[NEW_ID, 3],  # 0x00FD = new address, 0x00FE = baudrate (3 = 9600)
    device_id=OLD_ID
)
```

This is already handled in `set_slave_ID_pt100.py`.

### Configuration registers (function code 0x10 — Write Multiple Registers)

| Register | Parameter     | Default | Range / Settings                             |
|----------|---------------|---------|----------------------------------------------|
| 0x00FD   | Slave address | 1       | 1 to 247                                     |
| 0x00FE   | Baud rate     | 3       | 0=1200 / 1=2400 / 2=4800 / 3=9600 / 4=19200 |

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
| 0x03 | Read Holding Registers (data)  |
| 0x06 | Write Single Register          |
| 0x10 | Write Multiple Registers       |