# HubAudio PCB Floor Plan

- Status: Draft
- Date: 2026-08-01
- Document Type: Hardware Architecture


# 1. Overview

This document defines the preliminary PCB floor plan for the HubAudio
single-board audio platform.

The PCB integrates:

- System Controller
- Audio Processor
- Radio Receiver
- Wireless Audio Interfaces
- Digital Audio Interfaces
- Power Management
- Battery Operation Support


The floor plan follows the fundamental HubAudio architecture:


ESP32-S3 manages the Control Domain.

ADAU1467 manages the Audio Domain.

The Clock Distribution Layer provides synchronization
for digital audio peripherals.


The PCB layout must preserve separation between:

- Control Domain
- Audio Domain
- Clock Domain
- Power Domain


The objective is to create a compact portable audio platform while
maintaining:

- audio signal integrity
- clock stability
- RF performance
- power efficiency
- battery operation capability


---

# 2. PCB Constraints


## 2.1 Target Dimensions


The HubAudio board is designed as a compact single-board platform.


Preferred PCB size:
Layer 1
Component placement
Critical digital signals
Audio routing

Layer 2
Continuous GND plane

Layer 3
Power distribution

Layer 4
Control signals
Low speed routing
Auxiliary signals


A 6-layer PCB remains an optional evolution only if required after
routing verification.


The transition to 6 layers must be justified by:

- routing density
- clock integrity
- RF isolation requirements
- power distribution constraints


The initial architecture target remains:
4 Layer PCB


---

# 4. Functional PCB Zones


The PCB is divided into five functional areas.


## 4.1 Control Zone


Contains:

- ESP32-S3
- USB interface
- programming interface
- user interface connections


Responsibilities:

- network connectivity
- streaming control
- configuration management
- firmware updates


Placement requirements:

- close to PCB edge
- antenna clearance
- separated from switching regulators


---

## 4.2 Audio Processing Zone


Contains:

- ADAU1467
- Audio EEPROM
- Clock circuitry
- Audio domain support components


The ADAU1467 is the physical center of the Audio Domain.


Responsibilities:

- DSP processing
- routing
- mixing
- synchronization


Critical signals:

- MCLK
- BCLK
- LRCLK
- I2S DATA


must remain short.


---

## 4.3 Radio Zone


Contains:

- Si4684
- RF interface
- antenna related components


Placement requirements:

- close to RF input
- separated from switching noise
- local power filtering


The Si4684 operates as a digital audio peripheral
inside the Audio Domain.


---

## 4.4 Audio Interface Zone


Contains:

- Bluetooth interfaces
- Optical interfaces
- CODEC/DAC stages


Interfaces:
I2S
|
ADAU1467


Placement requirements:

- close to PCB edge
- short I2S paths
- controlled supply filtering


---

## 4.5 Power Zone


Contains:

- Battery input
- USB power input
- Charger
- PMIC
- Regulators
- Filtering components


Placement:

PCB edge area


Power path:

Battery / USB

  |

Protection

  |

Charger

  |

PMIC

  |

Regulators

  |

Digital / Analog domains



The Power Zone must remain physically separated from:

- clock circuitry
- RF section
- sensitive audio signals


---

# 5. Preliminary Floor Plan


Conceptual arrangement:



+--------------------------------+
| |
| ESP32-S3 Si4684 |
| CONTROL RADIO |
| |
| |
| CLOCK |
| BUFFER |
| | |
| | |
| ADAU1467 |
| AUDIO PROCESSOR |
| |
| |
| BT RX SPDIF CODEC BT TX |
| AUDIO INTERFACE |



BATTERY / PMIC / CHARGER
POWER DOMAIN

+--------------------------------+

PCB TARGET:

90 mm x 70 mm



This arrangement keeps the ADAU1467 physically central.

The placement minimizes:

- I2S length
- clock distribution length
- audio routing complexity


---

# 6. ADAU1467 Placement


The ADAU1467 is the physical center of the digital audio subsystem.


This follows the architecture decision:



ADAU1467 = Audio Domain Master



Placement rules:

- central PCB position
- shortest clock paths
- shortest I2S paths
- local decoupling network
- separated from switching regulators


The ADAU1467 area includes:

- DSP processor
- clock interface
- SPI configuration interface
- audio EEPROM


Critical signals:


MCLK
BCLK
LRCLK
I2S DATA



must be routed with priority.


---

# 7. ESP32-S3 Placement


The ESP32-S3 belongs to the Control Domain.


Placement rules:

- PCB edge placement
- antenna keep-out area
- USB accessibility
- separation from analog audio


The ESP32-S3 interfaces:

Control:


SPI



Audio:


I2S Source



The ESP32-S3 is not the audio clock master.


---

# 8. Clock Distribution Placement


The Clock Distribution Layer provides:

- MCLK
- BCLK
- LRCLK


Architecture:


         ADAU1467

      Audio Clock Master

             |

      Clock Buffer

             |

 +-----------+-----------+

 |           |           |

CODEC Si4684 BT



Clock traces must have priority routing.


---

# 9. Routing Priorities


Routing priority:


1. Clock signals


MCLK
BCLK
LRCLK



2. I2S audio buses


3. SPI control


4. Power distribution


5. Low-speed signals


Clock and audio signals must avoid:

- switching regulator nodes
- RF traces
- high current battery paths


---

# 10. Summary


The HubAudio PCB follows the architectural separation:



CONTROL DOMAIN

ESP32-S3

    SPI

AUDIO DOMAIN

ADAU1467

    I2S

CLOCK DOMAIN

Clock Distribution

POWER DOMAIN

Battery / PMIC / Regulators



The floor plan defines a compact single-board implementation
optimized for:

- portability
- battery operation
- audio integrity
- future expansion