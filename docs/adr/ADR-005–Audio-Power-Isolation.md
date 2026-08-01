# ADR-005 – Audio Power Isolation

- **Status:** Accepted
- **Date:** YYYY-MM-DD

# Context

Il dominio audio comprende dispositivi con elevata sensibilità ai disturbi di alimentazione.

Condividere la medesima alimentazione tra DSP, ricevitore radio, codec e modulo Bluetooth aumenterebbe la probabilità di accoppiamenti indesiderati.

# Decision

Ogni Integrated Circuit appartenente al dominio audio dispone di un proprio ramo di alimentazione indipendente.

Ogni ramo segue la seguente topologia:

3V3_AUDIO
↓

TPS22918

↓

Ferrite Bead

↓

Condensatori locali

↓

Integrated Circuit

Il Power Switch permette il controllo indipendente del dominio.

La ferrite realizza l'isolamento ad alta frequenza.

I condensatori locali garantiscono il corretto bypass del dispositivo.

# Consequences

## Advantages

- isolamento reciproco dei dispositivi
- riduzione delle interferenze
- possibilità di riavvio del singolo componente
- power sequencing
- minore propagazione del rumore

## Trade-offs

- aumento del numero di componenti
- incremento dell'area PCB