# docs/architecture/Power_Domains.md

# Power Domains

## Overview

Ogni Integrated Circuit appartenente al dominio audio possiede un'alimentazione dedicata.

La distribuzione segue sempre la stessa topologia.

```
3V3_AUDIO
     │
 TPS22918
     │
 Ferrite
     │
10µF
1µF
100nF
     │
Audio IC
```

Questa architettura permette:

- isolamento elettrico
- riduzione del rumore
- power sequencing
- diagnostica

---

# ADAU1467 Domain

```
3V3_AUDIO
      │
 TPS22918
      │
 Ferrite
      │
 AVDD / PVDD
```

Le tensioni locali vengono generate mediante LDO dedicati.

```
3V3_ADAU
      │
 TPS7A2018
      │
 1V8_ADAU
```

```
3V3_ADAU
      │
 TPS7A2012
      │
 1V2_ADAU
```

---

# Si4684 Domain

```
3V3_AUDIO
      │
 TPS22918
      │
 Ferrite
      │
 Si4684
```

---

# Bluetooth Domain

```
3V3_AUDIO
      │
 TPS22918
      │
 Ferrite
      │
 Bluetooth Module
```

---

# Future Domains

L'architettura permette di aggiungere ulteriori domini senza modificare quelli esistenti.

Esempi:

- DAC
- ADC
- SPDIF
- HDMI Audio
- DSP aggiuntivi

Ogni nuovo dominio segue la medesima struttura.