# Mappatura Hardware e Pinout: ESP32-S31-WROOM-3

Questo documento raccoglie la configurazione completa e definitiva dei pin per il modulo **ESP32-S31-WROOM-3** utilizzata nel layout del PCB.

---

## 1. Tabella Definitiva Mappatura Hardware

| Periferica / Blocco | Segnale Hardware | GPIO ESP32-S31 | Pin Schema | Note e Connessioni Hardware |
| :--- | :--- | :--- | :--- | :--- |
| **ETHERNET (RMII / LAN8720A)** | `ETH_50MHZ_CLOCK` | **GPIO13** | **Pin 19** | Ingresso Clock 50 MHz da oscillatore |
| | `ETH_TXD0` | **GPIO8** | **Pin 14** | Dati TX Bit 0 |
| | `ETH_TXD1` | **GPIO9** | **Pin 15** | Dati TX Bit 1 |
| | `ETH_TXEN` | **GPIO12** | **Pin 18** | Transmit Enable |
| | `ETH_RXD0` | **GPIO19** | **Pin 25** | Dati RX Bit 0 |
| | `ETH_RXD1` | **GPIO18** | **Pin 24** | Dati RX Bit 1 |
| | `ETH_CRS_DV` | **GPIO15** | **Pin 21** | Carrier Sense / Data Valid |
| | `ETH_MDC` | **GPIO5** | **Pin 11** | Clock Gestione PHY |
| | `ETH_MDIO` | **GPIO6** | **Pin 12** | Dati Gestione PHY (Pull-up 1.5 kΩ ~ 4.7 kΩ) |
| | `ETH_RST#` | **GPIO7** | **Pin 13** | Reset Hardware LAN8720A |
| | `ETH_RXER` | **GPIO10** | **Pin 16** | Receive Error / Config. Indirizzo PHY0 |
| | `ETH_INT#` | **GPIO4** | **Pin 10** | Interruzione PHY (Pull-up 10 kΩ) |
| **SPI BUS (Master)** | `SPI_MOSI` | **GPIO2** | **Pin 6** | Dati in Uscita (Condiviso Si4684 + ADAU1467)[cite: 1] |
| | `SPI_MISO` | **GPIO3** | **Pin 7** | Dati in Ingresso (Condiviso Si4684 + ADAU1467)[cite: 1] |
| | `SPI_CLK` | **GPIO1** | **Pin 9** | Clock Serial SPI[cite: 1] |
| | `SPI_SI4684_CS` | **GPIO16** | **Pin 22** | Chip Select Radio Si4684[cite: 1] |
| | `SPI_ADAU1467_CS` | **GPIO17** | **Pin 23** | Chip Select DSP ADAU1467[cite: 1] |
| **I2C BUS (Master)** | `I2C_SDA` | **GPIO50** | **Pin 60** | (Pull-up 4.7 kΩ) |
| | `I2C_SCL` | **GPIO51** | **Pin 61** | (Pull-up 4.7 kΩ) |
| **I2S_0 (Slave)** | `I2S0_BCLK` | **GPIO42** | **Pin 52** | Bit Clock (Ingresso da Master esterno)[cite: 1] |
| | `I2S0_LRCLK` | **GPIO43** | **Pin 53** | Frame Sync / WS (Ingresso da Master)[cite: 1] |
| | `I2S0_DATA` | **GPIO44** | **Pin 54** | Dati Audio 1[cite: 1] |
| **I2S_1 (Slave)** | `I2S1_BCLK` | **GPIO46** | **Pin 56** | Bit Clock (Ingresso da Master esterno)[cite: 1] |
| | `I2S1_LRCLK` | **GPIO47** | **Pin 57** | Frame Sync / WS (Ingresso da Master)[cite: 1] |
| | `I2S1_DATA` | **GPIO48** | **Pin 58** | Dati Audio 2[cite: 1] |
| **UART BT1035** | `BT_TX` | **GPIO52** | **Pin 62** | Collegare a **RXD** del modulo BT1035 |
| | `BT_RX` | **GPIO53** | **Pin 63** | Collegare a **TXD** del modulo BT1035 |
| | `BT_RTS` *(Opz.)* | **GPIO54** | **Pin 64** | Controllo di flusso (Collegare a **CTS** del BT1035) |
| | `BT_CTS` *(Opz.)* | **GPIO55** | **Pin 65** | Controllo di flusso (Collegare a **RTS** del BT1035) |
| **INTERRUPTS & IO** | `PCA_POWER_INT` | **GPIO11** | **Pin 17** | Interruzione da espansore I2C PCA9555 (Power Unit)[cite: 1] |
| | `SPARE_IO0` | **GPIO16** | **Pin 22** | GPIO libero / Riserva[cite: 1] |
| | `SPARE_IO1` | **GPIO17** | **Pin 23** | GPIO libero / Riserva[cite: 1] |
| **SYSTEM & BOOT** | `ESP_EN` | **EN** | **Pin 5** | Reset Hardware (Pull-up 10 kΩ + Cap 1 µF verso GND)[cite: 1] |
| | `ESP_BOOT` | **GPIO61** | **Pin 71** | Strapping Pin / Pulsante BOOT (Pull-up interno)[cite: 1] |
| | `USB_DP` | **USB_DP** | **Pin 40** | USB Data+ (Coppia differenziale 90 Ω)[cite: 1] |
| | `USB_DM` | **USB_DM** | **Pin 41** | USB Data- (Coppia differenziale 90 Ω)[cite: 1] |

---

## 2. Note di Progettazione Hardware

### USB Serial / JTAG Integrato
* Per programmazione e debug è sufficiente un singolo connettore **USB Type-C** direttamente collegato a `USB_DP` (Pin 40) e `USB_DM` (Pin 41)[cite: 1].
* Inserire **due resistenze da 5.1 kΩ** su CC1 e CC2 verso GND sul connettore Type-C.

### Bus SPI
* I dispositivi controllati in SPI sono 2: **Si4684** (`CS0` su `GPIO13`) e **ADAU1467** (`CS1` su `GPIO14`)[cite: 1].
* Aggiungere resistori di **pull-up esterni da 10 kΩ a 3.3V** sulle linee CS per garantire lo stato HIGH durante il boot.

### Bus I2C
* Il codec **TLV320AIC3104** (indirizzo `0x18`) è controllato via I2C (`GPIO50` per SDA e `GPIO51` per SCL).
* Prevedere due resistori di pull-up esterni da **2.2 kΩ a 4.7 kΩ** verso 3.3V.

### Interfacce I2S Audio
* Entrambi i canali I2S sono configurati in modalità **Slave**. I segnali di clock `BCLK` e `LRCLK` provengono dai rispettivi dispositivi Master esterni[cite: 1].
