# HubAudio
## Modular Network Audio Platform
### Hardware Architecture and Engineering Design Document

**Project:** HubAudio  
**Document:** Hardware Architecture Specification  
**Revision:** 0.1  
**Status:** Design Phase  
**Target MCU:** ESP32-S3  
**Architecture:** Modular Audio Processing Platform  

---

# 1. Introduction

HubAudio is a modular high-quality network audio platform designed around a central DSP audio architecture.

The goal is not to create a simple Internet radio, but a flexible audio processing system capable of integrating multiple digital audio sources:

- FM radio
- DAB/DAB+ radio
- Bluetooth audio
- Network streaming
- Future digital sources

All audio sources are converted into a common digital audio stream and processed by a dedicated DSP before being sent to the final audio output stage.

The core design philosophy is:

> Keep the audio path fully digital until the final DAC stage.

The system is designed as a professional embedded audio platform, with concepts derived from industrial and commercial audio products:

- modular hardware blocks
- independent firmware management
- device identification
- firmware update capability
- replaceable source modules
- DSP-based audio processing


---

# 2. Design Goals

## Primary objectives

The HubAudio platform shall provide:

- High quality audio processing
- Multiple independent audio sources
- Network connectivity
- Bluetooth integration
- Digital signal processing
- Expandability
- Long-term maintainability


## Audio sources

The initial supported sources are:

| Source | Device |
|-|-|
| FM/DAB+ Radio | Skyworks Si4684 |
| Bluetooth TX | FSC-BT1035 |
| Bluetooth RX | FSC-BT1026 or equivalent |
| Network Audio | ESP32-S3 |


---

# 3. System Overview

The system is composed of four main functional blocks:

                     HUBAUDIO


                     ESP32-S3
                        |
         System control / Network / MQTT
                        |
    +-------------------+-------------------+
    |                   |                   |
    |                   |                   |
 Si4684             BT RX Module        BT1035
FM/DAB+             A2DP Sink           A2DP Source
    |                   |                   |
    |                   |                   |
    +-------------------+-------------------+

                        |
                       I2S

                        |
                        |
                  ADAU1467 DSP

                        |
                        |
                     DAC Stage

                        |
                        |
                Power Amplifier



---

# 4. System Philosophy

## Modular approach

Each functional block is considered an independent subsystem.

Modules:
+-----------------------------+
| Audio Module |
| |
| Processing IC |
| EEPROM Identification |
| Firmware Storage |
| Local configuration |
| I2S Interface |
| Control Interface |
+-----------------------------+

Every module shall contain:

- hardware identification
- revision information
- serial number
- configuration data


The identification device is:


24AA025E48T-I/OT


which provides:

- EEPROM memory
- factory programmed MAC address
- unique identification


---

# 5. Global Architecture

## Control domain

The ESP32-S3 is the system controller.

Responsibilities:

- WiFi connection
- MQTT communication
- Web interface
- OTA updates
- module discovery
- configuration management
- power sequencing


The ESP32-S3 does NOT process the main audio stream.

Audio remains outside the MCU.

---

## Audio domain

The audio domain is controlled by:


ADAU1467


The DSP is the central audio router.

Responsibilities:

- equalization
- filters
- crossover
- volume control
- loudness
- audio routing
- room correction


---

# 6. Audio Data Flow


## Bluetooth reception

Example:


Smartphone

|

Bluetooth A2DP

|

BT RX Module

|

I2S

|

ADAU1467

|

DAC

|

Amplifier



---

## Bluetooth transmission

Example:


Radio / Streaming

   |

ADAU1467

   |

  I2S

   |

BT1035

   |

Bluetooth TX

   |

Headphones



---

## Radio reception



Antenna

|

Si4684

|

I2S

|

ADAU1467

|

DAC



---

# 7. Power Architecture

The system shall use separated power domains.


Recommended domains:



VIN

|

+----------------+
|
+-- Digital 3.3V
|
| ESP32-S3
| EEPROM
| Control IC
|
|
+-- Audio 3.3V
|
| ADAU1467
| Audio modules
|
|
+-- RF supply
Si4684
Bluetooth modules



Important:

