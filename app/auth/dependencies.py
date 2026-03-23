from fastapi import Depends, Header, HTTPException, Request, status

from app.config import settings
from app.auth.owners import OwnerContext, resolve_owner_context
from app.schemas.context import ContextRequest


def authenticated_subject(request: Request, x_authenticated_subject: str | None = Header(default=None)) -> str | None:
    # Preferred source during the transition: upstream auth/session middleware
    # should populate request.state.authenticated_subject.
    subject = getattr(request.state, "authenticated_subject", None)

    # Temporary bridge for tests and local integration until real auth/session
    # middleware is in place. This header path should be removed once the
    # backend can always resolve the subject server-side.
    if (
        subject is None
        and x_authenticated_subject is not None
        and settings.environment in {"development", "test"}
    ):
        request.state.authenticated_subject = x_authenticated_subject
        subject = x_authenticated_subject
    return subject


def resolve_context_owner(
    payload: ContextRequest,
    subject: str | None = Depends(authenticated_subject),
) -> OwnerContext:
    # Error policy for the transition step on runtime endpoints:
    # - 403 for authenticated subject mismatches / forbidden owner access
    # - 400 when the client provides no usable identity context at all
    return resolve_runtime_owner(owner_id=payload.owner_id, authenticated_subject=subject)


def resolve_runtime_owner(owner_id: str | None, authenticated_subject: str | None) -> OwnerContext:
    try:
        return resolve_owner_context(
            authenticated_subject=authenticated_subject,
            owner_id=owner_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
