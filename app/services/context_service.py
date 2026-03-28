import logging
from app.db.models.feedback import Feedback
from sqlalchemy.orm import Session

from app.auth.owners import resolve_owner_context
from app.db.models.relationship import Relationship

from app.db.models.decision import Decision
from app.db.models.assumption import Assumption
from app.db.models.initiative import Initiative
from app.db.models.adjustment import Adjustment
from app.db.models.pattern import Pattern
from app.db.repositories.common import list_retrievable
from app.runtime.statuses import status_rank_adjustment


GENERIC_TAGS = {
    "pattern",
    "adjustment",
    "initiativ",
    "initiative",
    "runtime",
    "minne",
    "retrieval",
    "ai-ledningsteam",
}

LOW_SIGNAL_TAGS = {
    "energi",
    "investering",
    "risk",
    "projektutveckling",
    "prioritering",
    "analys",
    "projekt",
    "portfolj",
    "kapacitet",
    "stabschef",
    "investeringsbedomning",
}

logger = logging.getLogger(__name__)

FEEDBACK_GENERIC_TERMS = {
    "test",
    "feedback",
    "minne",
    "memory",
}


def _normalize(text: str | list[str] | None) -> str:
    if isinstance(text, list):
        return " ".join(part.strip() for part in text if part and part.strip()).lower()
    return (text or "").strip().lower()


def _expanded_query_tokens(text: str | None) -> list[str]:
    normalized = _normalize(text)
    if not normalized:
        return []

    raw_tokens = [token for token in normalized.split() if token]

    expanded_tokens = []
    seen = set()

    for token in raw_tokens:
        for expanded in _expand_compound_token(token):
            if expanded not in seen:
                seen.add(expanded)
                expanded_tokens.append(expanded)

    return expanded_tokens


def _direct_match_tokens(text: str | None) -> list[str]:
    expanded = _expanded_query_tokens(text)
    direct_tokens = []

    for token in expanded:
        if token in LOW_SIGNAL_TAGS:
            continue
        direct_tokens.append(token)

    return direct_tokens


def _expand_compound_token(token: str) -> list[str]:
    expanded = {token}

    compound_parts = [
        ("investeringsrisk", ["investering", "risk"]),
        ("natkapacitetsrisk", ["nat", "kapacitet", "risk"]),
        ("nätkapacitetsrisk", ["nat", "kapacitet", "risk"]),
        ("batterilager", ["batterilager"]),
        ("natanslutning", ["natanslutning", "nat", "anslutning"]),
        ("nätanslutning", ["natanslutning", "nat", "anslutning"]),
    ]

    for needle, parts in compound_parts:
        if needle in token:
            expanded.update(parts)

    if token.endswith("risk") and token != "risk":
        expanded.add("risk")
    if token.endswith("investering") and token != "investering":
        expanded.add("investering")
    if token.endswith("kapacitet") and token != "kapacitet":
        expanded.add("kapacitet")

    return list(expanded)


def _model_name_to_item_type(model_name: str) -> str:
    mapping = {
        "decision": "decision",
        "assumption": "assumption",
        "initiative": "initiative",
        "adjustment": "adjustment",
        "pattern": "pattern",
        "feedback": "feedback",
    }
    return mapping[model_name]


def _item_type_to_model(item_type: str):
    mapping = {
        "decision": Decision,
        "assumption": Assumption,
        "initiative": Initiative,
        "adjustment": Adjustment,
        "pattern": Pattern,
        "feedback": Feedback,
    }
    return mapping.get(item_type)


def _load_relationship_edges(db: Session) -> list[Relationship]:
    return db.query(Relationship).all()


def _collect_related_ids(
    db: Session,
    direct_map: dict[str, list],
) -> dict[str, set[str]]:
    related_ids = {
        "decision": set(),
        "assumption": set(),
        "initiative": set(),
        "adjustment": set(),
        "pattern": set(),
        "feedback": set(),
    }

    allowed_relationship_types = {
        "depends_on",
        "guided_by",
        "derived_from",
    }

    seed_pairs = {
        (model_name, item.id)
        for model_name, items in direct_map.items()
        for item in items
    }

    edges = _load_relationship_edges(db)

    frontier = set(seed_pairs)
    visited = set(seed_pairs)

    for _ in range(2):
        next_frontier = set()

        for edge in edges:
            if edge.relationship_type not in allowed_relationship_types:
                continue

            left = (edge.from_type, edge.from_id)
            right = (edge.to_type, edge.to_id)

            if left in frontier and right not in visited:
                if edge.to_type in related_ids:
                    related_ids[edge.to_type].add(edge.to_id)
                next_frontier.add(right)
                visited.add(right)

            if right in frontier and left not in visited:
                if edge.from_type in related_ids:
                    related_ids[edge.from_type].add(edge.from_id)
                next_frontier.add(left)
                visited.add(left)

        frontier = next_frontier
        if not frontier:
            break

    return related_ids


