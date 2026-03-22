import sys
from pathlib import Path

from sqlalchemy import inspect, text

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.db.models  # noqa: F401
from app.auth.owners import CALLE_OWNER_ID, CALLE_OWNER_NAME
from app.db.session import engine


CORE_TABLES = [
    "decisions",
    "assumptions",
    "preferences",
    "goals",
    "initiatives",
    "case_outcomes",
    "feedback",
    "adjustments",
    "patterns",
]


def ensure_owner_columns(connection, table_name: str) -> None:
    existing_columns = {column["name"] for column in inspect(connection).get_columns(table_name)}
    if "owner_name" not in existing_columns:
        connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN owner_name VARCHAR(255)"))
    if "legacy_owner" not in existing_columns:
        connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN legacy_owner VARCHAR(255)"))


def migrate_table(connection, table_name: str) -> dict[str, int]:
    calle_result = connection.execute(
        text(
            f"""
            UPDATE {table_name}
            SET owner = :owner_id,
                owner_name = :owner_name,
                legacy_owner = 'calle'
            WHERE lower(owner) = 'calle'
            """
        ),
        {"owner_id": CALLE_OWNER_ID, "owner_name": CALLE_OWNER_NAME},
    )
    alfa_result = connection.execute(
        text(
            f"""
            UPDATE {table_name}
            SET owner = :owner_id,
                owner_name = :owner_name,
                legacy_owner = 'alfa 22'
            WHERE owner = 'alfa 22'
            """
        ),
        {"owner_id": CALLE_OWNER_ID, "owner_name": CALLE_OWNER_NAME},
    )
    known_owner_result = connection.execute(
        text(
            f"""
            UPDATE {table_name}
            SET owner_name = :owner_name
            WHERE owner = :owner_id
              AND (owner_name IS NULL OR owner_name = '')
            """
        ),
        {"owner_id": CALLE_OWNER_ID, "owner_name": CALLE_OWNER_NAME},
    )

    return {
        "calle": calle_result.rowcount or 0,
        "alfa_22": alfa_result.rowcount or 0,
        "owner_name_backfill": known_owner_result.rowcount or 0,
    }


def main() -> None:
    totals = {"calle": 0, "alfa_22": 0, "owner_name_backfill": 0}

    with engine.begin() as connection:
        for table_name in CORE_TABLES:
            ensure_owner_columns(connection, table_name)
            counts = migrate_table(connection, table_name)
            for key, value in counts.items():
                totals[key] += value
            print(f"{table_name}: {counts}")

    print(f"calle -> {CALLE_OWNER_ID} ({CALLE_OWNER_NAME}) migrated: {totals['calle']}")
    print(f"alfa 22 -> {CALLE_OWNER_ID} ({CALLE_OWNER_NAME}) migrated: {totals['alfa_22']}")
    print(f"owner_name backfilled for {CALLE_OWNER_NAME}: {totals['owner_name_backfill']}")


if __name__ == "__main__":
    main()
