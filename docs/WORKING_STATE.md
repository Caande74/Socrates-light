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
```

## Lifecycle v1.5

Lifecycle v1.5 är nu den första användbara releasen för runtime-lifecycle.
Den inkluderar Batch 1 och Batch 2.
Batch 3 är uttryckligen uppskjuten.

### Batch 1 changed
- tillatna statusvarden ar nu `active`, `needs_review`, `inactive` for alla minnestyper
- assumptions tillater dessutom `invalid`
- `/context/get` behandlar `active` och `needs_review` som retrievable
- `needs_review` rankas under motsvarande `active`
- `inactive` exkluderas från normal context retrieval
- assumptions med `invalid` exkluderas från normal context retrieval

### Batch 1 intentionally unchanged
- `/initiatives/active` ar fortsatt strict-active
- feedback-dedupe ar fortsatt active-only
- inga nya databaskolumner
- inga PATCH/DELETE/archive/supersede-endpoints i Batch 1

### Batch 1 tests run
- targeted lifecycle tests via `.venv/bin/python -m pytest tests/test_context.py tests/test_assumptions.py tests/test_feedback.py tests/test_initiatives.py`
- full suite via `.venv/bin/python -m pytest`

### Batch 1 compatibility notes
- feedback-retrieval for generiska queries ar fortfarande selektiv; `needs_review` ar retrievable men en starkare match kan fortfarande prioriteras ensam i svaga query-fall
- feedback-dedupe fortsatter att anvanda endast `active` records

### Batch 2 changed
- PATCH status-endpoints finns nu for assumptions, initiatives och feedback
- status-patch ar owner-scopad och kraver samma owner-context som ovriga scoped endpoints
- retrieval reflekterar patchad status direkt

### Batch 2 intentionally unchanged
- `/initiatives/active` ar fortsatt strict-active
- feedback-dedupe ar fortsatt active-only
- non-assumptions accepterar fortfarande inte `invalid`
- decisions, adjustments och patterns har inte fatt PATCH-status i denna batch

### GPT policy alignment
- aktuell runtime-lasning ska vaga tyngre an tidigare tradsyntes eller tidigare GPT-svar i samma konversation
- `inactive` och `invalid` ska inte behandlas som normal aktiv grund bara for att de tidigare varit del av resonemanget
