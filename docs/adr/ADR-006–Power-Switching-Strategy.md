# ADR-006 – Power Switching Strategy

- **Status:** Accepted
- **Date:** YYYY-MM-DD

# Context

HubAudio è progettato come piattaforma modulare.

I sottosistemi possono essere utilizzati singolarmente oppure contemporaneamente.

La possibilità di controllare dinamicamente l'alimentazione costituisce un requisito fondamentale.

# Decision

Ogni dominio audio viene alimentato attraverso un Load Switch dedicato.

Il firmware controlla direttamente i Load Switch mediante GPIO.

I domini possono essere:

- abilitati
- disabilitati
- riavviati
- sequenziati

Il firmware implementa la sequenza di accensione e spegnimento del sistema.

# Consequences

## Advantages

- riduzione dei consumi
- riavvio selettivo dei dispositivi
- migliore gestione degli errori
- possibilità di future modalità operative
- migliore diagnostica

## Trade-offs

- firmware leggermente più complesso
- gestione delle temporizzazioni di accensione