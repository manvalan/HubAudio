# HubAudio — MCP23S17 GPIO Distribution

**Progetto:** HubAudio  
**Revisione:** definitiva  
**Data:** 2026-08-22

---

## Distribuzione GPIO

| IC | PORTA | GPIO | Segnale | Direzione | Pull |
|---|---|---|---|---|---|
| U34 | A | GPA0 | `SI4684_RESET` | OUT | UP |
| U34 | A | GPA1 | `SI4684_SMODE` | OUT | - |
| U34 | A | GPA2 | `SI4684_ANT_SEL` | OUT | - |
| U34 | A | GPA3 | `SI4684_INT` | IN | - |
| U34 | A | GPA4 | `ADAU1467_RESET` | OUT | UP |
| U34 | A | GPA5 | `ADAU1467_SELFBOOT` | OUT/STRAP | UP |
| U34 | A | GPA6 | `RESERVED` | — | - |
| U34 | A | GPA7 | `MIC_SOURCE_SELECT` | OUT | - |
| U34 | B | GPB0 | `MIC_DETECT` | IN | UP |
| U34 | B | GPB1 | `LINE_IN_DETECT` | IN | UP |
| U34 | B | GPB2 | `LINE_OUT_DETECT` | IN | UP |
| U34 | B | GPB3 | `JACK_DETECT` | IN | UP |
| U34 | B | GPB4 | `BQ25896_INT` | IN | UP |
| U34 | B | GPB5 | `BQ25896_PG#` | IN | UP |
| U34 | B | GPB6 | `BQ27441_GPOUT` | IN | UP |
| U34 | B | GPB7 | `TPS63020_PG` | IN | UP |
| U36 | A | GPA0 | `BT1035_RESET` | OUT | - |
| U36 | A | GPA1 | `BT1035_SYSCTRL` | OUT | DOWN |
| U36 | A | GPA2 | `UART_RESET` | OUT | UP |
| U36 | A | GPA3 | `UART_INT` | IN | - |
| U36 | A | GPA4 | `ETH_RST#` | OUT | UP |
| U36 | A | GPA5 | `ANALOG_POWER_EN` | OUT | - |
| U36 | A | GPA6 | `ETHERNET_POWER_EN` | OUT | - |
| U36 | A | GPA7 | `BQ25896_PSEL` | OUT | - |
| U36 | B | GPB0 | `INA228_ANALOG_ALERT` | IN | UP |
| U36 | B | GPB1 | `INA228_DIGITAL_ALERT` | IN | UP |
| U36 | B | GPB2 | `TEMP_PWR_ALERT` | IN | UP |
| U36 | B | GPB3 | `TEMP_ESP32_ALERT` | IN | UP |
| U36 | B | GPB4 | `TEMP_ETH_ALERT` | IN | UP |
| U36 | B | GPB5 | `TEMP_CODEC_ALERT` | IN | UP |
| U36 | B | GPB6 | `RESERVED` | — | - |
| U36 | B | GPB7 | `RESERVED` | — | - |

---

# Pull-up / Pull-down

## Pull-UP

Le seguenti linee hanno pull-up esterno:

- `SI4684_RESET`
- `ADAU1467_RESET`
- `ADAU1467_SELFBOOT`
- `MIC_DETECT`
- `LINE_IN_DETECT`
- `LINE_OUT_DETECT`
- `JACK_DETECT`
- `BQ25896_INT`
- `BQ25896_PG#`
- `BQ27441_GPOUT`
- `TPS63020_PG`
- `UART_RESET`
- `ETH_RST#`
- `INA228_ANALOG_ALERT`
- `INA228_DIGITAL_ALERT`
- `TEMP_PWR_ALERT`
- `TEMP_ESP32_ALERT`
- `TEMP_ETH_ALERT`
- `TEMP_CODEC_ALERT`

Per le linee open-drain/status viene utilizzato come valore nominale:

**10 kΩ**

In particolare:

- `BQ27441_GPOUT` → 10 kΩ
- `TPS63020_PG` → 10 kΩ
- `INA228_ANALOG_ALERT` → 10 kΩ
- `INA228_DIGITAL_ALERT` → 10 kΩ
- `BQ25896_INT` → 10 kΩ
- `BQ25896_PG#` → 10 kΩ
- `TEMP_PWR_ALERT` → 10 kΩ
- `TEMP_ESP32_ALERT` → 10 kΩ
- `TEMP_ETH_ALERT` → 10 kΩ
- `TEMP_CODEC_ALERT` → 10 kΩ

