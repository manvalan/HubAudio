# ADAU1467 Hardware Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: Component Architecture


# 1. Overview

The ADAU1467 is the central audio processor of HubAudio.

It represents the boundary between:

- Control Domain
- Audio Domain
- Time Domain

The device provides:

- SigmaDSP processing
- digital audio routing
- serial audio interfaces
- clock generation
- self boot capability


The ADAU1467 is not considered a simple peripheral but the master component
of the Audio Domain.


---

# 2. Functional Role

The ADAU1467 performs:

- DSP execution
- audio mixing
- signal routing
- sample rate management
- digital audio synchronization


The ESP32-S3 configures the ADAU1467 but does not process real-time audio.


Architecture:


ESP32-S3

|
|

SPI

|

ADAU1467

|
|

I2S

Audio Peripherals



---

# 3. Power Architecture

The ADAU1467 requires separated power domains.

Main domains:


Digital Supply

DVDD

|

Digital core

Analog Supply

AVDD

|

PLL and analog sections

Interface Supply

IOVDD

|

Digital interfaces



Power design rules:

- local decoupling on every supply pin
- clean analog supply
- short return paths
- separation between noisy digital regulators and audio rails


The ADAU1467 power domains must be integrated with the HubAudio power
architecture.


---

# 4. Master Clock Architecture


The ADAU1467 uses an external reference clock.

Target audio clock family:


12.288 MHz

48 kHz × 256



Clock chain:


12.288 MHz Reference

    |

 ADAU1467

    |

Internal PLL

    |

Audio Clock Domain

    |

MCLK / BCLK / LRCLK



The ADAU1467 defines the timing reference of the Audio Domain.


---

# 5. Clock Distribution


The ADAU1467 clock output can be distributed using a dedicated clock buffer.


             ADAU1467

          Clock Master

                |

               MCLK

                |

         PCS2P2309NZ

          Clock Buffer

    +-----------+-----------+

    |           |           |

 CODEC       BT       Radio


The PCS2P2309NZ provides fan-out and signal integrity improvement.

It does not generate the audio clock.


---

# 6. SPI Control Interface


The ADAU1467 provides an SPI control interface.


Connection:


ESP32-S3

SPI MASTER

  |

  |

ADAU1467

SPI SLAVE



Used for:

- configuration
- parameter update
- status monitoring


---

# 7. Self Boot EEPROM


The ADAU1467 supports self boot from external EEPROM.


HubAudio implementation:



ADAU1467

SPI MASTER

  |

25AA1024 EEPROM

  |

DSP Program



During normal operation:

- ESP32 configures the ADAU1467
- ADAU1467 manages its DSP memory


The EEPROM remains part of the Audio Processor domain.


---

# 8. Serial Audio Interfaces


The ADAU1467 provides multiple serial audio ports.


HubAudio allocation:


Inputs:


SDATA_IN0

ESP32-S3

SDATA_IN1

Si4684

SDATA_IN2

Optical DECODEC

SDATA_IN3

Bluetooth RX



Outputs:


SDATA_OUT0

CODEC

SDATA_OUT1

Bluetooth TX

SDATA_OUT2

Optical ENCODEC



The ADAU1467 operates as audio timing master.


---

# 9. Boot Sequence



Power ON

|

ESP32-S3 startup

|

Configure ADAU1467

|

ADAU1467 loads DSP program

|

Audio clocks enabled

|

Audio peripherals synchronized

|

System ready



---

# 10. PCB Design Requirements


Critical signals:

- MCLK
- BCLK
- LRCLK
- SPI
- I2S DATA


Layout rules:

- continuous ground reference
- short clock traces
- avoid RF proximity
- local decoupling
- controlled return currents


The ADAU1467 section should be treated as a high-performance mixed-signal
audio subsystem.


---

# 11. Design Philosophy


The ADAU1467 is the conductor of the HubAudio orchestra.

The ESP32-S3 provides instructions.

The peripherals provide instruments.

The ADAU1467 defines timing, routing and processing.

