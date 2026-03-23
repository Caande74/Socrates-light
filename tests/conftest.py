import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TEST_DB_PATH = ROOT / "test_runtime.db"
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

from app.db.base import Base
from app.db.session import engine


@pytest.fixture(autouse=True)
def reset_database():
    if str(engine.url).endswith("/runtime.db"):
        raise RuntimeError("Refusing to run tests against the primary runtime database")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
