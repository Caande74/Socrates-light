from fastapi import Request

from app.config import settings


def _trusted_upstream_subject(request: Request) -> str | None:
    header_name = settings.trusted_authenticated_subject_header
    if not header_name:
        return None
    return request.headers.get(header_name)


async def attach_authenticated_subject(request: Request, call_next):
    if getattr(request.state, "authenticated_subject", None) is None:
        trusted_subject = _trusted_upstream_subject(request)
        if trusted_subject:
            # Preferred per-user source when present: a configured upstream
            # identity header injected by trusted auth/proxy infrastructure.
            request.state.authenticated_subject = trusted_subject

    if (
        getattr(request.state, "authenticated_subject", None) is None
        and
        settings.api_authenticated_subject
        and request.headers.get("x-api-key") == settings.api_key
    ):
        # Integration fallback only: this is not per-user identity, just a
        # temporary bridge until real upstream identity is always available.
        request.state.authenticated_subject = settings.api_authenticated_subject

    return await call_next(request)
