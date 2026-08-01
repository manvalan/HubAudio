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

The SPI architecture is divided into independent functional domains.

The ESP32-S3 operates as the master of the system control SPI bus.

The ADAU1467 and Si4684 expose SPI slave interfaces for external
configuration and control.

The internal management of each device remains under the responsibility of
the device itself.

## Architecture

System control SPI domain:

            ESP32-S3

          SPI MASTER

              |
    +---------+---------+
    |                   |
 ADAU1467            Si4684

SPI SLAVE          SPI SLAVE

## ADAU1467 Configuration Domain

The ADAU1467 manages its own external configuration memory through its
internal SPI master interface.

          ADAU1467

        SPI MASTER

              |

          25AA1024

   DSP Program / Configuration Memory

The ESP32-S3 controls the ADAU1467 through the external SPI interface but
does not directly access the DSP configuration memory during normal
operation.

## Si4684 Firmware Domain

The Si4684 firmware loading and configuration process is managed through
commands exchanged on the external SPI control interface.

           ESP32-S3

        SPI MASTER

              |

           Si4684

              |

    Internal Firmware Loader

              |

         Internal RAM

The ESP32-S3 controls the initialization process but does not directly access
the internal operational memory of the Si4684.

## Consequences

### Positive

- Clear ownership of every SPI interface
- No bus contention between devices
- Reduced electrical loading
- Independent device initialization
- Easier debugging and validation

### Negative

- Multiple control interfaces are required
- Firmware update procedures must coordinate different device domains

## Rationale

The ESP32-S3 supervises the complete HubAudio system but does not replace the
internal controllers of specialized devices.

Each component remains responsible for its own functional domain.

The control plane and the audio plane remain architecturally separated.