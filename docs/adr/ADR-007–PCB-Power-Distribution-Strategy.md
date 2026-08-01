# ADR-007 – PCB Power Distribution Strategy

- Status: Accepted

# Context

La distribuzione dell'alimentazione su un PCB multistrato influenza direttamente:

- rumore
- EMI
- stabilità
- integrità del segnale

# Decision

Il PCB utilizza uno stack-up a quattro layer.

Il layer di alimentazione non è costituito da un unico piano.

Viene realizzato:

- un poligono dedicato al dominio 3V3_DIGITAL;

- piste dedicate per tutti i domini audio.

Ogni dominio audio viene distribuito individualmente fino al rispettivo dispositivo.

Non vengono creati piani condivisi per il dominio audio.

# Rationale

Questa soluzione:

- riduce le correnti condivise;
- migliora l'isolamento;
- facilita il debug;
- semplifica l'espansione futura della piattaforma.

# Consequences

Il layout richiede una pianificazione accurata della distribuzione delle alimentazioni ma garantisce una maggiore robustezza dell'intero sistema.