RF and audio domains must be isolated from noisy digital switching sources.


---

# 8. Firmware Storage Concept


The system supports independent firmware storage.

Example:



ESP32 Flash

|
|
+-- HubAudio Firmware

SPI Flash

|
|
+-- Si4684 firmware

SPI Flash

|
|
+-- ADAU1467 DSP program



The ESP32-S3 manages:

- firmware verification
- checksum
- update
- programming sequence


---

# 9. Update Procedure


Firmware update sequence:


ESP32 receives firmware
Disable audio modules
Power down Si4684 / ADAU1467
Program external memory
Verify checksum
Restart module
Resume operation


This avoids requiring direct programming access during normal operation.


---

# 10. Hardware Design Rules


## Clocking

I2S requires careful definition:

Possible configurations:

### Option A

ADAU1467 as I2S master.

Advantages:

- single audio clock source
- better synchronization


### Option B

Source modules as masters.

Requires:

- clock switching
- sample rate management


Preferred:

ADAU1467 master.


---

# 11. Open Engineering Points

The following points require verification during schematic phase:


## I2S topology

Need to verify:

- master/slave capability of each module
- supported sample rates
- MCLK requirement


## Bluetooth Gateway Function

The system intentionally separates:

- Bluetooth RX
- Bluetooth TX

because simultaneous A2DP RX/TX operation on a single Bluetooth module is not guaranteed.


The chosen architecture is:



BT RX Module

BT1035 TX Module

ADAU1467 routing



This provides reliable simultaneous operation.

---
# 12. ESP32-S3 System Controller

## 12.1 Overview

The ESP32-S3 is the main system controller of HubAudio.

It is responsible for:

- system initialization
- network communication
- MQTT management
- Web interface
- OTA firmware updates
- module identification
- power management
- configuration storage
- communication with audio peripherals


The ESP32-S3 is NOT part of the main audio signal chain.

The audio stream shall never pass through the MCU.

---

# 12.2 ESP32-S3 Main Interfaces

The ESP32-S3 communicates with the audio modules using:


| Function | Interface |
|-|-|
| Si4684 control | SPI |
| ADAU1467 control | I2C/SPI |
| Bluetooth modules | UART |
| EEPROM identification | I2C |
| Audio control | GPIO |
| Power management | GPIO |

---

# 12.3 Recommended ESP32-S3 Connections


## Power Supply

ESP32-S3 requires:

- 3.3V regulated supply
- low noise supply
- adequate decoupling close to pins


Recommended:


3.3V

|
+---- 10uF
|
+---- 100nF
|
ESP32-S3 VDD



Important:

The ESP32-S3 has high current peaks during WiFi transmission.

The regulator must support:

- >500mA transient capability
- low output impedance


Recommended regulators:

- TPS62162
- AP63203
- similar low noise buck converters


---

# 12.4 Important GPIO Considerations


ESP32-S3 pins have boot functions.

Avoid using boot-sensitive pins for critical peripherals.

Important signals:


## EN

Chip enable:


EN

HIGH = normal operation
LOW = reset



Recommended:

- RC reset network
- external supervisor optional


---

## UART

Recommended:


ESP32-S3 TX
|
|
Module RX

ESP32-S3 RX
|
|
Module TX



Used for:

- Bluetooth configuration
- module diagnostics


---

## I2C Bus


Shared bus:



ESP32-S3

SDA
|
+---- 24AA025E48
|
+---- ADAU1467
|
+---- sensors / expansion

SCL
|
+---- devices



Recommended pull-ups:

Typically:

2.2k - 4.7k

depending on bus length.


---

# 12.5 ESP32-S3 Firmware Architecture


Software layers:



Application

|
|
HubAudio Manager

|
+----------------+
| |
Drivers Network

|
Hardware abstraction

|
ESP32 HAL



The MCU shall manage modules as independent devices.


Example:



detect modules

read EEPROM

load configuration

initialize devices

start audio routing



---

# 13. Skyworks Si4684 Radio Module


## 13.1 Overview


The Si4684 is the selected radio receiver IC.


Functions:

- FM receiver
- AM receiver
- DAB/DAB+
- RDS/RBDS
- digital audio output


