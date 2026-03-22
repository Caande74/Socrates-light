# WORKING STATE

## Projekt
`unified-runtime-api-v1-scaffold`

## Syfte
Bygga en lokal runtime för AI-ledningsteamet som kan:
- lagra minne
- hämta relevant kontext
- lagra lärande
- senare kopplas till GPT via Actions

## Lokal miljö
- Mac
- Homebrew installerat
- Git installerat
- Python 3.11 installerat
- virtuell miljö `.venv` fungerar
- FastAPI kör lokalt via `uvicorn`
- SQLite används i v1 via `runtime.db`

## Projektmapp
`~/Projects/full-model-runtime-starter/02_runtime_scaffold/unified-runtime-api-v1-scaffold`

## Startkommando
```bash
cd ~/Projects/full-model-runtime-starter/02_runtime_scaffold/unified-runtime-api-v1-scaffold
source .venv/bin/activate
uvicorn app.main:app --reload
