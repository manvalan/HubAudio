# docs/architecture/PCB_Stackup.md

# PCB Stack-up

## Layer Structure

HubAudio utilizza un PCB a quattro layer.

```
Layer 1
Top
Components + Signals

Layer 2
Continuous Ground Plane

Layer 3
Power Distribution

Layer 4
Bottom Signals
```

---

## Ground Plane

Il secondo layer è un piano GND continuo.

Non vengono create interruzioni.

Il piano di massa costituisce il riferimento comune per:

- segnali
- alimentazioni
- ritorni di corrente
- impedenza controllata

---

## Power Layer

Il layer di alimentazione non è costituito da un unico piano.

Sono presenti:

- un poligono dedicato al dominio digitale;
- piste dedicate ai domini audio.

```
Inner2

+-------------------------------+

 3V3_DIGITAL
 ███████████████████████████

        │

        ├─────────────► 3V3_ADAU

        ├─────────────► 3V3_SI4684

        ├─────────────► 3V3_BT

        ├─────────────► 1V8_ADAU

        └─────────────► 1V2_ADAU
```

---

## Routing Philosophy

Il dominio digitale utilizza un poligono dedicato.

Le alimentazioni audio vengono distribuite tramite piste dedicate.

Questa scelta:

- riduce il rumore condiviso;
- limita le correnti impulsive;
- semplifica il controllo EMI;
- migliora la leggibilità del layout.

---

## Local Decoupling

Ogni IC dispone di:

- condensatori di bypass locali;
- ferrite dedicata;
- power switch dedicato.

La distribuzione dell'alimentazione è quindi gerarchica e non condivisa.