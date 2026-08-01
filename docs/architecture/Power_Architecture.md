# docs/architecture/Power_Architecture.md

# Power Architecture

## Overview

HubAudio adotta un'architettura di alimentazione basata su **Power Domains** indipendenti anziché su una semplice distribuzione delle tensioni.

L'obiettivo è ottenere:

- isolamento tra domini digitali e audio;
- riduzione delle interferenze EMI;
- possibilità di power sequencing;
- monitoraggio energetico;
- elevata modularità.

L'intera distribuzione dell'alimentazione è organizzata come una gerarchia di domini funzionali.

```
                VIN
                 │
          Primary Buck 3.3V
                 │
        ┌────────┴────────┐
        │                 │
   3V3_DIGITAL      3V3_AUDIO_RAW
                          │
                     π Filter
                          │
                      INA226
                          │
                     3V3_AUDIO
```

---

## Digital Power Domain

Il dominio digitale alimenta esclusivamente i componenti di controllo.

Comprende:

- ESP32-S3
- EEPROM
- GPIO Expander
- Display
- Bus I²C
- Logica digitale

Questo dominio è distribuito tramite un poligono dedicato sul layer di alimentazione.

---

## Audio Power Domain

Il dominio audio deriva direttamente dal convertitore principale ma viene completamente isolato tramite:

- filtro π
- monitor INA226
- distribuzione dedicata

Il dominio audio alimenta esclusivamente i dispositivi audio.

Ogni IC riceve successivamente un'alimentazione dedicata mediante un proprio Power Switch.

---

## Design Philosophy

HubAudio considera ogni sottosistema come un dominio energetico indipendente.

Ogni dominio deve poter essere:

- acceso
- spento
- monitorato
- riavviato

senza influenzare gli altri.