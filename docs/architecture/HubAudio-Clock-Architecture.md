# HubAudio Clock Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: Architecture Specification


# 1. Overview

The HubAudio architecture defines a centralized audio timing domain.

The Audio Processor is the master of the audio clock system.

The purpose of this architecture is to provide a single timing reference for
all digital audio devices, avoiding independent clock domains and minimizing
sample synchronization problems.

The audio clock domain is composed of:

- Master oscillator
- Audio Processor PLL and clock generation
- Clock distribution stage
- Audio peripheral clock inputs


---

# 2. Audio Clock Master

The Audio Processor is responsible for generating the audio timing reference.

The Audio Processor provides:

- DSP processing clock
- Serial audio clock generation
- I2S synchronization


Conceptually:

          Reference Clock

                |
                |

           Audio Processor

      DSP + Audio Clock Master

                |

         MCLK / BCLK / LRCLK

The Audio Processor is the timing authority of the Audio Domain.


---

# 3. Reference Frequency

The preferred audio clock family is based on 48 kHz.

The standard relationship is:


48 kHz × 256 = 12.288 MHz


The reference oscillator is therefore selected around:


12.288 MHz


This frequency is suitable for:

- streaming audio
- DAB/DAB+
- Bluetooth audio
- consumer digital audio systems


Future support for 44.1 kHz family may require:

- alternate oscillator
- PLL reconfiguration
- ASRC usage


---

# 4. Clock Distribution

The Audio Processor clock output is distributed through a dedicated clock buffer.

The Clock Buffer is used as clock distribution element.

Its role is:

- fan-out of the clock signal
- reduction of clock loading
- improved signal integrity


It does not generate the audio clock.


Architecture:

                Audio Processor

             Audio Clock Master

                   |

                  MCLK

                   |

            Clock Buffer

          Clock Distribution

      +------------+------------+
      |            |            |
      |            |            |

   Radio Receiver       BT Modules    CODEC

---

# 5. Clock Domain Devices

All digital audio peripherals belong to the same clock domain.

Expected clock relationships:

             Audio Processor

                |

    +-----------+-----------+
    |
 MCLK/BCLK/LRCLK

    |

+------+------+------+------+
| | | |
ESP32 Radio Receiver BT RX CODEC



Each device must support operation as:

- I2S slave
- external MCLK
- externally provided BCLK/LRCLK


---

# 6. Clock and Audio Data Relationship

The audio data flow is independent from control communication.

Control:


System Controller

|
|

SPI

|

Audio Processor / Radio Receiver



Audio:


Source Device

  |
  |
 I2S

  |
  |

Audio Processor


Timing:


Audio Processor

  |
  |

Clock Signals

  |
  |

Audio Peripherals



---

# 7. Design Rules

The following rules apply to the PCB:

## Clock Routing

- Clock lines must be short
- Clock return path must be continuous
- Avoid routing near RF sections
- Avoid unnecessary vias


## Power Integrity

The clock generator and buffer require:

- clean supply rails
- adequate decoupling
- low noise power domains


## Grounding

Clock signals must always reference a continuous ground plane.


---

# 8. Architectural Consequences

## Advantages

- Single audio timing reference
- No asynchronous sample drift
- Simplified DSP routing
- Professional audio architecture


## Limitations

- All peripherals must support external clocking
- Clock tree becomes a critical design element
- PCB layout quality directly affects audio performance


---

# 9. Design Philosophy

The HubAudio clock architecture follows the same principle as a musical
orchestra:

The Audio Processor is the conductor.

The Clock Buffer distributes the beat.

All audio devices perform synchronized to the same timing reference.