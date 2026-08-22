# HubAudio — I²C Bus Map

**Progetto:** HubAudio  
**Revisione:** definitiva  
**Data:** 2026-08-23

## Dispositivi I²C

| IC | Componente | Configurazione indirizzo | Indirizzo I²C (7-bit) |
|---|---|---|---:|
| U1 | BQ25896RTWR | Indirizzo fisso | `0x6B` |
| U2 | BQ27441DRZR-G1B | Indirizzo fisso | `0x55` |
| U4 | INA228AQDGSRQ1 | A0 = 0, A1 = 0 | `0x40` |
| U8 | INA228AQDGSRQ1 | A0 = 0, A1 = 1 | `0x41` |
| U17 | 24AA025E64 | A2 = 0, A1 = 0, A0 = 0 | `0x50` |
| U20 | TPS22994RUKT | ADDR3 = 0, ADDR2 = 0, ADDR1 = 0 | `0x20` |
| U23 | TPS22994RUKT | ADDR3 = 0, ADDR2 = 0, ADDR1 = 1 | `0x21` |
| U31 | TMP117NAIDRVR | ADDR = GND | `0x48` |
| U32 | TMP117NAIDRVR | ADDR = VCC | `0x49` |
| U33 | TMP117NAIDRVR | ADDR = SDA | `0x4A` |
| U37 | TMP117NAIDRVR | ADDR = SCL | `0x4B` |

## Address Map

| Indirizzo | IC | Dispositivo |
|---:|---|---|
| `0x20` | U20 | TPS22994 |
| `0x21` | U23 | TPS22994 |
| `0x40` | U4 | INA228 — Analog |
| `0x41` | U8 | INA228 — Digital |
| `0x48` | U31 | TMP117 — Power |
| `0x49` | U32 | TMP117 — ESP32 |
| `0x4A` | U33 | TMP117 — DSP |
| `0x4B` | U37 | TMP117 — Codec |
| `0x50` | U17 | 24AA025E64 |
| `0x55` | U2 | BQ27441 |
| `0x6B` | U1 | BQ25896 |

## TMP117

I quattro TMP117 utilizzano tutte le quattro configurazioni disponibili del
pin `ADDR`:

- **U31 — Power:** `ADDR → GND` → `0x48`
- **U32 — ESP32:** `ADDR → VCC` → `0x49`
- **U33 — DSP:** `ADDR → SDA` → `0x4A`
- **U37 — Codec:** `ADDR → SCL` → `0x4B`

Ogni TMP117 dispone di un condensatore di bypass locale da **100 nF**.

## INA228

- **U4 — Analog:** A0 = 0, A1 = 0 → `0x40`
- **U8 — Digital:** A0 = 0, A1 = 1 → `0x41`

## TPS22994

- **U20:** ADDR3 = 0, ADDR2 = 0, ADDR1 = 0 → `0x20`
- **U23:** ADDR3 = 0, ADDR2 = 0, ADDR1 = 1 → `0x21`

## EEPROM

**U17 — 24AA025E64**

```text
A2 = GND
A1 = GND
A0 = GND

→ 0x50

Indirizzi fissi

U1 — BQ25896: 0x6B

U2 — BQ27441: 0x55

Verifica collisioni

Non risultano collisioni tra gli indirizzi I²C assegnati.

Totale dispositivi I²C: 11

Indirizzi utilizzati: 11

0x20
0x21
0x40
0x41
0x48
0x49
0x4A
0x4B
0x50
0x55
0x6B
