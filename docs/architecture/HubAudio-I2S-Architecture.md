# HubAudio I2S Audio Architecture

- Status: Draft
- Date: 2026-08-01
- Document Type: Architecture Specification


# 1. Overview

The HubAudio audio architecture is based on a centralized digital audio
processing model.

The Audio Processor is the core audio processor and manages:

- digital audio routing
- DSP processing
- mixing
- synchronization
- audio stream conversion

All digital audio streams are connected to the Audio Processor through serial audio
interfaces.

The audio domain is independent from the system control domain.


CONTROL DOMAIN

System Controller
|
|
SPI
|
Configuration

AUDIO DOMAIN

System Controller
Radio Receiver
BT RX
Optical Input

  |
  |
  v

Audio Processor

  |
  |

CODEC
BT TX
Optical Output


---

# 2. Audio Clock Master

The Audio Processor is the master of the audio timing domain.

The generated audio clock consists of:

- MCLK
- BCLK
- LRCLK


All external audio devices should operate as synchronized slaves whenever
supported.

             Audio Processor

          AUDIO CLOCK MASTER

                |
      +---------+---------+
      |
    MCLK/BCLK/LRCLK

                |
   +------------+------------+
   |            |            |
 Radio Receiver       BT RX       CODEC

---

# 3. Input Audio Interfaces

The Audio Processor provides multiple serial input ports.

The HubAudio input allocation is:

| ADAU Port | Source | Description |
|-----------|--------|-------------|
| SDATA_IN0 | System Controller | Network audio stream |
| SDATA_IN1 | Radio Receiver | Radio receiver audio |
| SDATA_IN2 | DECODEC | Optical digital input |
| SDATA_IN3 | Bluetooth RX | Wireless audio input |


## System Controller Audio Input

The System Controller acts as a digital audio source.

Its role inside the Audio Domain is equivalent to any other audio source.


System Controller

I2S DATA OUT
|
|
v

Audio Processor SDATA_IN0


The System Controller does not control the audio timing.

The timing is provided by the Audio Processor clock domain.


---

## Radio Receiver Audio Input

The Radio Receiver provides decoded radio audio.


Radio Receiver

I2S DATA OUT
|
|
v

Audio Processor SDATA_IN1


The Radio Receiver is a peripheral of the audio domain.

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

Audio Processor SDATA_IN2


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

Audio Processor SDATA_IN3


The selected Bluetooth module must support external audio clock operation.


---

# 4. Output Audio Interfaces

The Audio Processor output allocation is:

| ADAU Port | Destination | Description |
|-----------|-------------|-------------|
| SDATA_OUT0 | CODEC/DAC | Analog audio output |
| SDATA_OUT1 | Bluetooth TX | Wireless transmission |
| SDATA_OUT2 | ENCODEC | Optical digital output |
| SDATA_OUT3 | Reserved | Future expansion |


## Analog Audio Output


Audio Processor

SDATA_OUT0

  |

CODEC / DAC

  |

Analog Output



---

## Bluetooth Transmission Output


Audio Processor

SDATA_OUT1

  |

Bluetooth TX

  |

Wireless Audio



---

## Optical Digital Output


Audio Processor

SDATA_OUT2

  |

ENCODEC

  |

SPDIF Optical Output



---

# 5. I2S Versus TDM Strategy

The Audio Processor supports multiple serial audio formats including:

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


The Audio Processor remains the central audio routing element for future HubAudio
versions.