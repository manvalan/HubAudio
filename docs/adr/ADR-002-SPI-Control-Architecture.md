# ADR-002: SPI Control Architecture

- Status: Accepted
- Date: 2026-08-01
- Decision Type: Hardware Architecture

## Context

HubAudio integrates multiple programmable devices requiring configuration,
control and firmware management.

The main devices involved are:

- System Controller system controller
- Audio Processor audio processor
- Radio Receiver radio receiver

A clear separation between system control and internal device management is
required.

The SPI interface is used exclusively as a control interface and not as an
audio transport interface.

## Decision

The SPI architecture is divided into independent control domains.

The System Controller operates as the master of the system control SPI bus.

The Audio Processor and Radio Receiver expose SPI slave interfaces for external
configuration and control.

The internal management of each device remains under the responsibility of
the device itself.

## Architecture

System control SPI domain:

            System Controller

          SPI MASTER

              |
    +---------+---------+
    |                   |
 Audio Processor            Radio Receiver

SPI SLAVE          SPI SLAVE

## Audio Processor Configuration Domain

The Audio Processor manages its own external configuration memory through its
internal SPI master interface.

          Audio Processor

        SPI MASTER

              |

          Audio EEPROM

   DSP Program / Configuration Memory

The System Controller controls the Audio Processor through the external SPI interface but
does not directly access the DSP configuration memory during normal
operation.

## Radio Receiver Firmware Domain

The Radio Receiver firmware loading and configuration process is managed through
commands exchanged on the external SPI control interface.

           System Controller

        SPI MASTER

              |

           Radio Receiver

              |

    Internal Firmware Loader

              |

         Internal RAM

The System Controller supervises the Radio Receiver initialization process. Internal firmware loading remains under the responsibility of the Radio Receiver boot architecture.

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

The System Controller supervises the complete HubAudio system but does not replace the
internal controllers of specialized devices.

Each component remains responsible for its own functional domain.

The control plane and the audio plane remain architecturally separated.