def _expand_items_by_relationships(
    active_items: list,
    existing_items: list,
    related_ids: set[str],
    limit: int = 5,
) -> list:
    existing_ids = {item.id for item in existing_items}
    relationship_items = []

    for item in active_items:
        if item.id in existing_ids:
            continue
        if item.id in related_ids:
            relationship_items.append(item)

    expanded = list(existing_items)

    for item in relationship_items:
        if len(expanded) >= limit:
            break
        expanded.append(item)

    return expanded


def _tokenize(text: str | None) -> list[str]:
    return _expanded_query_tokens(text)


def _tag_list(tags: str | list[str] | None) -> list[str]:
    if isinstance(tags, list):
        return [tag.strip().lower() for tag in tags if tag and tag.strip()]

    raw = _normalize(tags)
    if not raw:
        return []
    return [tag.strip() for tag in raw.split(",") if tag.strip()]


def _meaningful_tags(tags: str | None) -> set[str]:
    return {tag for tag in _tag_list(tags) if tag not in GENERIC_TAGS}


def _high_signal_tags(tags: str | None) -> set[str]:
    return {
        tag
        for tag in _tag_list(tags)
        if tag not in GENERIC_TAGS and tag not in LOW_SIGNAL_TAGS
    }


def _matched_terms(item, query: str) -> list[str]:
    query_tokens = _tokenize(query)
    title = _normalize(item.title)
    content = _normalize(item.content)
    tags = _normalize(item.tags)

    matched = []
    for token in query_tokens:
        if token in title or token in content or token in tags:
            matched.append(token)
    return matched


def _matched_tags(item, seed_tags: set[str] | None = None) -> list[str]:
    item_tags = _high_signal_tags(item.tags)
    if seed_tags is None:
        return sorted(item_tags)
    return sorted(item_tags.intersection(seed_tags))


def _to_context_item(item, retrieval_path: str, matched_terms: list[str], matched_tags: list[str]) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "content": item.content,
        "status": item.status,
        "tags": item.tags,
        "confidence": item.confidence,
        "source": item.source,
        "owner_id": item.owner_id,
        "owner_name": item.owner_name,
        "legacy_owner": item.legacy_owner,
        "retrieval_path": retrieval_path,
        "matched_terms": matched_terms,
        "matched_tags": matched_tags,
    }


def _base_score_item(item, query: str) -> int:
    query_tokens = _direct_match_tokens(query)
    if not query_tokens:
        return 0

    title = _normalize(item.title)
    content = _normalize(item.content)
    tags = _normalize(item.tags)

    score = 0
    for token in query_tokens:
        if token in title:
            score += 3
        if token in content:
            score += 2
        if token in tags:
            score += 2
    return score


def _mode_bonus(model_name: str, mode: str | None) -> int:
    mode_normalized = _normalize(mode)

    if mode_normalized == "execution":
        bonuses = {
            "decision": 3,
            "initiative": 3,
            "assumption": 1,
            "adjustment": 1,
            "pattern": 0,
            "feedback": 0,
        }
        return bonuses.get(model_name, 0)

    if mode_normalized == "analysis":
        bonuses = {
            "decision": 1,
            "initiative": 0,
            "assumption": 3,
            "adjustment": 2,
            "pattern": 2,
            "feedback": 0,
        }
        return bonuses.get(model_name, 0)

    if mode_normalized == "strategy":
        bonuses = {
            "decision": 2,
            "initiative": 2,
            "assumption": 2,
            "adjustment": 2,
            "pattern": 3,
            "feedback": 0,
        }
        return bonuses.get(model_name, 0)

    return 0


def _role_bonus(model_name: str, role: str | None, item) -> int:
    role_normalized = _normalize(role)
    tags = _meaningful_tags(item.tags)
    title = _normalize(item.title)
    content = _normalize(item.content)

    score = 0

    if role_normalized == "investeringsradgivare":
        if model_name in {"assumption", "adjustment", "pattern"}:
            score += 2
        if "investering" in tags or "risk" in tags:
            score += 2
        if "investering" in title or "risk" in title or "investering" in content or "risk" in content:
            score += 1

    elif role_normalized == "operator":
        if model_name in {"decision", "initiative", "adjustment"}:
            score += 2
        if "execution" in tags or "drift" in tags or "operativ" in tags:
            score += 2

    elif role_normalized == "stabschef":
        if model_name in {"decision", "assumption", "adjustment", "pattern"}:
            score += 1
        if "risk" in tags or "prioritering" in tags:
            score += 2

    return score


