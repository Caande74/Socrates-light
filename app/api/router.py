from fastapi import APIRouter
from app.api.routes import (
    health,
    context,
    decisions,
    assumptions,
    preferences,
    goals,
    initiatives,
    relationships,
    case_outcomes,
    feedback,
    adjustments,
    patterns,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(context.router, prefix="/context", tags=["context"])
api_router.include_router(decisions.router, prefix="/decisions", tags=["decisions"])
api_router.include_router(assumptions.router, prefix="/assumptions", tags=["assumptions"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(initiatives.router, prefix="/initiatives", tags=["initiatives"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(case_outcomes.router, prefix="/case-outcomes", tags=["case-outcomes"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(adjustments.router, prefix="/adjustments", tags=["adjustments"])
api_router.include_router(patterns.router, prefix="/patterns", tags=["patterns"])