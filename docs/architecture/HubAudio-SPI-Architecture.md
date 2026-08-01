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

             System Controller

          System Controller

                |
                |
          SPI Control Bus

    +-----------+-----------+
    |                       |

Audio Processor                Radio Receiver

Audio Processor Radio Receiver



---

# 2. System Controller Control Domain

The System Controller is the system supervisor.

Its responsibilities are:

- system startup
- peripheral initialization
- configuration management
- communication with external devices
- firmware update coordination


The System Controller owns the main control SPI interface.

            System Controller

         SPI MASTER

              |
    +---------+---------+
    |                   |

 Audio Processor            Radio Receiver

SPI SLAVE          SPI SLAVE


The control bus is independent from all audio data paths.


---

# 3. Audio Processor SPI Domain

The Audio Processor contains its own SPI interface for external control.

The System Controller uses this interface for:

- DSP configuration
- parameter updates
- operational control
- status reading


The Audio Processor also manages its external program memory.

             Audio Processor

    +----------------------+
    |
    | SPI MASTER
    |
    v

          Audio EEPROM

   DSP Program Memory


The System Controller does not directly access the EEPROM during normal operation.

The Audio Processor is responsible for loading its DSP configuration.


---

# 4. Radio Receiver SPI Domain

The Radio Receiver is controlled by the System Controller through its SPI slave interface.

The System Controller manages:

- initialization sequence
- command exchange
- configuration
- firmware loading procedure


             System Controller

          SPI MASTER

               |

             Radio Receiver

               |

    Internal Firmware Management

               |

          Internal RAM


The Radio Receiver remains responsible for its internal operational memory.


---

# 5. SPI Bus Isolation Principle

The HubAudio architecture intentionally avoids a single shared SPI bus.

The design uses:

          System Controller

      +-------------+

      |             |

   SPI-A          SPI-B

      |             |

  Audio Processor       Radio Receiver


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

System Controller boot

|

Initialize SPI buses

|

Configure Audio Processor

|
+--> ADAU loads DSP program from Audio EEPROM

|

Configure Radio Receiver

|
+--> Firmware initialization

|

Enable Audio Domain

|

Audio Processor starts audio processing



---

# 7. Separation Between Domains


## Control Domain


System Controller

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

Audio Processor

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

The System Controller is the system coordinator.

The Audio Processor is the audio processor.

The Radio Receiver is a specialized audio peripheral.

Each component controls its own functional domain while remaining part of the
complete HubAudio system.