The device is selected because it integrates:

- RF receiver
- digital demodulation
- audio processing
- DAB stack


The Si4684 is treated as a complete radio subsystem.


---

# 13.2 Si4684 System Architecture



Antenna

|

RF Matching

|

Si4684

|

Digital Audio I2S

|

ADAU1467



---

# 13.3 Si4684 Control Interface


The preferred interface:

SPI


Connections:



ESP32-S3 Si4684

SPI CLK -----------> SCLK

SPI MOSI ----------> SDIO

SPI CS ------------> CS

GPIO --------------> RESET

GPIO <-------------- IRQ



---

# 13.4 Important Si4684 Pins


## VDD


Requirements:

- clean 3.3V supply
- RF filtering required


Recommended:



3.3V

|
Ferrite bead

|

Si4684 VDD

|
100nF
1uF
10uF



The RF section is sensitive to noise.


---

## RESET


Active low.


Recommended:



ESP GPIO

|

RESET

|

10k pull-up

|

3.3V



The MCU must control reset during startup.


---

## IRQ


Interrupt output.


Used for:

- data ready
- command completion
- events


Connection:



Si4684 IRQ

|

ESP32 GPIO interrupt



---

# 13.5 Si4684 Audio Interface


Digital output:



Si4684

BCLK
|
LRCLK
|
DATA

|

ADAU1467



Preferred:

- 24 bit audio
- 48kHz sample rate


---

# 13.6 Si4684 Firmware Management


Important design issue:


The Si4684 requires firmware loading.


The architecture includes:



SPI Flash

|

Si4684 firmware

|

ESP32-S3 loader



Startup sequence:



Power ON

|

ESP32 starts

|

Keep Si4684 reset

|

Load firmware

|

Release RESET

|

Initialize radio



---

# 13.7 Si4684 PCB Recommendations


RF section:


Must be physically separated from:

- DC/DC converters
- digital switching
- WiFi antenna


Recommended PCB placement:



+--------------------------+

RF AREA

Antenna
Matching
Si4684

DIGITAL AREA

ESP32
DSP
Power

+--------------------------+



---

# 13.8 Si4684 Design Risks


## Firmware availability

The firmware is proprietary.

The project must consider:

- legal firmware distribution
- firmware update method
- version control


The binary firmware shall be stored separately from source code.


---

## RF layout

The PCB RF layout is critical.

Must follow:

- antenna impedance rules
- controlled impedance traces
- ground plane continuity


---

# 13.9 Si4684 Summary


Role:

FM/DAB radio source.


Interface:

SPI + I2S.


Connection:


ESP32-S3

SPI

Si4684

I2S

ADAU1467



The Si4684 is considered a replaceable radio module.


(Fine Parte 2)


---

# 14. Analog Devices ADAU1467 Audio DSP


## 14.1 Overview


The ADAU1467 is the central digital audio processing unit of HubAudio.


It belongs to the Analog Devices SigmaDSP family and is designed for high quality audio processing applications.


The DSP is responsible for:


- audio routing
- equalization
- crossover filtering
- dynamic processing
- loudness compensation
- volume control
- delay management
- room correction algorithms


The ADAU1467 represents the central audio processing hub.


---

# 14.2 Audio Architecture


All digital audio sources converge into the ADAU1467.


                 AUDIO SOURCES


     Si4684          BT RX          Network Audio

        |              |                  |

        |              |                  |

        +--------------+------------------+

                       |

                      I2S

                       |

                  ADAU1467 DSP

                       |

          +------------+------------+

          |                         |

        DAC                    BT1035 TX


          |

     Power Amplifier


14.3 Why Use a Dedicated DSP

The ESP32-S3 is not suitable for high quality audio processing.

Reasons:

operating system tasks
WiFi interruptions
unpredictable timing
insufficient deterministic audio processing

The ADAU1467 provides:

deterministic processing
hardware audio engine
low latency
professional audio quality
14.4 ADAU1467 Main Interfaces

The DSP uses:

Function	Interface
Configuration	I2C / SPI
Program loading	SPI Flash
Audio input/output	I2S/TDM
Clock	MCLK
Reset	GPIO
14.5 ADAU1467 Power Supply

