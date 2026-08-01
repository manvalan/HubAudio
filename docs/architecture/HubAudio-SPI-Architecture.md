# HubAudio SPI Control Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: Architecture Specification


# 1. Overview

The HubAudio system separates the control communication layer from the audio
signal layer.

SPI is used exclusively for:

- device configuration
- initialization
- status monitoring
- firmware loading procedures
- parameter management

SPI is not used for real-time audio transport.


The control architecture is based on independent SPI domains.


CONTROL PLANE

             ESP32-S3

          System Controller

                |
                |
          SPI Control Bus

    +-----------+-----------+
    |                       |

ADAU1467                Si4684

Audio Processor Radio Receiver



---

# 2. ESP32-S3 Control Domain

The ESP32-S3 is the system supervisor.

Its responsibilities are:

- system startup
- peripheral initialization
- configuration management
- communication with external devices
- firmware update coordination


The ESP32-S3 owns the main control SPI interface.

            ESP32-S3

         SPI MASTER

              |
    +---------+---------+
    |                   |

 ADAU1467            Si4684

SPI SLAVE          SPI SLAVE


The control bus is independent from all audio data paths.


---

# 3. ADAU1467 SPI Domain

The ADAU1467 contains its own SPI interface for external control.

The ESP32-S3 uses this interface for:

- DSP configuration
- parameter updates
- operational control
- status reading


The ADAU1467 also manages its external program memory.

             ADAU1467

    +----------------------+
    |
    | SPI MASTER
    |
    v

          25AA1024

   DSP Program Memory


The ESP32-S3 does not directly access the EEPROM during normal operation.

The ADAU1467 is responsible for loading its DSP configuration.


---

# 4. Si4684 SPI Domain

The Si4684 is controlled by the ESP32-S3 through its SPI slave interface.

The ESP32-S3 manages:

- initialization sequence
- command exchange
- configuration
- firmware loading procedure


             ESP32-S3

          SPI MASTER

               |

             Si4684

               |

    Internal Firmware Management

               |

          Internal RAM


The Si4684 remains responsible for its internal operational memory.


---

# 5. SPI Bus Isolation Principle

The HubAudio architecture intentionally avoids a single shared SPI bus.

The design uses:

          ESP32-S3

      +-------------+

      |             |

   SPI-A          SPI-B

      |             |

  ADAU1467       Si4684


Advantages:

- no chip-select conflicts
- independent timing
- reduced electrical loading
- easier firmware management
- simpler debugging


---

# 6. Boot Sequence

The expected startup sequence is:



Power ON

|

ESP32-S3 boot

|

Initialize SPI buses

|

Configure ADAU1467

|
+--> ADAU loads DSP program from 25AA1024

|

Configure Si4684

|
+--> Firmware initialization

|

Enable Audio Domain

|

ADAU1467 starts audio processing



---

# 7. Separation Between Domains


## Control Domain


ESP32-S3

|
|

SPI

|

Peripheral configuration



## Audio Domain


Audio Sources

|
|

I2S

|

ADAU1467

|

Audio Outputs



The two domains interact only through configuration and status information.


---

# 8. Design Rules

SPI signals require:

- controlled routing
- clean reference plane
- appropriate termination where required
- separation from high-speed clock signals


Critical signals:

- SCLK
- MOSI
- MISO
- CS


---

# 9. Design Philosophy

The ESP32-S3 is the system coordinator.

The ADAU1467 is the audio processor.

The Si4684 is a specialized audio peripheral.

Each component controls its own functional domain while remaining part of the
complete HubAudio system.