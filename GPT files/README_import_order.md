# Paket för ny GPT-struktur

Detta paket innehåller:
- `Instructions.md` – ny kort huvudinstruktion
- `knowledge/` – ny uppdelad knowledge-struktur

## Rekommenderad importordning
1. Lägg in innehållet i `Instructions.md` som GPT Instructions.
2. Ladda upp samtliga filer i `knowledge/` som knowledge.
3. Om du vill börja minimalt kan du först ladda upp:
   - 01_operating_model.md
   - 02_principal_model.md
   - 04_governance_and_approval_rules.md
   - 05_memory_model_and_retention.md
   - 10_roles_core.md
   - 11_routing_and_mode_selection.md
   - 12_house_style_and_communication.md
4. Lägg sedan till mode-filer, mallar, triggers och tekniska runtime-filer.

## Designprincip
- Instructions bär bara det som måste vara aktivt hela tiden.
- Knowledge bär policy, routing, roller, modes, mallar och tekniska specialregler.
- Tekniska runtime-regler och tillfälligt driftläge ligger separat så att de kan ändras utan att kärnbeteendet skrivs om.
