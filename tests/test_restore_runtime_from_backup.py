import sqlite3

from app.auth.owners import CALLE_OWNER_ID, CALLE_OWNER_NAME
from scripts.restore_runtime_from_backup import restore_runtime_from_backup


def create_source_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE feedback (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            target_type TEXT,
            target_id TEXT,
            signal TEXT,
            severity TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE assumptions (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            falsification_signal TEXT,
            affected_items TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE adjustments (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            target_scope TEXT,
            target_name TEXT,
            adjustment_type TEXT,
            instruction_delta TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE patterns (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            pattern_type TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE initiatives (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            objective TEXT,
            stage TEXT,
            next_step TEXT,
            blockers TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE decisions (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            decision_date TEXT,
            rationale TEXT,
            impact_scope TEXT
        )
        """
    )
    connection.commit()


def create_target_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE feedback (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            owner_name TEXT,
            legacy_owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            target_type TEXT,
            target_id TEXT,
            signal TEXT,
            severity TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE assumptions (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            owner_name TEXT,
            legacy_owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            falsification_signal TEXT,
            affected_items TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE adjustments (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            owner_name TEXT,
            legacy_owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            target_scope TEXT,
            target_name TEXT,
            adjustment_type TEXT,
            instruction_delta TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE patterns (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            owner_name TEXT,
            legacy_owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            pattern_type TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE initiatives (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            owner_name TEXT,
            legacy_owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            objective TEXT,
            stage TEXT,
            next_step TEXT,
            blockers TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE decisions (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            status TEXT,
            tags TEXT,
            confidence REAL,
            source TEXT,
            owner TEXT,
            owner_name TEXT,
            legacy_owner TEXT,
            created_at TEXT,
            updated_at TEXT,
            decision_date TEXT,
            rationale TEXT,
            impact_scope TEXT
        )
        """
    )
    connection.commit()


def test_restore_runtime_from_backup_imports_calle_and_skips_existing_ids(tmp_path):
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"

    source_connection = sqlite3.connect(source_db)
    target_connection = sqlite3.connect(target_db)

    create_source_schema(source_connection)
    create_target_schema(target_connection)

    source_connection.execute(
        """
        INSERT INTO feedback (
            id, title, content, status, tags, confidence, source, owner, created_at, updated_at,
            target_type, target_id, signal, severity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "feedback-source-1",
            "Restored feedback",
            "Restored content",
            "active",
            "restore,test",
            0.8,
            "backup",
            "calle",
            "2026-01-01T00:00:00",
            "2026-01-01T00:00:00",
            "decision",
            "dec-1",
            "positive",
            "medium",
        ),
    )
    source_connection.execute(
        """
        INSERT INTO feedback (
            id, title, content, status, tags, confidence, source, owner, created_at, updated_at,
            target_type, target_id, signal, severity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "feedback-other-owner",
            "Other owner",
            "Should not import",
            "active",
            None,
            None,
            "backup",
            "someone-else",
            "2026-01-01T00:00:00",
            "2026-01-01T00:00:00",
            None,
            None,
            None,
            None,
        ),
    )
    source_connection.execute(
        """
        INSERT INTO feedback (
            id, title, content, status, tags, confidence, source, owner, created_at, updated_at,
            target_type, target_id, signal, severity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "feedback-source-2",
            "Imported restore row",
            "Import me from backup",
            "active",
            "restore,second",
            0.9,
            "backup",
            "calle",
            "2026-01-03T00:00:00",
            "2026-01-03T00:00:00",
            "feedback",
            "fb-2",
            "neutral",
            "low",
        ),
    )
    target_connection.execute(
        """
        INSERT INTO feedback (
            id, title, content, status, tags, confidence, source, owner, owner_name, legacy_owner,
            created_at, updated_at, target_type, target_id, signal, severity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "feedback-source-1",
            "Already present",
            "Keep target version",
            "active",
            None,
            None,
            "target",
            CALLE_OWNER_ID,
            CALLE_OWNER_NAME,
            "calle",
            "2026-01-02T00:00:00",
            "2026-01-02T00:00:00",
            None,
            None,
            None,
            None,
        ),
    )
    target_connection.commit()
    source_connection.commit()
    source_connection.close()
    target_connection.close()

    restore_runtime_from_backup(str(source_db), str(target_db))

    check_connection = sqlite3.connect(target_db)
    check_connection.row_factory = sqlite3.Row
    rows = check_connection.execute("SELECT * FROM feedback ORDER BY id").fetchall()
    check_connection.close()

    assert len(rows) == 2
    assert rows[0]["id"] == "feedback-source-1"
    assert rows[0]["owner"] == CALLE_OWNER_ID
    assert rows[0]["owner_name"] == CALLE_OWNER_NAME
    assert rows[0]["legacy_owner"] == "calle"
    assert rows[0]["content"] == "Keep target version"

    assert rows[1]["id"] == "feedback-source-2"
    assert rows[1]["owner"] == CALLE_OWNER_ID
    assert rows[1]["owner_name"] == CALLE_OWNER_NAME
    assert rows[1]["legacy_owner"] == "calle"
