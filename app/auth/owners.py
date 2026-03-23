from dataclasses import dataclass
from uuid import UUID


CALLE_OWNER_ID = "6c9bd676-4594-5ef3-a58c-30b2f083ed1b"
CALLE_OWNER_NAME = "Calle"


@dataclass(frozen=True)
class OwnerRecord:
    owner_id: str
    owner_name: str
    legacy_owners: tuple[str, ...] = ()
    auth_subjects: tuple[str, ...] = ()


@dataclass(frozen=True)
class OwnerContext:
    owner_id: str
    owner_name: str | None = None
    legacy_owner: str | None = None


KNOWN_OWNERS = (
    OwnerRecord(
        owner_id=CALLE_OWNER_ID,
        owner_name=CALLE_OWNER_NAME,
        legacy_owners=("calle", "alfa 22"),
        auth_subjects=("subject-calle",),
    ),
)

OWNER_BY_ID = {record.owner_id: record for record in KNOWN_OWNERS}
LEGACY_OWNER_TO_RECORD = {
    legacy_owner: record
    for record in KNOWN_OWNERS
    for legacy_owner in record.legacy_owners
}
AUTH_SUBJECT_TO_OWNER_ID = {
    auth_subject: record.owner_id
    for record in KNOWN_OWNERS
    for auth_subject in record.auth_subjects
}


def normalize_owner_id(value: str | UUID | None) -> str | None:
    if value is None:
        return None
    return str(UUID(str(value)))


def get_owner_record(owner_id: str | UUID | None) -> OwnerRecord | None:
    normalized_owner_id = normalize_owner_id(owner_id)
    if normalized_owner_id is None:
        return None
    return OWNER_BY_ID.get(normalized_owner_id)


def get_owner_record_for_legacy_owner(legacy_owner: str | None) -> OwnerRecord | None:
    if legacy_owner is None:
        return None
    return LEGACY_OWNER_TO_RECORD.get(legacy_owner.strip().lower())


def resolve_owner_context(
    owner_id: str | UUID | None = None,
    *,
    authenticated_subject: str | None = None,
    legacy_owner: str | None = None,
) -> OwnerContext:
    """
    Current flow: callers pass the explicit owner_id from the request body.

    Future shared-GPT flow: backend auth/session should call this with the
    authenticated subject and omit the prompt-level owner_id. This module does
    not infer identities from chat text or free-form content.
    """
    normalized_owner_id = normalize_owner_id(owner_id)
    mapped_owner_id = AUTH_SUBJECT_TO_OWNER_ID.get(authenticated_subject or "") if authenticated_subject else None

    if authenticated_subject and mapped_owner_id is None:
        raise PermissionError("authenticated_subject is not mapped to a runtime owner")

    if mapped_owner_id and normalized_owner_id and mapped_owner_id != normalized_owner_id:
        raise PermissionError("authenticated_subject does not match owner_id")

    resolved_owner_id = mapped_owner_id or normalized_owner_id
    if resolved_owner_id is None:
        raise ValueError("owner_id or authenticated_subject is required")

    record = OWNER_BY_ID.get(resolved_owner_id)

    return OwnerContext(
        owner_id=resolved_owner_id,
        owner_name=record.owner_name if record else None,
        legacy_owner=legacy_owner,
    )
