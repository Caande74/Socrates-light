# Dedupe-Regel

## När Dedupe Är Tillåten

Dedupe är bara tillåten när alla följande villkor är uppfyllda:

- posterna är språkliga dubletter
- posterna tillhör samma owner
- posterna ligger i samma tabell
- det finns en tydlig canonical post

## När Dedupe Inte Är Tillåten

Dedupe är inte tillåten när:

- formuleringarna ändrar operativ innebörd
- bredare processansvar blandas ihop med smalare kontaktansvar

## Hur Dedupe Görs

Dedupe ska göras konservativt och reversibelt:

- backup först
- verifiering först
- sätt `status='inactive'`
- lägg till spårbar tags-markering
- ingen delete i första läget

## Hur Det Valideras Efteråt

Efter dedupe ska följande kontrolleras:

- kontroll av status
- kontroll av retrieval-path
- kontroll att `inactive` inte kommer med i normal context retrieval
