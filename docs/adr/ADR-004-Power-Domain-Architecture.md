# ADR-004 – Power Domain Architecture

- **Status:** Accepted
- **Date:** 2026-08-02

# Context

HubAudio integra sottosistemi con caratteristiche elettriche molto differenti:

- elaborazione digitale (System Controller)
- DSP audio
- ricevitore radio
- Bluetooth
- codec audio
- periferiche di controllo

Una distribuzione tradizionale mediante un unico rail a 3.3 V comporterebbe la condivisione delle correnti impulsive tra dispositivi con requisiti completamente differenti, aumentando il rumore di alimentazione e rendendo più complesso il debug del sistema.

# Decision

L'architettura di alimentazione viene organizzata mediante **Power Domains**.

La distribuzione primaria genera due domini principali:

- **3V3_DIGITAL**
- **3V3_AUDIO**

Il dominio digitale alimenta esclusivamente la logica di controllo.

Il dominio audio alimenta esclusivamente i dispositivi appartenenti alla catena audio.

Ogni nuovo sottosistema dovrà appartenere ad un dominio chiaramente identificato.

La separazione dei domini rappresenta una scelta architetturale e non un dettaglio implementativo.

# Consequences

## Advantages

- riduzione del rumore tra domini
- migliore immunità EMI
- maggiore modularità
- possibilità di monitoraggio energetico
- semplificazione del power sequencing
- migliore manutenibilità

## Trade-offs

- incremento del numero di rail
- maggiore complessità dello schema
- maggiore attenzione richiesta durante il layout PCB