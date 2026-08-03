# ADR-003: I2S Audio Routing Architecture

- Status: Accepted
- Date: 2026-08-01
- Decision Type: Audio Architecture

## Context

HubAudio integrates multiple digital audio sources and destinations:

Sources:

- System Controller streaming subsystem
- Radio Receiver radio receiver
- Bluetooth receiver
- Optical digital input

Destinations:

- Analog audio output through CODEC/DAC
- Bluetooth transmission
- Optical digital output

A deterministic and scalable digital audio routing architecture is required.

## Decision

The Audio Processor is the central routing element of the Audio Domain.

Each major audio device is assigned to a dedicated serial audio interface.

The preferred architecture is:


One audio device = One dedicated I2S interface


The Audio Processor operates as the audio timing reference.

External audio devices operate as I2S slaves whenever supported.

## Audio Input Allocation

|| Audio Processor Input | Device | Function |
|---|---|---|
| SDATA_IN0 | System Controller | Network audio stream |
| SDATA_IN1 | Radio Receiver | Radio audio |
| SPDIFIN | Optical Interface | Optical digital audio input |
| SDATA_IN2 | Bluetooth RX | Wireless audio input |

The ADAU1467 internal audio routing matrix allows any digital audio input
to be routed to the DSP core, ASRCs, serial outputs or SPDIF output.

System Controller --------
Radio Receiver ---------
DECODEC ----------+---- Audio Processor
BT RX ---------/


## Audio Output Allocation

## Audio Output Allocation

| Audio Processor Output | Device | Function |
|---|---|---|
| SDATA_OUT0 | CODEC/DAC | Analog audio output |
| SDATA_OUT1 | Bluetooth TX | Wireless audio output |
| SPDIFOUT | Optical Interface | Optical digital audio output |
| SDATA_OUT3 | Reserved | Future expansion |

             Audio Processor

                 |
    +------------+------------+
    |            |            |
  CODEC        BTTX       ENCODEC

## Clocking

The Audio Processor provides the master audio timing reference.

The audio clock domain consists of:

- MCLK
- BCLK
- LRCLK

All connected audio peripherals must operate synchronized to this clock
domain.

## Consequences

### Positive

- Deterministic audio timing
- Simple routing model
- Independent audio channels
- Easier debugging
- Future expansion capability

### Negative

- Higher pin usage
- More PCB routing resources required
- Peripheral selection must consider I2S slave capability

## Rationale

HubAudio prioritizes signal integrity, maintainability and deterministic
audio behavior over maximum bus utilization.

The Audio Processor acts as the central audio router of the system.