The ADAU1467 contains sensitive analog/digital sections.

Power domains must be carefully designed.

Recommended:


3.3V_AUDIO

       |

       +---- DSP Digital Supply

       |

       +---- DSP Analog Supply



Important:

The DSP supply must be separated from:

ESP32 WiFi supply
DC/DC switching nodes
Bluetooth RF supply
14.6 Decoupling Requirements

Standard decoupling:


VDD

 |

100nF ceramic

 |

1uF ceramic

 |

10uF bulk



Additional filtering is recommended:


3.3V

 |

Ferrite bead

 |

ADAU1467 supply


The ferrite bead is particularly important because DSP noise can couple into the audio path.

14.7 ADAU1467 Configuration Interface

The ESP32-S3 controls the DSP.

Preferred:

I2C Control

Connection:


ESP32-S3             ADAU1467


SDA ---------------- SDA

SCL ---------------- SCL



Used for:

volume
routing
parameter updates
runtime control
14.8 DSP Program Memory

The ADAU1467 does not permanently store the DSP program internally.

External SPI memory is required.

Architecture:


ESP32-S3


    |

    |

SPI Flash


    |

    |

ADAU1467



Startup sequence:


Power ON

 |

ESP32 starts

 |

Program ADAU1467 memory

 |

Verify checksum

 |

Enable audio processing


14.9 SPI Flash Programming Strategy

The ESP32-S3 shall be able to:

erase DSP memory
program new firmware
verify CRC
restore previous version

Possible update procedure:


Receive DSP image

        |

Disable ADAU1467

        |

Program SPI Flash

        |

Verify

        |

Restart DSP



This allows field firmware updates.

14.10 Audio Interface (I2S)

The ADAU1467 is the preferred audio clock master.

Recommended architecture:


                ADAU1467

                    |

          BCLK / LRCLK / MCLK

                    |

        +-----------+-----------+

        |                       |

     Si4684                 BT Modules



Advantages:

single clock domain
no asynchronous sample conversion
better audio stability
14.11 I2S Signals

Typical signals:

BCLK

Bit clock.

Carries the individual audio bits.

LRCLK

Word select clock.

Defines:

left channel
right channel
DATA

Serial audio data.

MCLK

Master clock.

Important:

Some audio devices require MCLK.

Others generate internal clocks.

Each module must be verified.

14.12 I2S Routing Problems

A critical design issue:

Multiple I2S sources cannot directly drive the same bus.

Wrong:


Si4684

     |

     +------------ I2S ------------ ADAU1467

BT RX

     |

     +------------ I2S ------------



Two masters conflict.

Correct:


Source modules

      |

      |

Dedicated inputs

      |

      |

ADAU1467



The ADAU1467 must provide multiple serial ports.

14.13 ADAU1467 Audio Ports

The DSP provides multiple serial interfaces.

Suggested allocation:

Port	Device
Serial Input 0	Si4684
Serial Input 1	BT RX
Serial Output 0	DAC
Serial Output 1	BT1035

This avoids external I2S multiplexers.

14.14 DSP Software

The SigmaDSP project shall contain:

routing matrix
equalizer
volume control
filters
crossover
protection algorithms

Example:


Input Selector

       |

Equalizer

       |

Dynamic Processing

       |

Volume

       |

Output Router


14.15 ADAU1467 Reset

Reset must be controlled.

Recommended:


ESP32 GPIO

      |

RESET

      |

10k Pull-up

      |

3.3V



Startup:


Hold RESET LOW

       |

Configure clocks

       |

Release RESET

       |

Load DSP program


14.16 ADAU1467 PCB Placement

The DSP should be placed:

close to audio connectors
away from ESP32 antenna
away from DC/DC converters

Recommended:


+-----------------------------+

RF AREA

Bluetooth
Si4684


-----------------------------


AUDIO AREA

ADAU1467
DAC


-----------------------------


DIGITAL AREA

ESP32-S3
Power


+-----------------------------+

14.17 ADAU1467 Design Risks
Clock synchronization

Must verify:

MCLK requirement
sample frequency compatibility
master/slave configuration
Firmware dependency

