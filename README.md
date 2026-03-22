# Unified Runtime API v1 Scaffold

Detta är ett första tekniskt scaffold för runtime-lagret bakom AI-ledningsteamet.

## Mål med scaffoldet
- ge en ren repo-struktur
- få FastAPI, databas och API-yta på plats
- göra det lätt att börja implementera stegvis
- ge en OpenAPI-bas för GPT Actions

## Första körning
1. Skapa virtuell miljö
2. Installera dependencies från `requirements.txt`
3. Kopiera `.env.example` till `.env`
4. Starta appen med uvicorn
5. Verifiera `/health`

## Prioriterad byggordning
1. Health + appstart
2. Databaskoppling
3. Memory-objekt
4. Context-endpoint
5. Learning-objekt
6. OpenAPI för GPT Actions
