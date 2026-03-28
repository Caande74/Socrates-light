# NEXT STEP

## Nästa konkreta steg
Lifecycle v1.5 är nu användbar med Batch 1 och Batch 2.
Nästa konkreta steg är att uttryckligen deferera Batch 3 till ett separat steg.

## Mål
Lägg till återstående status-PATCH för:
- decisions
- adjustments
- patterns

## Önskad effekt
Lifecycle-stöd ska vara konsekvent över alla primära memory-typer utan att ändra datamodellen mer än nödvändigt.
Samtidigt ska aktuell runtime väga tyngre än tidigare trådsyntes när GPT läser ny kontext.

## När detta är klart
Nästa steg efter det är:
1. förbättra relation expansion till full objekt-expansion
2. börja använda learning-objekten mer aktivt i runtime-logiken
3. därefter förbereda GPT Action-koppling

## Arbetsregel
Jobba vidare steg för steg.
Ändra så få filer som möjligt per steg.
Verifiera varje steg med curl innan nästa ändring.