## Pull-DOWN

- `BT1035_SYSCTRL` → **10 kΩ verso GND**

## Nessun pull esterno

- `SI4684_SMODE`
- `SI4684_ANT_SEL`
- `SI4684_INT`
- `MIC_SOURCE_SELECT`
- `BT1035_RESET`
- `UART_INT`
- `ANALOG_POWER_EN`
- `ETHERNET_POWER_EN`
- `BQ25896_PSEL`
- tutti i GPIO `RESERVED`

---

# Sensori di temperatura

Sono previsti sensori di temperatura **I²C** basati su **TMP117**.

I sensori sono distribuiti fisicamente sulla scheda per monitorare le zone termicamente più significative:

| Sensore | Zona | Posizione |
|---|---|---|
| `TEMP_PWR` | Dominio alimentazione | BOTTOM, vicino ai dispositivi di alimentazione |
| `TEMP_ESP32` | ESP32 | vicino all'ESP32 |
| `TEMP_ETH` | Ethernet / PHY | vicino al PHY Ethernet |
| `TEMP_CODEC` | Codec TAC5212 | vicino al codec |

I sensori condividono il bus I²C e vengono identificati tramite il relativo indirizzo `ADDR`.

Ogni sensore dispone di:

- alimentazione locale
- condensatore di bypass **100 nF**
- `SDA`
- `SCL`
- `ADDR`
- `ALERT`

### ALERT

L'uscita `ALERT` dei TMP117 viene utilizzata come segnalazione hardware verso il Device Manager:

- `TEMP_PWR_ALERT` → U36 GPB2
- `TEMP_ESP32_ALERT` → U36 GPB3
- `TEMP_ETH_ALERT` → U36 GPB4
- `TEMP_CODEC_ALERT` → U36 GPB5

Le linee `ALERT` sono ingressi del MCP23S17 e utilizzano un pull-up esterno da **10 kΩ**.

Il Device Manager può quindi ricevere immediatamente una segnalazione di superamento della soglia termica senza dover effettuare continuamente il polling dei sensori.

---

## Note sui dispositivi

### SI4684

`SI4684_RESET` è il reset active-low del dispositivo.

Il pull-up garantisce il rilascio del reset dopo la fase di power-up.

### ADAU1467

`ADAU1467_RESET` è active-low.

`ADAU1467_SELFBOOT` deve essere HIGH per il self-boot dalla EEPROM.

### TAC5212

Il codec `XTAC5212IRGER` è il **TAC5212**.

Non esiste un reset hardware dedicato da collegare al MCP23S17; il reset è gestito tramite la configurazione software del dispositivo.

**U34 GPA6 = RESERVED.**

### BT1035

`BT1035_RESET` non necessita di pull-up esterno perché il modulo dispone del proprio pull-up interno.

`BT1035_SYSCTRL` richiede invece il pull-down esterno.

### BQ27441

`GPOUT` è open-drain e il datasheet raccomanda esplicitamente una resistenza di pull-up da **10 kΩ**.

### TPS63020

`PG` è un'uscita **open-drain**. Il pull-up è quindi necessario quando il segnale viene utilizzato come ingresso digitale dal MCP23S17.

### INA228

`ALERT` è la linea di alert del monitor e viene utilizzata come ingresso verso il MCP23S17; è prevista con pull-up esterno.

### TMP117

Il TMP117 è utilizzato come sensore di temperatura locale.

La comunicazione avviene tramite I²C. Il pin `ALERT` viene utilizzato per generare una segnalazione hardware verso il Device Manager tramite U36.

Ogni sensore dispone di un proprio indirizzo I²C tramite il pin `ADDR`.

---

# Regola generale

Ogni net deve avere **una sola resistenza fisica di pull-up/pull-down**.

Se una net viene condivisa da più dispositivi, non devono essere installate resistenze duplicate sui vari dispositivi.

Il pull-up interno del MCP23S17 non viene utilizzato come sostituto dei pull-up esterni delle linee di stato/open-drain.

Per le linee `ALERT` dei TMP117 viene mantenuto il pull-up esterno da **10 kΩ**.

---

# Distribuzione funzionale

