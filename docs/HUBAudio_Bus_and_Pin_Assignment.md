# HubAudio
# Bus Architecture and Preliminary Pin Assignment

**Document:** Hardware Interface Definition  
**Revision:** 0.1  
**Status:** Preliminary Design  
**Controller:** ESP32-S3


---

# 1. Purpose

This document defines the preliminary hardware interfaces between the ESP32-S3 system controller and all HubAudio modules.

The purpose is to establish:

- bus ownership
- GPIO allocation
- peripheral assignment
- boot-safe pins
- expansion possibilities


This document must be reviewed before PCB routing.


---

# 2. Design Rules


The following rules apply:


## Rule 1

The ESP32-S3 controls configuration only.


Audio data does not pass through the MCU.


---

## Rule 2

All audio sources connect directly to ADAU1467.



SOURCE

|

I2S

|

ADAU1467



---

## Rule 3

Every external module must be identifiable.


Identification:


24AA025E48T-I/OT



---

# 3. ESP32-S3 Peripheral Allocation


## 3.1 Overview


| Function | Interface |
|-|-|
| Radio control | SPI |
| DSP control | I2C |
| Module EEPROM | I2C |
| Bluetooth control | UART |
| Debug | USB/JTAG |
| Expansion | Reserved GPIO |


---

# 4. Proposed GPIO Map


## 4.1 I2C Bus


Shared bus:


| Signal | ESP32-S3 GPIO | Devices |
|-|-|-|
| SDA | GPIO8 | EEPROM, ADAU1467 |
| SCL | GPIO9 | EEPROM, ADAU1467 |


Notes:

- keep traces short
- external pull-ups required
- address conflicts must be checked


---

# 4.2 SPI Bus


Used for radio and memories.


| Signal | ESP32-S3 GPIO | Function |
|-|-|-|
| SCLK | GPIO12 | SPI Clock |
| MOSI | GPIO11 | SPI Data |
| MISO | GPIO13 | SPI Data |
| CS_RADIO | GPIO10 | Si4684 |
| CS_FLASH | GPIO14 | External memories |


---

# 4.3 UART Bus


Bluetooth modules:


## BT RX


| Signal | GPIO |
|-|-|
| TX ESP32 | GPIO17 |
| RX ESP32 | GPIO18 |


## BT1035 TX


Second UART:


| Signal | GPIO |
|-|-|
| TX ESP32 | GPIO43 |
| RX ESP32 | GPIO44 |


Notes:

ESP32-S3 provides multiple UART peripherals.


---

# 4.4 Module Control GPIO


| Signal | GPIO | Function |
|-|-|-|
| RADIO_RESET | GPIO4 | Si4684 reset |
| DSP_RESET | GPIO5 | ADAU1467 reset |
| BT_RX_RESET | GPIO6 | BT receiver reset |
| BT_TX_RESET | GPIO7 | BT1035 reset |


---

# 5. Si4684 Interface


## Control


SPI:



ESP32-S3

SCLK
|
Si4684 CLK

MOSI
|
Si4684 SDIO

CS
|
Si4684 CS



Control:



GPIO4

|

RESET



Interrupt:



Si4684 IRQ

|

ESP32 GPIO



---

# 6. ADAU1467 Interface


## Control Interface


Preferred:


I2C



ESP32-S3

SDA

SCL

|

ADAU1467



Used for:


- volume
- routing
- DSP parameters


---

# 7. Bluetooth TX Interface


Device:

FSC-BT1035


## Control


UART:



ESP32-S3

TX

|

BT1035 RX

ESP32-S3

RX

|

BT1035 TX



---

## Audio


I2S:



ADAU1467

  |

  |

BT1035

BCLK

LRCLK

DATA



The clock direction must be verified.


Preferred:


ADAU1467 master.


---

# 8. Bluetooth RX Interface


Device:

FSC-BT1026 or equivalent.


## Control


UART:



ESP32-S3

|

BT RX Module



---

## Audio



BT RX

|

I2S OUT

|

ADAU1467 INPUT



---

# 9. I2S Architecture


## Important Design Decision


Multiple I2S sources are not connected together.


Wrong:



Si4684
|
|
BT RX
|
+------ I2S ------ ADAU1467



Correct:



Si4684

I2S Port 0

    |

    |

ADAU1467

BT RX

I2S Port 1

    |

    |

ADAU1467



The ADAU1467 internal serial ports perform routing.


---

# 10. Proposed ADAU1467 Serial Port Allocation


| DSP Port | Device | Direction |
|-|-|-|
| Serial Input 0 | Si4684 | RX |
| Serial Input 1 | BT RX | RX |
| Serial Output 0 | DAC | TX |
| Serial Output 1 | BT1035 | TX |


---

# 11. EEPROM Bus


All modules include:



24AA025E48T



Example:


| Module | Address |
|-|-|
| Main Board | 0x50 |
| Radio | 0x51 |
| Bluetooth | 0x52 |
| DSP | 0x53 |


Address selection must be verified.


---

# 12. Reserved Expansion Interface


Future modules:


Possible:

- external DAC
- amplifier module
- display
- sensors
- remote control


Reserved:


SPI

I2C

UART

I2S

GPIO

Power



---

# 13. Boot Safety Review


ESP32-S3 boot pins must be checked.


Before PCB release:


Verify:

- GPIO assignment
- strapping pins
- pull-up/pull-down resistors


No external device must force an incorrect boot state.


---

# 14. Recommended Connector Between Modules


For removable modules:


Example:



MODULE HEADER

1 3.3V
2 GND
3 SDA
4 SCL
5 UART TX
6 UART RX
7 RESET
8 IRQ
9 I2S BCLK
10 I2S LRCLK
11 I2S DATA
12 RESERVED



---

# 15. Final Review Before Schematic


Before drawing schematic:


Check:


[ ] ESP32-S3 GPIO availability

[ ] Boot strap conflicts

[ ] I2S clock ownership

[ ] Module power consumption

[ ] RF placement

[ ] EEPROM addressing

[ ] Firmware update paths


---

# END