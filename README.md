# HubAudio

## Professional Embedded Audio Platform

HubAudio is a modular embedded audio platform designed around a clear separation of hardware domains:

- System control
- Audio processing
- Digital radio
- Wireless audio
- Clock management
- Power management

The primary design objective is maintainability.

The architecture follows the principle:

> Code and hardware design must fit in the engineer's head.

Complexity is introduced only when it provides a measurable improvement in reliability, flexibility or performance.

---

# Project Goals

HubAudio is intended to provide:

- High quality digital audio routing
- Multiple audio sources and destinations
- Expandable DSP processing
- Robust embedded operation
- Professional PCB architecture
- Long-term maintainability

---

# Core Architecture

## Main Domains

                SYSTEM DOMAIN

                ESP32-S3
                   |
          Control / Network / UI
                   |
                   |
            AUDIO CONTROL BUS


                AUDIO DOMAIN

               ADAU1467

    +-------------+-------------+
    |             |             |
  I2S          SPDIF        Bluetooth
    |             |             |
Si4684        IO Codec      BT Module
 Radio

---

# Hardware Philosophy

The system is divided into independent domains:

## System Domain

Responsible for:

- Connectivity
- User interface
- Configuration
- Network services
- OTA updates

Main component:

- ESP32-S3


## Audio Domain

Responsible for:

- Routing
- DSP processing
- Mixing
- Sample rate management

Main component:

- Analog Devices ADAU1467


## RF Domain

Responsible for:

- Digital radio reception
- Wireless communication


## Power Domain

Responsible for:

- Battery operation
- USB power
- Voltage regulation
- Monitoring


---

# Repository Structure


HubAudio/

├── docs/
│
├── hardware/
│
├── firmware/
│
├── simulation/
│
├── research/
│
└── tools/


---

# Design Rules

1. Prefer simple architectures.
2. Avoid unnecessary abstraction.
3. Separate noisy and sensitive domains.
4. Document every architectural decision.
5. Choose components for lifecycle, not only price.

---

# Status

Architecture phase.

Hardware implementation follows documented decisions.