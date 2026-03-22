import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.auth.owners import CALLE_OWNER_ID, CALLE_OWNER_NAME


SHARED_COLUMNS = [
    "id",
    "title",
    "content",
    "status",
    "tags",
    "confidence",
    "source",
    "created_at",
    "updated_at",
]

RESTORE_TABLES = {
    "feedback": ["target_type", "target_id", "signal", "severity"],
    "assumptions": ["falsification_signal", "affected_items"],
    "adjustments": ["target_scope", "target_name", "adjustment_type", "instruction_delta"],
    "patterns": ["pattern_type"],
    "initiatives": ["objective", "stage", "next_step", "blockers"],
    "decisions": ["decision_date", "rationale", "impact_scope"],
}


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def get_columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def ensure_target_columns(connection: sqlite3.Connection, table_name: str) -> None:
    columns = get_columns(connection, table_name)
    if "owner_name" not in columns:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN owner_name TEXT")
    if "legacy_owner" not in columns:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN legacy_owner TEXT")


def restore_runtime_from_backup(source_db: str, target_db: str) -> dict[str, int]:
    source_connection = sqlite3.connect(source_db)
    target_connection = sqlite3.connect(target_db)
    source_connection.row_factory = sqlite3.Row
    target_connection.row_factory = sqlite3.Row

    imported_counts: dict[str, int] = {}

    try:
        for table_name, extra_columns in RESTORE_TABLES.items():
            imported_counts[table_name] = 0

            if not table_exists(source_connection, table_name):
                print(f"{table_name}: skipped, missing in source")
                continue
            if not table_exists(target_connection, table_name):
                print(f"{table_name}: skipped, missing in target")
                continue

            ensure_target_columns(target_connection, table_name)

            source_columns = SHARED_COLUMNS + ["owner"] + extra_columns
            target_columns = SHARED_COLUMNS + ["owner", "owner_name", "legacy_owner"] + extra_columns

            source_rows = source_connection.execute(
                f"""
                SELECT {", ".join(source_columns)}
                FROM {table_name}
                WHERE owner = ?
                """,
                ("calle",),
            ).fetchall()

            existing_ids = {
                row["id"]
                for row in target_connection.execute(f"SELECT id FROM {table_name}").fetchall()
            }

            rows_to_insert = []
            for row in source_rows:
                if row["id"] in existing_ids:
                    continue

                row_values = [row[column] for column in SHARED_COLUMNS]
                row_values.extend([CALLE_OWNER_ID, CALLE_OWNER_NAME, "calle"])
                row_values.extend(row[column] for column in extra_columns)
                rows_to_insert.append(tuple(row_values))

            if rows_to_insert:
                placeholders = ", ".join("?" for _ in target_columns)
                target_connection.executemany(
                    f"""
                    INSERT INTO {table_name} ({", ".join(target_columns)})
                    VALUES ({placeholders})
                    """,
                    rows_to_insert,
                )
                target_connection.commit()

            imported_counts[table_name] = len(rows_to_insert)
            print(f"{table_name}: imported {imported_counts[table_name]}")

    finally:
        source_connection.close()
        target_connection.close()

    return imported_counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Restore selected runtime tables from a backup SQLite DB.")
    parser.add_argument("--source-db", required=True, help="Path to the backup SQLite DB")
    parser.add_argument("--target-db", required=True, help="Path to the current runtime SQLite DB")
    args = parser.parse_args()

    restore_runtime_from_backup(args.source_db, args.target_db)


if __name__ == "__main__":
    main()
