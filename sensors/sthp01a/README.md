# RS485 Modbus Sensor Toolkit

Outils Python pour interagir avec un capteur de température/humidité/pression via RS485 Modbus RTU sur macOS.

---

## Prérequis matériel

- Capteur RS485 (STHP01A)
- Adaptateur USB → RS485 (Hub USB si port USB C)
- Câble de connexion A/B vers le capteur

---

## Installation

### 1. Installer les dépendances

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Identifier le port série

Brancher l'adaptateur USB→RS485, puis :

```bash
ls /dev/tty.usbserial-*    # macOS
ls /dev/ttyUSB*            # Linux
```
Windows : ouvrir le **Gestionnaire de périphériques → Ports (COM et LPT)**, le port apparaît comme `COM3`, `COM4`, etc.

Mettre à jour la variable `PORT` dans chaque script :

```python
PORT = "/dev/tty.usbserial-A5069RR4"   # macOS
PORT = "/dev/ttyUSB0"                  # Linux
PORT = "COM3"                          # Windows
```
---

## Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. Scanner le bus  →  scan_bus.py                  │
│     Trouve l'adresse Slave ID du capteur            │
│                                                     │
│  2. Lire les données  →  read_sensor.py             │
│     Utilise le Slave ID trouvé pour lire T/H/P      │
│                                                     │
│  3. (Optionnel) Changer le Slave ID  →  change_id.py│
│     Si plusieurs capteurs sur le même bus           │
└─────────────────────────────────────────────────────┘
```

---

## Étape 1 — Scanner le bus (`scan_bus.py`)

Si vous ne connaissez pas l'adresse Modbus de votre capteur, ce script interroge toutes les adresses de 1 à 247.

```bash
python scan_bus.py
```

**Sortie attendue :**
```
Recherche du capteur...
Capteur trouvé à l'adresse : 1
```

> Le scan peut prendre quelques secondes (timeout de 0.5s par adresse).  
> Notez le Slave ID trouvé, il sera utilisé à l'étape suivante.

---

## Étape 2 — Lire les données (`read_sensor.py`)

Mettre à jour `SLAVE_ID` dans le script avec la valeur trouvée au scan, puis :

```bash
python read_sensor.py
```

**Sortie attendue :**
```
Registres bruts : [2265, 3924, 809, 10194]
Température : 22.65 °C
Humidité    : 39.24 %
Pression    : 1019.4 hPa
```

### Correspondance des registres

| Registre | Index | Paramètre   | Diviseur | Unité |
|----------|-------|-------------|----------|-------|
| 0x0000   | [0]   | Température | /100     | °C    |
| 0x0001   | [1]   | Humidité    | /100     | %RH   |
| 0x0002   | [2]   | (réservé)   | —        | —     |
| 0x0003   | [3]   | Pression    | /10      | hPa   |

---

## Étape 3 — Changer le Slave ID (`change_id.py`) *(optionnel)*

Utile si vous avez plusieurs capteurs sur le même bus RS485 et devez les différencier. Chaque capteur doit avoir une adresse unique (1–247).

Mettre à jour `OLD_ID` (adresse actuelle) et `NEW_ID` (nouvelle adresse souhaitée) dans le script, puis :

```bash
python change_id.py
```

**Sortie attendue :**
```
Changement adresse 2 → 1
Adresse modifiée avec succès !
```

> Après le changement d’adresse, redémarrer électriquement le capteur (OFF → ON), puis relancer scan_bus.py pour confirmer la nouvelle adresse.
---

## Configuration RS485

| Paramètre | Valeur |
|-----------|--------|
| Baudrate  | 9600   |
| Data bits | 8      |
| Parité    | None   |
| Stop bits | 1      |
| Protocole | Modbus RTU |

---