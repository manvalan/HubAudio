# HubAudio — SPI Bus Map

**Progetto:** HubAudio  
**Revisione:** definitiva  
**Data:** 2026-08-23

## SPI Bus Architecture

HubAudio utilizza un bus SPI principale con ESP32-S31-WROOM-3 come master.

Il bus principale condivide:

- `SPI_SCLK`
- `SPI_MOSI`
- `SPI_MISO`

Ogni slave dispone di una propria linea Chip Select (`CS`).

---

## SPI Main Bus

| IC | Dispositivo | Ruolo | CS |
|---|---|---|---|
| U5 | XTAC5212IRGER | Audio Codec | `SPI_CODEC_CS` |
| U34 | MCP23S17-E/ML | Device Manager A | `SPI_DEV_MAN_A_CS` |
| U36 | MCP23S17-E/ML | Device Manager B | `SPI_DEV_MAN_B_CS` |
| U18 | ADAU1467WBCPZ300R | Audio DSP | `SPI_ADAU1467_CS` |
| U12 | Si4684-A10-GM | Radio | `SPI_SI4684_CS` |
| U10 | W25Q128JVS | Flash | `SPI_W25Q128_CS` |
| U30 | SC16IS740IPW,128 | UART Bridge | `SPI_UART_CS` |

### Shared SPI Signals

| Segnale | Funzione |
|---|---|
| `SPI_SCLK` | SPI Clock |
| `SPI_MOSI` | Master Out / Slave In |
| `SPI_MISO` | Master In / Slave Out |

Il master SPI è l'**ESP32-S31-WROOM-3 (U11)**.

Le linee `SPI_SCLK`, `SPI_MOSI` e `SPI_MISO` sono condivise tra gli slave
del bus principale.

Le linee `CS` sono indipendenti e vengono utilizzate per selezionare
un singolo slave alla volta.

---

## Chip Select

| CS | Slave |
|---|---|
| `SPI_CODEC_CS` | U5 — TAC5212 |
| `SPI_DEV_MAN_A_CS` | U34 — MCP23S17 |
| `SPI_DEV_MAN_B_CS` | U36 — MCP23S17 |
| `SPI_ADAU1467_CS` | U18 — ADAU1467 |
| `SPI_SI4684_CS` | U12 — Si4684 |
| `SPI_W25Q128_CS` | U10 — W25Q128JVS |
| `SPI_UART_CS` | U30 — SC16IS740 |

---

# Private SPI Buses

Alcuni dispositivi dispongono di una memoria SPI dedicata e non fanno
parte del bus SPI principale dell'ESP32.

## ADAU1467 — Private SPI

| Master | Slave | Dispositivo |
|---|---|---|
| U18 | U24 | 25AA1024-I/SM |

**Master:** ADAU1467  
**Slave:** 25AA1024 SPI EEPROM

La memoria U24 utilizza il bus SPI privato dell'ADAU1467.

U24 **non** è uno slave del bus SPI principale dell'ESP32 e pertanto non
possiede una linea `CS` appartenente al namespace `SPI_*` del bus principale.

---

## Si4684 — Private SPI

| Master | Slave | Dispositivo |
|---|---|---|
| U12 | U27 | W25Q16JW |

**Master:** Si4684  
**Slave:** W25Q16JW SPI Flash

La memoria U27 utilizza il bus SPI privato del Si4684.

U27 **non** è uno slave del bus SPI principale dell'ESP32 e pertanto non
possiede una linea `CS` appartenente al namespace `SPI_*` del bus principale.

---

# SPI Topology

```text
                         ESP32-S31-WROOM-3
                              U11
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
             SPI_SCLK      SPI_MOSI      SPI_MISO
                 │             │             │
       ┌─────────┴─────────────┴─────────────┴─────────┐
       │                 SPI MAIN BUS                  │
       │                                                │
       ├── U5   TAC5212       ← SPI_CODEC_CS            │
       ├── U34  MCP23S17      ← SPI_DEV_MAN_A_CS        │
       ├── U36  MCP23S17      ← SPI_DEV_MAN_B_CS        │
       ├── U18  ADAU1467      ← SPI_ADAU1467_CS         │
       ├── U12  Si4684        ← SPI_SI4684_CS           │
       ├── U10  W25Q128JVS    ← SPI_W25Q128_CS          │
       └── U30  SC16IS740     ← SPI_UART_CS             │
                                                        │
       └────────────────────────────────────────────────┘


        PRIVATE SPI BUS                    PRIVATE SPI BUS
        ADAU1467                           Si4684
           U18                                U12
            │                                  │
            │ SPI                              │ SPI
            ▼                                  ▼
     U24 25AA1024                         U27 W25Q16JW
SPI Slave Summary
Bus	Master	Slave	Device
Main SPI	ESP32 U11	U5	TAC5212
Main SPI	ESP32 U11	U34	MCP23S17
Main SPI	ESP32 U11	U36	MCP23S17
Main SPI	ESP32 U11	U18	ADAU1467
Main SPI	ESP32 U11	U12	Si4684
Main SPI	ESP32 U11	U10	W25Q128JVS
Main SPI	ESP32 U11	U30	SC16IS740
Private SPI	ADAU1467 U18	U24	25AA1024
Private SPI	Si4684 U12	U27	W25Q16JW
Design Rules
SPI_SCLK, SPI_MOSI e SPI_MISO del bus principale sono condivisi tra
tutti gli slave del bus.
Ogni slave del bus principale deve avere una propria linea CS.
Deve essere attivo un solo CS alla volta durante una transazione SPI.
U24 e U27 non appartengono al bus SPI principale.
U24 è controllata direttamente dall'ADAU1467.
U27 è controllata direttamente dal Si4684.
I Chip Select dei bus privati non devono essere confusi con i CS
del bus SPI principale dell'ESP32.
La nomenclatura SPI_*_CS identifica esclusivamente le linee Chip Select
del bus SPI principale.
Main SPI Chip Select Map
SPI_CODEC_CS       → U5   TAC5212
SPI_DEV_MAN_A_CS   → U34  MCP23S17
SPI_DEV_MAN_B_CS   → U36  MCP23S17
SPI_ADAU1467_CS    → U18  ADAU1467
SPI_SI4684_CS      → U12  Si4684
SPI_W25Q128_CS     → U10  W25Q128JVS
SPI_UART_CS        → U30  SC16IS740
Stato

SPI principale: 7 slave.

SPI privato ADAU1467: 1 slave.

SPI privato Si4684: 1 slave.

Totale dispositivi SPI: 9.

Master SPI principale: ESP32-S31-WROOM-3.

Master SPI privati: ADAU1467 e Si4684.