def _expansion_score(item, seed_tags: set[str]) -> int:
    item_tags = _high_signal_tags(item.tags)
    if not item_tags or not seed_tags:
        return 0

    overlap = item_tags.intersection(seed_tags)
    if not overlap:
        return 0

    return len(overlap) * 3


def _select_direct_items(
    active_items: list,
    model_name: str,
    query: str,
    mode: str | None,
    role: str | None,
    limit: int = 5,
) -> list:
    scored = []
    for item in active_items:
        base_score = _base_score_item(item, query)
        if base_score <= 0:
            continue

        score = (
            base_score
            + _mode_bonus(model_name, mode)
            + _role_bonus(model_name, role, item)
            + status_rank_adjustment(item.status)
        )
        scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for score, item in scored[:limit]]


def _collect_seed_tags(grouped_items: list[list]) -> set[str]:
    seed_tags: set[str] = set()
    for items in grouped_items:
        for item in items:
            seed_tags.update(_high_signal_tags(item.tags))
    return seed_tags


def _expand_items(active_items: list, existing_items: list, seed_tags: set[str], limit: int = 5) -> list:
    existing_ids = {item.id for item in existing_items}
    scored = []

    for item in active_items:
        if item.id in existing_ids:
            continue

        score = _expansion_score(item, seed_tags)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    expanded = list(existing_items)
    for score, item in scored:
        if len(expanded) >= limit:
            break
        expanded.append(item)

    return expanded


def _serialize(final_items: list, direct_ids: set[str], query: str, seed_tags: set[str]) -> list[dict]:
    serialized = []
    for item in final_items:
        retrieval_path = "direct" if item.id in direct_ids else "expanded"
        serialized.append(
            _to_context_item(
                item=item,
                retrieval_path=retrieval_path,
                matched_terms=_matched_terms(item, query),
                matched_tags=_matched_tags(item, seed_tags),
            )
        )
    return serialized


def _feedback_query_tokens(query: str) -> list[str]:
    return [
        token
        for token in _direct_match_tokens(query)
        if token not in FEEDBACK_GENERIC_TERMS
    ]


def _feedback_match_priority(item, query: str) -> tuple[int, int]:
    normalized_query = _normalize(query)
    if not normalized_query:
        return (0, 0)

    content = _normalize(item.content)
    title = _normalize(item.title)

    if normalized_query == content:
        return (4, len(normalized_query))

    if normalized_query == title:
        return (3, len(normalized_query))

    contains_score = 0
    if normalized_query in content:
        contains_score = max(contains_score, 2)
    if normalized_query in title:
        contains_score = max(contains_score, 1)

    term_hits = 0
    for token in _feedback_query_tokens(query):
        if token in content or token in title:
            term_hits += 1

    if contains_score or term_hits >= 2:
        return (2, contains_score + term_hits)

    return (0, 0)


def _feedback_term_hits(item, query: str) -> int:
    content = _normalize(item.content)
    title = _normalize(item.title)

    hits = 0
    for token in _feedback_query_tokens(query):
        if token in content or token in title:
            hits += 1
    return hits


def _feedback_fallback_score(item, query: str, mode: str | None, role: str | None) -> int:
    if _feedback_term_hits(item, query) < 2:
        return 0

    fallback_query = " ".join(_feedback_query_tokens(query))
    base_score = _base_score_item(item, fallback_query)
    if base_score <= 0:
        return 0

    return (
        base_score
        + _mode_bonus("feedback", mode)
        + _role_bonus("feedback", role, item)
        + status_rank_adjustment(item.status)
    )


def _select_direct_feedback_items(
    active_items: list,
    query: str,
    mode: str | None,
    role: str | None,
    limit: int = 5,
) -> list:
    strong_matches = []
    fallback_matches = []

    for item in active_items:
        priority, priority_score = _feedback_match_priority(item, query)
        fallback_score = _feedback_fallback_score(item, query, mode, role)

        if priority > 0:
            strong_matches.append((priority, priority_score, fallback_score, item))
            continue

        if fallback_score > 0:
            fallback_matches.append((fallback_score, item))

    if strong_matches:
        strong_matches.sort(key=lambda row: (row[0], row[1], row[2]), reverse=True)
        return [item for _, _, _, item in strong_matches[:limit]]

    fallback_matches.sort(key=lambda row: row[0], reverse=True)
    return [item for _, item in fallback_matches[:limit]]


