# HubAudio System Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: System Architecture


# 1. Overview

HubAudio is a modular digital audio platform designed around a centralized
Audio Domain architecture.

The system separates three main functional areas:

- Control Domain
- Audio Domain
- Clock Distribution Layer

Each area has a clearly defined responsibility.

The architecture is based on the principle:


System Controller System Controller manages the Control Domain.

Audio Processor Audio Processor manages the Audio Domain.

The Clock Distribution Layer provides the synchronization reference
for all digital audio peripherals.


The Audio Processor acts as the timing and routing authority of the digital
audio infrastructure, while the System Controller provides supervision,
connectivity and configuration management.

# 2. High Level Architecture
                     HUBAUDIO


                CONTROL DOMAIN

             System Controller System Controller

          Network / UI / Configuration

                       |

                       |

                      SPI

                       |

        +--------------+--------------+

        |                             |

 Audio Processor Audio Processor      Radio Receiver Radio Receiver

        |
        |
        |
     AUDIO DOMAIN


 Audio Sources:

 System Controller System Controller
 Radio Receiver Radio Receiver
 Bluetooth Receiver
 Optical Input


        |

        |

 Audio Processing

 DSP / Routing / Mixing


        |

        |

 Audio Destinations:

 CODEC/DAC
 Bluetooth Transmitter
 Optical Output


                       |

                       |

          CLOCK DISTRIBUTION LAYER

                       |

              MCLK / BCLK / LRCLK

# 3. Functional Domains


# 3.1 Control Domain

The Control Domain is responsible for system management.

Main component:


System Controller


Responsibilities:

- network connectivity
- streaming services
- user interface
- configuration management
- firmware update coordination
- device supervision


Communication:


System Controller

  |

 SPI

  |

Audio peripherals



The Control Domain does not transport real-time audio.


---

# 3.2 Audio Domain

The Audio Domain is centered around the Audio Processor.

The Audio Processor is responsible for:

- DSP processing
- audio routing
- mixing
- digital effects
- format conversion
- audio synchronization


Audio sources:


System Controller
Radio Receiver
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

The Audio Processor is the audio clock master.

The clock distribution provides:

- MCLK
- BCLK
- LRCLK


Clock distribution:

             Audio Processor

         Audio Clock Master

                |

                |

          Clock Buffer

                |

    +-----------+-----------+

    |           |           |

  CODEC      Radio Receiver      BT


---

# 4. Component Roles


## System Controller

Role:

System Controller + Audio Source


Functions:

- network audio streaming
- system management
- configuration


Inside Audio Domain:


I2S Source



---

## Audio Processor

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

## Radio Receiver

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

Audio Processor



Bluetooth TX:


Audio Processor

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

Audio Processor



Output:


Audio Processor

|

I2S

|

ENCODEC

|

SPDIF



---

# 5. Design Philosophy


HubAudio follows a distributed intelligence model.

The System Controller provides connectivity and supervision.

The Audio Processor provides audio intelligence.

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

System Controller
|
SPI

AUDIO PLANE

Audio Processor
|
I2S

TIME PLANE

Audio Processor
|
Clock Distribution



This separation defines the fundamental architecture of HubAudio.