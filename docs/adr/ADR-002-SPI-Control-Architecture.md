# ADR-002: SPI Control Architecture

- Status: Accepted
- Date: 2026-08-01
- Decision Type: Hardware Architecture

## Context

HubAudio integrates multiple programmable devices requiring configuration,
control and firmware management.

The main devices involved are:

- ESP32-S3 system controller
- ADAU1467 audio processor
- Si4684 radio receiver

A clear separation between system control and internal device management is
required.

The SPI interface is used exclusively as a control interface and not as an
audio transport interface.

## Decision

The SPI architecture is divided into independent domains.

The ESP32-S3 operates as the master of the system control SPI bus.

The ADAU1467 and Si4684 expose SPI slave interfaces for external configuration.

Each device maintains its own internal SPI master domain for accessing local
memories or peripherals.

## Architecture

System control bus:

            ESP32-S3

          SPI MASTER

              |
    +---------+---------+
    |                   |
 ADAU1467            Si4684

SPI SLAVE          SPI SLAVE


ADAU1467 local memory:

          ADAU1467

        SPI MASTER

              |

          25AA1024
      DSP Configuration Memory


Si4684 local memory:

           Si4684

        SPI MASTER

              |

      Firmware Memory


## Consequences

### Positive

- Clear ownership of every SPI bus
- Reduced electrical loading
- Independent firmware management
- Easier debugging

### Negative

- Multiple SPI peripherals are required
- Firmware coordination is required between domains

## Rationale

The ESP32-S3 supervises the system but does not replace the internal
controllers of specialized devices.

Each component remains responsible for its own functional domain.