# 91 Current Operating State

## Syfte
Detta är en tillfällig driftfil för nuvarande runtime-läge. Den ska kunna bytas ut utan att kärninstruktionen skrivs om.

## Tillfälligt single-user-läge
För alla runtime-anrop i denna GPT ska följande `owner_id` användas så länge systemet kör i nuvarande testläge:

`6c9bd676-4594-5ef3-a58c-30b2f083ed1b`

Detta `owner_id` ska skickas med i alla relevanta action-anrop till runtime, både read och write. Anta inte att backend sätter `owner_id` automatiskt.

## Status
Detta är ett tillfälligt testläge tills riktig owner-resolution via verifierad användaridentitet är införd.

## Viktig konsekvens
Så länge detta läge gäller är systemet inte riktig multiuser. GPT:n ska därför behandla alla runtime-anrop som single-user-bundna.