## U34 PORTA — Audio / Radio Control

| GPIO | Funzione |
|---|---|
| GPA0 | SI4684 RESET |
| GPA1 | SI4684 SMODE |
| GPA2 | SI4684 ANT SEL |
| GPA3 | SI4684 INT |
| GPA4 | ADAU1467 RESET |
| GPA5 | ADAU1467 SELFBOOT |
| GPA6 | RESERVED |
| GPA7 | MIC SOURCE SELECT |

## U34 PORTB — Detection / Power Status

| GPIO | Funzione |
|---|---|
| GPB0 | MIC DETECT |
| GPB1 | LINE IN DETECT |
| GPB2 | LINE OUT DETECT |
| GPB3 | JACK DETECT |
| GPB4 | BQ25896 INT |
| GPB5 | BQ25896 PG# |
| GPB6 | BQ27441 GPOUT |
| GPB7 | TPS63020 PG |

## U36 PORTA — BT / UART / Ethernet / Power

| GPIO | Funzione |
|---|---|
| GPA0 | BT1035 RESET |
| GPA1 | BT1035 SYSCTRL |
| GPA2 | UART RESET |
| GPA3 | UART INT |
| GPA4 | ETH RESET |
| GPA5 | ANALOG POWER EN |
| GPA6 | ETHERNET POWER EN |
| GPA7 | BQ25896 PSEL |

## U36 PORTB — Power / Temperature Monitoring

| GPIO | Funzione |
|---|---|
| GPB0 | INA228 ANALOG ALERT |
| GPB1 | INA228 DIGITAL ALERT |
| GPB2 | TEMP PWR ALERT |
| GPB3 | TEMP ESP32 ALERT |
| GPB4 | TEMP ETH ALERT |
| GPB5 | TEMP CODEC ALERT |
| GPB6 | RESERVED |
| GPB7 | RESERVED |

---

# Tabella resistenze da inserire nello schematico

| Net | Resistenza | Collegamento |
|---|---:|---|
| `SI4684_RESET` | 10 kΩ | VIO → RESET |
| `ADAU1467_RESET` | 10 kΩ | IOVDD → RESET |
| `ADAU1467_SELFBOOT` | 10 kΩ | IOVDD → SELFBOOT |
| `MIC_DETECT` | 10 kΩ | VIO → DETECT |
| `LINE_IN_DETECT` | 10 kΩ | VIO → DETECT |
| `LINE_OUT_DETECT` | 10 kΩ | VIO → DETECT |
| `JACK_DETECT` | 10 kΩ | VIO → DETECT |
| `BQ25896_INT` | 10 kΩ | VIO → INT |
| `BQ25896_PG#` | 10 kΩ | VIO → PG# |
| `BQ27441_GPOUT` | 10 kΩ | VDD → GPOUT |
| `TPS63020_PG` | 10 kΩ | VOUT/VIO → PG |
| `BT1035_SYSCTRL` | 10 kΩ | SYSCTRL → GND |
| `UART_RESET` | 10 kΩ | VIO → RESET |
| `ETH_RST#` | 10 kΩ | VIO → RESET# |
| `INA228_ANALOG_ALERT` | 10 kΩ | VIO → ALERT |
| `INA228_DIGITAL_ALERT` | 10 kΩ | VIO → ALERT |
| `TEMP_PWR_ALERT` | 10 kΩ | VIO → ALERT |
| `TEMP_ESP32_ALERT` | 10 kΩ | VIO → ALERT |
| `TEMP_ETH_ALERT` | 10 kΩ | VIO → ALERT |
| `TEMP_CODEC_ALERT` | 10 kΩ | VIO → ALERT |

---

# Stato

**U34:** assegnazione completa.

**U36:** assegnazione completa.

**TAC5212:** nessun GPIO dedicato al reset.

**BT1035_RESET:** nessun pull esterno.

**BT1035_SYSCTRL:** 10 kΩ pull-down.

**Linee open-drain/status:** pull-up 10 kΩ.

**TMP117:** 4 sensori I²C distribuiti nelle zone termicamente significative.

**TMP117 ALERT:** collegati al Device Manager tramite U36 GPB2–GPB5.

**U34 GPA6:** RESERVED.

**U36 GPB6–GPB7:** RESERVED.

**INTB U34/U36:** non collegati intenzionalmente.
