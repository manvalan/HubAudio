# HubAudio System Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: System Architecture


# 1. Overview

HubAudio is a modular digital audio platform designed around a centralized
audio processing architecture.

The system separates three main functional domains:

- Control Domain
- Audio Domain
- Time Domain

Each domain has a clearly defined responsibility.

The architecture is based on the principle:


ESP32-S3 manages the system.

ADAU1467 manages the audio.

The clock domain synchronizes the orchestra.



---

# 2. High Level Architecture


                     HUBAUDIO


                CONTROL DOMAIN

                     ESP32-S3

              WiFi / Network / UI

                         |

                         |

                       SPI

                         |

         +---------------+---------------+

         |                               |

      ADAU1467                        Si4684

  Audio Processor                Radio Receiver


         |
         |
         |
    AUDIO DOMAIN


         |
 +-------+-------+-------+-------+
 |       |       |       |       |

ESP32 Si4684 BT RX Optical Other

         |

      ADAU1467

    DSP / Routing / Mixing


         |

 +-------+-------+-------+

 |       |       |

CODEC BT TX Optical Out

         |

    TIME DOMAIN

         |

    Audio Clock Tree

         |

    MCLK / BCLK / LRCLK


---

# 3. Functional Domains


# 3.1 Control Domain

The Control Domain is responsible for system management.

Main component:


ESP32-S3


Responsibilities:

- network connectivity
- streaming services
- user interface
- configuration management
- firmware update coordination
- device supervision


Communication:


ESP32-S3

  |

 SPI

  |

Audio peripherals



The Control Domain does not transport real-time audio.


---

# 3.2 Audio Domain

The Audio Domain is centered around the ADAU1467.

The ADAU1467 is responsible for:

- DSP processing
- audio routing
- mixing
- digital effects
- format conversion
- audio synchronization


Audio sources:


ESP32-S3
Si4684
Bluetooth RX
Optical Input



Audio destinations:


CODEC/DAC
Bluetooth TX
Optical Output



The audio transport uses:


I2S



---

# 3.3 Time Domain

The Time Domain provides the synchronization reference.

The ADAU1467 is the audio clock master.

The clock distribution provides:

- MCLK
- BCLK
- LRCLK


Clock distribution:

             ADAU1467

         Audio Clock Master

                |

                |

          Clock Buffer

                |

    +-----------+-----------+

    |           |           |

  CODEC      Si4684      BT


---

# 4. Component Roles


## ESP32-S3

Role:

System Controller + Audio Source


Functions:

- network audio streaming
- system management
- configuration


Inside Audio Domain:


I2S Source



---

## ADAU1467

Role:

Audio Domain Master


Functions:

- DSP
- routing
- mixing
- clock generation


Interfaces:


SPI -> Configuration
I2S -> Audio
Clock -> Synchronization



---

## Si4684

Role:

Digital Radio Audio Source


Functions:

- FM reception
- DAB/DAB+
- digital audio output


Interfaces:


SPI -> Control

I2S -> Audio



---

## Bluetooth Modules

Role:

Wireless Audio Interfaces


Bluetooth RX:


BT Audio

|

I2S

|

ADAU1467



Bluetooth TX:


ADAU1467

|

I2S

|

BT Transmitter



---

## Digital Converters

Optical interfaces are handled through dedicated conversion stages.


Input:


SPDIF

|

DECODEC

|

I2S

|

ADAU1467



Output:


ADAU1467

|

I2S

|

ENCODEC

|

SPDIF



---

# 5. Design Philosophy


HubAudio follows a distributed intelligence model.

The ESP32-S3 provides connectivity and supervision.

The ADAU1467 provides audio intelligence.

Dedicated peripherals provide specialized functions.


The architecture avoids making the microcontroller responsible for
time-critical audio processing.


---

# 6. Expansion Strategy


The architecture allows future integration of:

- additional audio sources
- additional DSP processing
- microphones
- sensors
- alternative wireless interfaces


Expansion follows the same principle:

Control:


SPI



Audio:


I2S



Synchronization:


Clock Domain



---

# 7. Summary


HubAudio is structured around three independent but coordinated planes:



CONTROL PLANE

ESP32-S3
|
SPI

AUDIO PLANE

ADAU1467
|
I2S

TIME PLANE

ADAU1467
|
Clock Distribution



This separation defines the fundamental architecture of HubAudio.