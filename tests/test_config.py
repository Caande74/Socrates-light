import importlib
import sys
from pathlib import Path

import pytest


def load_config_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    sys.modules.pop("app.config", None)
    return importlib.import_module("app.config")


def test_default_database_url_points_to_project_runtime_db(monkeypatch: pytest.MonkeyPatch):
    config = load_config_module(monkeypatch)

    expected_path = Path(__file__).resolve().parents[1] / "runtime.db"
    assert config.settings.database_url == f"sqlite:///{expected_path}"


def test_relative_sqlite_url_is_resolved_from_project_root(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./data/runtime.db")
    sys.modules.pop("app.config", None)

    config = importlib.import_module("app.config")

    expected_path = (Path(__file__).resolve().parents[1] / "data/runtime.db").resolve()
    assert config.settings.database_url == f"sqlite:///{expected_path}"


def test_in_memory_sqlite_is_rejected_outside_testing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("ENVIRONMENT", "development")
    sys.modules.pop("app.config", None)

    with pytest.raises(ValueError, match="in-memory SQLite"):
        importlib.import_module("app.config")


def test_in_memory_sqlite_is_allowed_for_testing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    sys.modules.pop("app.config", None)

    config = importlib.import_module("app.config")

    assert config.settings.database_url == "sqlite:///:memory:"
