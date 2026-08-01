# HubAudio Architecture Report

## adr/ADR-001-ADAU1467-Audio-Domain-Master.md

- Line 1: `ADAU1467` → `Audio Processor`
- Line 12: `ESP32-S3` → `System Controller`
- Line 13: `Si4684` → `Radio Receiver`
- Line 25: `ADAU1467` → `Audio Processor`
- Line 29: `ADAU1467` → `Audio Processor`
- Line 31: `ADAU1467` → `Audio Processor`
- Line 40: `ADAU1467` → `Audio Processor`
- Line 42: `ESP32-S3` → `System Controller`
- Line 43: `ESP32-S3` → `System Controller`
- Line 74: `ADAU1467` → `Audio Processor`

## adr/ADR-002-SPI-Control-Architecture.md

- Line 14: `ESP32-S3` → `System Controller`
- Line 15: `ADAU1467` → `Audio Processor`
- Line 16: `Si4684` → `Radio Receiver`
- Line 28: `ESP32-S3` → `System Controller`
- Line 30: `ADAU1467` → `Audio Processor`
- Line 30: `Si4684` → `Radio Receiver`
- Line 40: `ESP32-S3` → `System Controller`
- Line 47: `ADAU1467` → `Audio Processor`
- Line 47: `Si4684` → `Radio Receiver`
- Line 51: `ADAU1467` → `Audio Processor`
- Line 53: `ADAU1467` → `Audio Processor`
- Line 56: `ADAU1467` → `Audio Processor`
- Line 62: `25AA1024` → `Audio EEPROM`
- Line 66: `ADAU1467` → `Audio Processor`
- Line 66: `ESP32-S3` → `System Controller`
- Line 70: `Si4684` → `Radio Receiver`
- Line 72: `Si4684` → `Radio Receiver`
- Line 75: `ESP32-S3` → `System Controller`
- Line 81: `Si4684` → `Radio Receiver`
- Line 91: `ESP32-S3` → `System Controller`
- Line 92: `Si4684` → `Radio Receiver`
- Line 111: `ESP32-S3` → `System Controller`

## adr/ADR-003-I2S-Audio-Routing-Architecture.md

- Line 13: `ESP32-S3` → `System Controller`
- Line 14: `Si4684` → `Radio Receiver`
- Line 28: `ADAU1467` → `Audio Processor`
- Line 38: `ADAU1467` → `Audio Processor`
- Line 44: `ADAU1467` → `Audio Processor`
- Line 46: `ESP32-S3` → `System Controller`
- Line 47: `Si4684` → `Radio Receiver`
- Line 52: `ESP32-S3` → `System Controller`
- Line 53: `Si4684` → `Radio Receiver`
- Line 54: `ADAU1467` → `Audio Processor`
- Line 60: `ADAU1467` → `Audio Processor`
- Line 67: `ADAU1467` → `Audio Processor`
- Line 76: `ADAU1467` → `Audio Processor`
- Line 108: `ADAU1467` → `Audio Processor`

## adr/ADR-004-Power-Domain-Architecture.md

- Line 10: `ESP32-S3` → `System Controller`

## architecture/HubAudio-Clock-Architecture.md

- Line 12: `ADAU1467` → `Audio Processor`
- Line 21: `ADAU1467` → `Audio Processor`
- Line 30: `ADAU1467` → `Audio Processor`
- Line 32: `ADAU1467` → `Audio Processor`
- Line 46: `ADAU1467` → `Audio Processor`
- Line 54: `ADAU1467` → `Audio Processor`
- Line 94: `ADAU1467` → `Audio Processor`
- Line 96: `PCS2P2309NZ` → `Clock Buffer`
- Line 110: `ADAU1467` → `Audio Processor`
- Line 120: `PCS2P2309NZ` → `Clock Buffer`
- Line 128: `Si4684` → `Radio Receiver`
- Line 138: `ADAU1467` → `Audio Processor`
- Line 150: `Si4684` → `Radio Receiver`
- Line 170: `ESP32-S3` → `System Controller`
- Line 179: `ADAU1467` → `Audio Processor`
- Line 179: `Si4684` → `Radio Receiver`
- Line 195: `ADAU1467` → `Audio Processor`
- Line 201: `ADAU1467` → `Audio Processor`
- Line 269: `ADAU1467` → `Audio Processor`
- Line 271: `PCS2P2309NZ` → `Clock Buffer`

## architecture/HubAudio-I2S-Architecture.md