DSP algorithm is stored externally.

Need:

version management
backup image
checksum
Noise coupling

Avoid:

digital return currents through analog ground
switching regulator near DSP
long I2S traces
14.18 ADAU1467 Summary

Role:

Central audio processing engine.

Connections:


ESP32-S3

  |

I2C/SPI

  |

ADAU1467

  |

I2S/TDM

  |

Audio modules



The ADAU1467 defines the professional audio capability of HubAudio.


---

# 15. Bluetooth Audio Subsystem


## 15.1 Architecture Decision


The HubAudio platform intentionally separates Bluetooth reception and transmission.


The reason is reliability.


A single Bluetooth audio module capable of simultaneously handling:

- A2DP Sink
- A2DP Source
- independent Bluetooth links
- real-time audio routing


is not guaranteed in commercial modules.


Therefore the design uses two independent Bluetooth audio blocks.


Architecture:


             Bluetooth Subsystem


    Smartphone                 Headphones

         |                         ^

         |                         |

         v                         |

   BT RX MODULE              BT1035 TX

         |                         ^

         | I2S                     | I2S

         |                         |

         +-----------+-------------+

                     |

                  ADAU1467


Advantages:


- simultaneous operation
- independent firmware
- easier debugging
- modular replacement
- predictable audio routing


---

# 16. FSC-BT1035 Bluetooth Transmitter


## 16.1 Role in HubAudio


The FSC-BT1035 is used as Bluetooth Audio Transmitter.


Its function:



ADAU1467

|

I2S

|

FSC-BT1035

|

Bluetooth A2DP Source

|

Headphones / Speakers



---

# 16.2 Main Features


Typical capabilities:


- Bluetooth audio transmission
- A2DP Source
- AVRCP support
- digital audio interface
- UART configuration
- embedded antenna


The module handles:


- Bluetooth stack
- codec negotiation
- RF management


The ESP32-S3 does not process Bluetooth audio.


---

# 16.3 BT1035 Connections


Important signals:


## Power



3.3V

|

BT1035 VCC



The module requires:


- clean supply
- local decoupling
- RF isolation


Recommended:



3.3V

|

Ferrite bead

|

BT1035

|

100nF

|

10uF



---

## UART Control


Connection:



ESP32-S3 BT1035

TX ---------------- RX

RX ---------------- TX



Used for:


- configuration
- status
- debugging


---

## I2S Audio Input


The BT1035 receives digital audio from the DSP.



ADAU1467 BT1035

BCLK -------------- BCLK

LRCLK ------------- LRCLK

DATA -------------- DATA IN



Important:


The clock master/slave configuration must be verified.


Preferred:


ADAU1467 = clock master.


---

# 16.4 BT1035 Firmware Considerations


Commercial Bluetooth modules often contain vendor firmware.


Important:


Verify:


- A2DP Source enabled
- I2S input mode enabled
- codec selection
- sample rate support


The module configuration shall be stored separately from ESP32 firmware.


---

# 16.5 BT1035 Operating Modes


Normal operation:



Power ON

|

UART initialization

|

Configure audio interface

|

Start Bluetooth advertising

|

Connect headphones

|

Stream audio



---

# 17. Bluetooth RX Module


## 17.1 Requirements


The receiving module must provide:


Required:


- Bluetooth Classic
- A2DP Sink
- I2S output
- UART configuration


Optional:


- AVRCP
- BLE
- codec selection


---

# 17.2 Preferred Solution


A module based on:

- FSC-BT1026
- equivalent Bluetooth Audio Receiver


Architecture:



Smartphone

|

Bluetooth A2DP

|

BT RX Module

|

I2S

|

ADAU1467



---

# 17.3 BT RX Module Connections


## Power


Same philosophy:



3.3V

|

Filtering

|

BT RX Module



Bluetooth RF requires a clean supply.


---

## I2S Output


Connection:



BT RX ADAU1467

BCLK -----------> BCLK IN

LRCLK ----------> LRCLK IN

DATA -----------> DATA IN



---

## UART


Optional but recommended:



ESP32-S3 TX

 |

BT RX RX

ESP32-S3 RX

 |

BT RX TX



