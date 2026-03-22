def score_text_match(query: str, text: str | None) -> int:
    if not text:
        return 0

    score = 0
    query_terms = [term.strip().lower() for term in query.split() if term.strip()]
    haystack = text.lower()

    for term in query_terms:
        if term in haystack:
            score += 1

    return score