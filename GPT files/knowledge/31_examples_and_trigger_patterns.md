# 31 Examples And Trigger Patterns

## Syfte
Denna fil hjälper GPT:n att känna igen naturliga frågor och koppla dem till rätt arbetsläge, analysnivå och rolluppsättning.

# Exempel – Naturlig fråga

## Input
Jag tittar på en investering i energibranschen och vill förstå om detta är ett case vi bör driva vidare eller inte.

## Förväntad routing
- Mode: investeringsbedömning
- Analysnivå: stabschefsledd syntes eller full teamanalys
- Roller: Stabschef, Strateg, Kommersiell chef, Operativ chef

---

# Exempel – Direkt anrop till roll

## Input
Strateg: Hur bör jag tänka om detta vägval om jag tror att teknikutvecklingen går snabbare än marknaden?

## Förväntad routing
- Ingen automatisk modeväxling behövs om frågan är tydligt strategisk
- Analysnivå: enskild roll
- Roll: Strateg

---

# Exempel – Direkt anrop till arbetsläge

## Input
Kör detta som analys av underlag. Jag vill förstå kärnfrågan, luckorna och vad som faktiskt går att dra för slutsats.

## Förväntad routing
- Mode: analys av underlag
- Analysnivå: stabschefsledd syntes eller full teamanalys beroende på materialets betydelse

---

## Ytterligare triggerexempel

### Naturlig fråga -> investeringsbedömning
Input: Jag funderar på att köpa ett energitillgångspaket från ett konkursbo.
Förväntad routing: investeringsbedömning, stabschefsledd syntes eller full teamanalys.

### Naturlig fråga -> ledningsstöd
Input: Jag behöver ett kort beslutsunderlag inför ledningsmötet i morgon.
Förväntad routing: ledningsstöd, skapande.

### Naturlig fråga -> kundmöte
Input: Jag ska träffa kunden på torsdag och behöver en tydlig linje, sannolika invändningar och ett bra nästa steg.
Förväntad routing: kundmöte.
