from sqlalchemy.orm import Session

from app.db.repositories.assumptions import list_active_assumptions
from app.db.repositories.decisions import list_active_decisions
from app.db.repositories.goals import list_active_goals
from app.db.repositories.initiatives import list_active_initiatives
from app.db.repositories.preferences import list_active_preferences
from app.runtime.ranking import score_text_match


def retrieve_relevant_decisions(
    db: Session,
    query: str,
    owner_id: str | None = None,
    mode: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    limit: int = 5,
):
    decisions = list_active_decisions(db, owner_id)
    ranked = []

    for decision in decisions:
        score = 0
        score += score_text_match(query, decision.title)
        score += score_text_match(query, decision.content)
        score += score_text_match(query, decision.tags)
        score += score_text_match(query, decision.impact_scope)
        score += score_text_match(query, decision.rationale)

        if mode:
            score += score_text_match(mode, decision.impact_scope)
            score += score_text_match(mode, decision.tags)

        if tags:
            for tag in tags:
                score += score_text_match(tag, decision.tags)

        if score > 0:
            ranked.append((score, decision))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:limit]]


def retrieve_relevant_assumptions(
    db: Session,
    query: str,
    owner_id: str | None = None,
    mode: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    limit: int = 5,
):
    assumptions = list_active_assumptions(db, owner_id)
    ranked = []

    for assumption in assumptions:
        score = 0
        score += score_text_match(query, assumption.title)
        score += score_text_match(query, assumption.content)
        score += score_text_match(query, assumption.tags)
        score += score_text_match(query, assumption.falsification_signal)
        score += score_text_match(query, assumption.affected_items)

        if mode:
            score += score_text_match(mode, assumption.tags)

        if tags:
            for tag in tags:
                score += score_text_match(tag, assumption.tags)

        if score > 0:
            ranked.append((score, assumption))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:limit]]


def retrieve_relevant_preferences(
    db: Session,
    query: str,
    owner_id: str | None = None,
    mode: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    limit: int = 5,
):
    preferences = list_active_preferences(db, owner_id)
    ranked = []

    for preference in preferences:
        score = 0
        score += score_text_match(query, preference.title)
        score += score_text_match(query, preference.content)
        score += score_text_match(query, preference.tags)
        score += score_text_match(query, preference.scope)

        if mode:
            score += score_text_match(mode, preference.tags)
            score += score_text_match(mode, preference.scope)

        if role:
            score += score_text_match(role, preference.tags)
            score += score_text_match(role, preference.scope)

        if tags:
            for tag in tags:
                score += score_text_match(tag, preference.tags)

        if score > 0:
            ranked.append((score, preference))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:limit]]


def retrieve_relevant_goals(
    db: Session,
    query: str,
    owner_id: str | None = None,
    mode: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    limit: int = 5,
):
    goals = list_active_goals(db, owner_id)
    ranked = []

    for goal in goals:
        score = 0
        score += score_text_match(query, goal.title)
        score += score_text_match(query, goal.content)
        score += score_text_match(query, goal.tags)
        score += score_text_match(query, goal.horizon)

        if mode:
            score += score_text_match(mode, goal.tags)

        if tags:
            for tag in tags:
                score += score_text_match(tag, goal.tags)

        if score > 0:
            ranked.append((score, goal))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:limit]]


def retrieve_relevant_initiatives(
    db: Session,
    query: str,
    owner_id: str | None = None,
    mode: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    limit: int = 5,
):
    initiatives = list_active_initiatives(db, owner_id)
    ranked = []

    for initiative in initiatives:
        score = 0
        score += score_text_match(query, initiative.title)
        score += score_text_match(query, initiative.content)
        score += score_text_match(query, initiative.tags)
        score += score_text_match(query, initiative.objective)
        score += score_text_match(query, initiative.stage)
        score += score_text_match(query, initiative.next_step)
        score += score_text_match(query, initiative.blockers)

        if mode:
            score += score_text_match(mode, initiative.tags)

        if tags:
            for tag in tags:
                score += score_text_match(tag, initiative.tags)

        if score > 0:
            ranked.append((score, initiative))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:limit]]