Used for:


- pairing control
- diagnostics
- configuration


---

# 17.4 Bluetooth RX Firmware Risks


The main risk is vendor configuration.


A module may support:


- A2DP Sink only

or:


- A2DP Sink + Source


The required mode must be confirmed before PCB release.


---

# 18. Alternative Bluetooth RX Using ESP32-WROOM-32


## 18.1 Overview


The ESP32-WROOM-32 contains Bluetooth Classic support.


Unlike ESP32-S3:


- Bluetooth Classic available
- A2DP Sink supported


Architecture:



Smartphone

|

Bluetooth A2DP

|

ESP32-WROOM-32

|

I2S

|

ADAU1467



---

# 18.2 Advantages


Advantages:


- complete firmware control
- open development environment
- easy debugging
- same ecosystem as ESP32-S3


---

# 18.3 Disadvantages


Compared with dedicated modules:


- more firmware work
- Bluetooth stack maintenance
- higher CPU load
- more software complexity


---

# 18.4 Recommended Use


ESP32-WROOM should be considered:


- development prototype
- experimental firmware
- future custom Bluetooth module


Not the first production choice.


---

# 19. Bluetooth Clock Management


Bluetooth audio introduces clock problems.


Different devices may have:


- different sample clocks
- different oscillator accuracy


The ADAU1467 should manage:


- routing
- resampling if required
- synchronization


Possible solutions:


## Solution A

All sources synchronized to DSP clock.


Preferred.


---

## Solution B

Asynchronous sample rate conversion.


Required if modules cannot operate as slaves.


---

# 20. Bluetooth PCB Layout


RF modules require:


- antenna clearance
- ground plane
- no copper under antenna area
- separation from switching regulators


Recommended:



+--------------------+

Bluetooth Antenna

 KEEP OUT AREA

Digital electronics

Power section

+--------------------+



---

# 21. Bluetooth Subsystem Summary


Final architecture:


             ESP32-S3

                |

      +---------+---------+

      |                   |

   BT RX              BT1035

 A2DP Sink          A2DP Source

      |                   |

      | I2S               | I2S

      +---------+---------+

                |

            ADAU1467


This provides:


- smartphone audio reception
- Bluetooth headphone transmission
- simultaneous operation
- modular replacement


---
# 22. Module Identification System


## 22.1 Purpose


HubAudio is designed as a modular platform.


Every external module must be automatically identifiable by the main controller.


The system uses:



24AA025E48T-I/OT



as module identification memory.


---

# 22.2 24AA025E48T Overview


The device provides:


- I2C EEPROM memory
- factory programmed unique MAC address
- unique module identification


The ESP32-S3 reads the EEPROM during startup.


---

# 22.3 EEPROM Connection


Typical connection:



ESP32-S3 24AA025E48T

3.3V ---------------- VCC

GND ----------------- GND

SDA ----------------- SDA

SCL ----------------- SCL



Required:


I2C pull-up resistors.


Typical value:



2.2k - 4.7k



depending on bus capacitance.


---

# 22.4 Module Identification Structure


Example:


EEPROM:



Address 00

Module Type

01 = Radio Si4684

02 = Bluetooth RX

03 = Bluetooth TX

04 = DSP

Address 10

Hardware Revision

Address 20

Serial Number

Address 30

Configuration Data



---

# 22.5 Startup Discovery


The ESP32-S3 performs:



Power ON

|

Initialize I2C

|

Scan module bus

|

Read EEPROM

|

Identify hardware

|

Load configuration

|

Initialize drivers



The firmware does not need to know the exact board revision.


---

# 23. External SPI Memories


## 23.1 Purpose


Several components require external firmware storage.


Examples:


- ADAU1467 DSP program
- Si4684 firmware
- future modules


---

# 23.2 General Architecture



ESP32-S3

|

SPI

|

External Flash

|

Target Device



The ESP32-S3 acts as programmer.


---

# 23.3 Firmware Update Procedure


General sequence:



Receive update package

    |

Validate checksum

    |

Disable target device

    |

Program Flash

    |

Verify

    |

Restart module



---

# 24. Power Architecture


## 24.1 Design Objective


The audio system contains:


- RF circuits
- digital processors
- sensitive analog sections


Power distribution is critical.


---

# 24.2 Recommended Power Domains



Main Input

  |

  +----------------+

  |

Digital 3.3V

  |

  + ESP32-S3

  + EEPROM


  |

  |

Audio 3.3V

  |

  + ADAU1467

  + DAC


  |

  |

RF 3.3V

  |

  + Si4684

  + Bluetooth


---

# 24.3 Separation Rules


Avoid:


- ESP32 WiFi current peaks disturbing audio
- DC/DC switching noise entering DSP supply
- RF noise coupling into analog paths


---

# 24.4 Recommended Filtering


For DSP:



3.3V

|

Ferrite bead

|

100nF

|

1uF

|

10uF

|

ADAU1467



For RF modules:



3.3V

|

Ferrite bead

|

RF module



---

# 24.5 Ground Strategy


Recommended:


Single PCB ground plane.


However:


Control return currents carefully.


Avoid:


- digital currents crossing analog audio paths
- switching regulator return under DSP


---

# 25. System Boot Sequence


Complete startup:



POWER ON

|

Power regulators stable

|

ESP32-S3 reset release

|

Read EEPROM modules

|

Keep audio devices disabled

|

Initialize Si4684

|

Initialize ADAU1467

|

Initialize Bluetooth modules

|

Configure audio routing

|

Enable audio outputs



---

# 26. Audio Routing Software Model


The firmware shall expose audio sources:


Example:



SOURCE_RADIO

SOURCE_BT_RX

SOURCE_NETWORK

SOURCE_EXTERNAL



The DSP routing layer decides:



Selected Source

   |

ADAU1467

   |

Outputs



---

# 27. PCB Placement Strategy


Recommended board organization:



+--------------------------------+

| |
| RF AREA |
| |
| Si4684 Bluetooth Modules |
| |



AUDIO AREA

ADAU1467 DAC


-------------------------------

DIGITAL AREA

ESP32-S3 Power

+--------------------------------+


---

# 28. PCB Critical Rules


## RF


Must verify:


- antenna clearance
- impedance control
- keep-out area
- connector placement


---

## I2S


Keep:


- short traces
- controlled routing
- common ground reference


Avoid:


- crossing noisy clocks


---

## SPI


For:


- Si4684
- firmware memories


Use:


- short traces
- avoid unnecessary vias


---

# 29. Initial Bill Of Materials (Architecture Level)


| Block | Component |
|-|-|
| Main MCU | ESP32-S3 |
| Radio | Si4684 |
| DSP | ADAU1467 |
| Bluetooth TX | FSC-BT1035 |
| Bluetooth RX | FSC-BT1026 or equivalent |
| Module ID | 24AA025E48T-I/OT |
| DSP memory | SPI Flash |
| Radio memory | SPI Flash |
| DAC | To be selected |
| Amplifier | To be selected |


---

# 30. Open Issues Before PCB Release


## Must verify


### ADAU1467

- exact DSP memory size
- SPI Flash type
- clock configuration
- serial port allocation


---

### Si4684

- firmware acquisition
- RF matching network
- antenna design


---

### Bluetooth


- BT1035 I2S mode
- BT RX module A2DP Sink capability
- codec support
- UART commands


---

### Power


- regulator selection
- current budget
- thermal analysis


---

# 31. Final Architecture


The final HubAudio platform:


                     ESP32-S3

                        |

    +-------------------+-------------------+

    |                   |                   |

  Si4684             BT RX              BT1035

 FM/DAB+           A2DP Sink          A2DP Source

    |                   |                   |

    +-------------------+-------------------+

                        |

                       I2S

                        |

                   ADAU1467

                        |

             +----------+----------+

             |                     |

            DAC              Bluetooth Output


             |

        Amplifier


---

# 32. Engineering Philosophy


HubAudio is designed as a scalable embedded audio platform.


The architecture follows these principles:


- digital audio path
- modular hardware
- replaceable subsystems
- independent firmware management
- explicit hardware identification
- professional DSP processing


The system can evolve without redesigning the complete platform.


---

# END OF DOCUMENT

Revision 0.1
