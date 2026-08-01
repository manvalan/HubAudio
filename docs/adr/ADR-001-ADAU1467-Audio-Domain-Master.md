# ADR-001: ADAU1467 as Audio Domain Master

- Status: Accepted
- Date: 2026-08-01
- Decision Type: Architecture

## Context

HubAudio is designed as a modular digital audio platform integrating several
audio sources and destinations:

- ESP32-S3 streaming subsystem
- Si4684 radio receiver
- Bluetooth RX/TX modules
- Digital audio converters
- Analog CODEC/DAC stages

The system requires a central component responsible for:

- digital audio routing
- DSP processing
- timing synchronization
- audio stream management

The ADAU1467 has been selected as the central audio processor.

## Decision

The ADAU1467 is the master component of the HubAudio Audio Domain.

The ADAU1467 is responsible for:

- DSP processing
- audio routing
- digital mixing
- signal processing
- audio clock generation
- synchronization of external audio peripherals

The ADAU1467 is considered the audio domain master.

The ESP32-S3 participates in the Audio Domain as a digital audio source. It does not act as the audio timing master or routing controller. Its role inside the audio domain is equivalent to other digital audio sources.
The ESP32-S3 has a dual role:

- audio source inside the Audio Domain
system supervisor inside the Control Domain

It operates as system supervisor and is responsible for:

- network connectivity
- user interface
- configuration management
- firmware update management
- system control

## Consequences

### Positive

- Single audio timing reference
- Deterministic audio routing
- Reduced clock synchronization complexity
- Easier debugging and expansion
- Clear separation between control domain and audio domain

### Negative

- External audio devices must support slave clock operation
- Clock distribution becomes a critical design element
- Peripheral selection must consider I2S synchronization requirements

## Rationale

The ADAU1467 is selected not only as a DSP processor but as the central
controller of the digital audio domain.

This decision defines the HubAudio architecture.