- Line 13: `ADAU1467` → `Audio Processor`
- Line 21: `ADAU1467` → `Audio Processor`
- Line 29: `ESP32-S3` → `System Controller`
- Line 38: `ESP32-S3` → `System Controller`
- Line 39: `Si4684` → `Radio Receiver`
- Line 47: `ADAU1467` → `Audio Processor`
- Line 61: `ADAU1467` → `Audio Processor`
- Line 73: `ADAU1467` → `Audio Processor`
- Line 85: `Si4684` → `Radio Receiver`
- Line 91: `ADAU1467` → `Audio Processor`
- Line 97: `ESP32-S3` → `System Controller`
- Line 98: `Si4684` → `Radio Receiver`
- Line 103: `ESP32-S3` → `System Controller`
- Line 105: `ESP32-S3` → `System Controller`
- Line 110: `ESP32-S3` → `System Controller`
- Line 117: `ADAU1467` → `Audio Processor`
- Line 120: `ESP32-S3` → `System Controller`
- Line 122: `ADAU1467` → `Audio Processor`
- Line 127: `Si4684` → `Radio Receiver`
- Line 129: `Si4684` → `Radio Receiver`
- Line 132: `Si4684` → `Radio Receiver`
- Line 139: `ADAU1467` → `Audio Processor`
- Line 142: `Si4684` → `Radio Receiver`
- Line 169: `ADAU1467` → `Audio Processor`
- Line 193: `ADAU1467` → `Audio Processor`
- Line 203: `ADAU1467` → `Audio Processor`
- Line 216: `ADAU1467` → `Audio Processor`
- Line 235: `ADAU1467` → `Audio Processor`
- Line 254: `ADAU1467` → `Audio Processor`
- Line 272: `ADAU1467` → `Audio Processor`
- Line 328: `ADAU1467` → `Audio Processor`

## architecture/HubAudio-SPI-Architecture.md

- Line 29: `ESP32-S3` → `System Controller`
- Line 40: `ADAU1467` → `Audio Processor`
- Line 40: `Si4684` → `Radio Receiver`
- Line 48: `ESP32-S3` → `System Controller`
- Line 50: `ESP32-S3` → `System Controller`
- Line 61: `ESP32-S3` → `System Controller`
- Line 63: `ESP32-S3` → `System Controller`
- Line 71: `ADAU1467` → `Audio Processor`
- Line 71: `Si4684` → `Radio Receiver`
- Line 81: `ADAU1467` → `Audio Processor`
- Line 83: `ADAU1467` → `Audio Processor`
- Line 85: `ESP32-S3` → `System Controller`
- Line 93: `ADAU1467` → `Audio Processor`
- Line 95: `ADAU1467` → `Audio Processor`
- Line 103: `25AA1024` → `Audio EEPROM`
- Line 108: `ESP32-S3` → `System Controller`
- Line 110: `ADAU1467` → `Audio Processor`
- Line 115: `Si4684` → `Radio Receiver`
- Line 117: `ESP32-S3` → `System Controller`
- Line 117: `Si4684` → `Radio Receiver`
- Line 119: `ESP32-S3` → `System Controller`
- Line 127: `ESP32-S3` → `System Controller`
- Line 133: `Si4684` → `Radio Receiver`
- Line 144: `Si4684` → `Radio Receiver`
- Line 155: `ESP32-S3` → `System Controller`
- Line 165: `ADAU1467` → `Audio Processor`
- Line 165: `Si4684` → `Radio Receiver`
- Line 189: `ESP32-S3` → `System Controller`
- Line 197: `ADAU1467` → `Audio Processor`
- Line 200: `25AA1024` → `Audio EEPROM`
- Line 204: `Si4684` → `Radio Receiver`
- Line 215: `ADAU1467` → `Audio Processor`
- Line 227: `ESP32-S3` → `System Controller`
- Line 252: `ADAU1467` → `Audio Processor`
- Line 287: `ESP32-S3` → `System Controller`
- Line 289: `ADAU1467` → `Audio Processor`
- Line 291: `Si4684` → `Radio Receiver`

## architecture/HubAudio-System-Architecture.md

- Line 24: `ESP32-S3` → `System Controller`
- Line 26: `ADAU1467` → `Audio Processor`
- Line 42: `ESP32-S3` → `System Controller`
- Line 58: `ADAU1467` → `Audio Processor`
- Line 58: `Si4684` → `Radio Receiver`
- Line 73: `Si4684` → `Radio Receiver`
- Line 77: `ADAU1467` → `Audio Processor`
- Line 115: `ESP32-S3` → `System Controller`
- Line 131: `ESP32-S3` → `System Controller`
- Line 150: `ADAU1467` → `Audio Processor`
- Line 152: `ADAU1467` → `Audio Processor`
- Line 165: `ESP32-S3` → `System Controller`
- Line 166: `Si4684` → `Radio Receiver`
- Line 194: `ADAU1467` → `Audio Processor`
- Line 205: `ADAU1467` → `Audio Processor`
- Line 221: `Si4684` → `Radio Receiver`
- Line 229: `ESP32-S3` → `System Controller`
- Line 252: `ADAU1467` → `Audio Processor`
- Line 278: `Si4684` → `Radio Receiver`
- Line 321: `ADAU1467` → `Audio Processor`
- Line 328: `ADAU1467` → `Audio Processor`
- Line 362: `ADAU1467` → `Audio Processor`
- Line 369: `ADAU1467` → `Audio Processor`
- Line 392: `ESP32-S3` → `System Controller`
- Line 394: `ADAU1467` → `Audio Processor`
- Line 451: `ESP32-S3` → `System Controller`
- Line 457: `ADAU1467` → `Audio Processor`
- Line 463: `ADAU1467` → `Audio Processor`

## architecture/Power_Architecture.md

- Line 29: `ESP32-S3` → `System Controller`

## architecture/Power_Domains.md

- Line 22: `ADAU1467` → `Audio Processor`
- Line 34: `Si4684` → `Radio Receiver`

---

Files checked: 16

Issues found: 166