def get_context_payload(db: Session, query: str, owner_id: str, mode: str | None, role: str | None) -> dict:
    owner_context = resolve_owner_context(owner_id=owner_id)
    owner_id = owner_context.owner_id
    logger.info("runtime_context_get owner_id=%s owner_name=%s", owner_id, owner_context.owner_name)

    active_decisions = list_retrievable(db, Decision, owner_id)
    active_assumptions = list_retrievable(db, Assumption, owner_id)
    active_initiatives = list_retrievable(db, Initiative, owner_id)
    active_adjustments = list_retrievable(db, Adjustment, owner_id)
    active_patterns = list_retrievable(db, Pattern, owner_id)
    active_feedback = list_retrievable(db, Feedback, owner_id)

    direct_decisions = _select_direct_items(active_decisions, "decision", query, mode, role)
    direct_assumptions = _select_direct_items(active_assumptions, "assumption", query, mode, role)
    direct_initiatives = _select_direct_items(active_initiatives, "initiative", query, mode, role)
    direct_adjustments = _select_direct_items(active_adjustments, "adjustment", query, mode, role)
    direct_patterns = _select_direct_items(active_patterns, "pattern", query, mode, role)
    direct_feedback = _select_direct_feedback_items(active_feedback, query, mode, role)

    direct_map = {
        "decision": direct_decisions,
        "assumption": direct_assumptions,
        "initiative": direct_initiatives,
        "adjustment": direct_adjustments,
        "pattern": direct_patterns,
        "feedback": direct_feedback,
    }

    seed_tags = _collect_seed_tags([
        direct_decisions,
        direct_assumptions,
        direct_initiatives,
        direct_adjustments,
        direct_patterns,
        direct_feedback,
    ])

    related_ids = _collect_related_ids(db, direct_map)

    tag_expanded_decisions = _expand_items(active_decisions, direct_decisions, seed_tags)
    tag_expanded_assumptions = _expand_items(active_assumptions, direct_assumptions, seed_tags)
    tag_expanded_initiatives = _expand_items(active_initiatives, direct_initiatives, seed_tags)
    tag_expanded_adjustments = _expand_items(active_adjustments, direct_adjustments, seed_tags)
    tag_expanded_patterns = _expand_items(active_patterns, direct_patterns, seed_tags)
    tag_expanded_feedback = _expand_items(active_feedback, direct_feedback, seed_tags)

    final_decisions = _expand_items_by_relationships(
        active_items=active_decisions,
        existing_items=tag_expanded_decisions,
        related_ids=related_ids["decision"],
    )
    final_assumptions = _expand_items_by_relationships(
        active_items=active_assumptions,
        existing_items=tag_expanded_assumptions,
        related_ids=related_ids["assumption"],
    )
    final_initiatives = _expand_items_by_relationships(
        active_items=active_initiatives,
        existing_items=tag_expanded_initiatives,
        related_ids=related_ids["initiative"],
    )
    final_adjustments = _expand_items_by_relationships(
        active_items=active_adjustments,
        existing_items=tag_expanded_adjustments,
        related_ids=related_ids["adjustment"],
    )
    final_patterns = _expand_items_by_relationships(
        active_items=active_patterns,
        existing_items=tag_expanded_patterns,
        related_ids=related_ids["pattern"],
    )
    final_feedback = _expand_items_by_relationships(
        active_items=active_feedback,
        existing_items=tag_expanded_feedback,
        related_ids=related_ids["feedback"],
    )

    serialized_decisions = _serialize(final_decisions, {i.id for i in direct_decisions}, query, seed_tags)
    serialized_assumptions = _serialize(final_assumptions, {i.id for i in direct_assumptions}, query, seed_tags)
    serialized_initiatives = _serialize(final_initiatives, {i.id for i in direct_initiatives}, query, seed_tags)
    serialized_adjustments = _serialize(final_adjustments, {i.id for i in direct_adjustments}, query, seed_tags)
    serialized_patterns = _serialize(final_patterns, {i.id for i in direct_patterns}, query, seed_tags)
    serialized_feedback = _serialize(final_feedback, {i.id for i in direct_feedback}, query, seed_tags)

    return {
        "query": query,
        "decisions": serialized_decisions,
        "assumptions": serialized_assumptions,
        "initiatives": serialized_initiatives,
        "adjustments": serialized_adjustments,
        "patterns": serialized_patterns,
        "feedback": serialized_feedback,
        "guidance": {
            "adjustments": serialized_adjustments,
            "patterns": serialized_patterns,
        },
    }
