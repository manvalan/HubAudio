# HubAudio I2S Audio Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: Architecture Specification


# 1. Overview

The HubAudio audio architecture is based on a centralized digital audio
processing model.

The ADAU1467 is the core audio processor and manages:

- digital audio routing
- DSP processing
- mixing
- synchronization
- audio stream conversion

All digital audio streams are connected to the ADAU1467 through serial audio
interfaces.

The audio domain is independent from the system control domain.


CONTROL DOMAIN

ESP32-S3
|
|
SPI
|
Configuration

AUDIO DOMAIN

ESP32-S3
Si4684
BT RX
Optical Input

  |
  |
  v

ADAU1467

  |
  |

CODEC
BT TX
Optical Output


---

# 2. Audio Clock Master

The ADAU1467 is the master of the audio timing domain.

The generated audio clock consists of:

- MCLK
- BCLK
- LRCLK


All external audio devices should operate as synchronized slaves whenever
supported.

             ADAU1467

          AUDIO CLOCK MASTER

                |
      +---------+---------+
      |
    MCLK/BCLK/LRCLK

                |
   +------------+------------+
   |            |            |
 Si4684       BT RX       CODEC

---

# 3. Input Audio Interfaces

The ADAU1467 provides multiple serial input ports.

The HubAudio input allocation is:

| ADAU Port | Source | Description |
|-----------|--------|-------------|
| SDATA_IN0 | ESP32-S3 | Network audio stream |
| SDATA_IN1 | Si4684 | Radio receiver audio |
| SDATA_IN2 | DECODEC | Optical digital input |
| SDATA_IN3 | Bluetooth RX | Wireless audio input |


## ESP32-S3 Audio Input

The ESP32-S3 acts as a digital audio source.

Its role inside the Audio Domain is equivalent to any other audio source.


ESP32-S3

I2S DATA OUT
|
|
v

ADAU1467 SDATA_IN0


The ESP32-S3 does not control the audio timing.

The timing is provided by the ADAU1467 clock domain.


---

## Si4684 Audio Input

The Si4684 provides decoded radio audio.


Si4684

I2S DATA OUT
|
|
v

ADAU1467 SDATA_IN1


The Si4684 is a peripheral of the audio domain.

It does not define the system audio clock.


---

## Optical Digital Input

The optical input path is:


SPDIF Optical

  |
  |

DECODEC

  |
  |

I2S

  |
  |

ADAU1467 SDATA_IN2


The decoder must support operation synchronized with the HubAudio clock
architecture or provide an appropriate conversion stage.


---

## Bluetooth RX Input

The Bluetooth receiver provides digital audio:


Bluetooth RX

  |
  |

I2S

  |
  |

ADAU1467 SDATA_IN3


The selected Bluetooth module must support external audio clock operation.


---

# 4. Output Audio Interfaces

The ADAU1467 output allocation is:

| ADAU Port | Destination | Description |
|-----------|-------------|-------------|
| SDATA_OUT0 | CODEC/DAC | Analog audio output |
| SDATA_OUT1 | Bluetooth TX | Wireless transmission |
| SDATA_OUT2 | ENCODEC | Optical digital output |
| SDATA_OUT3 | Reserved | Future expansion |


## Analog Audio Output


ADAU1467

SDATA_OUT0

  |

CODEC / DAC

  |

Analog Output



---

## Bluetooth Transmission Output


ADAU1467

SDATA_OUT1

  |

Bluetooth TX

  |

Wireless Audio



---

## Optical Digital Output


ADAU1467

SDATA_OUT2

  |

ENCODEC

  |

SPDIF Optical Output



---

# 5. I2S Versus TDM Strategy

The ADAU1467 supports multiple serial audio formats including:

- I2S
- Left Justified
- Right Justified
- TDM


The initial HubAudio architecture uses dedicated I2S interfaces.

Advantages:

- simple routing
- easier debugging
- independent peripherals
- reduced firmware complexity


TDM remains an option for future expansion where multiple channels must share
a single physical interface.

The current design prioritizes clarity and robustness.


---

# 6. Signal Integrity Requirements

The following signals are considered critical:

- MCLK
- BCLK
- LRCLK
- SDATA


PCB design considerations:

- controlled return paths
- continuous ground reference
- short clock routes
- separation from RF sections
- controlled impedance where required


---

# 7. Future Expansion

The architecture reserves:

- additional serial output capability
- additional digital inputs
- TDM expansion possibilities


The ADAU1467 remains the central audio routing element for future HubAudio
versions.