from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "data" / "data.db"

_engine = None
_engine_url = None


def _get_engine():
    global _engine, _engine_url
    url = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB}")
    if _engine is None or url != _engine_url:
        _engine = create_engine(url, echo=False)
        _engine_url = url
    return _engine


def crear_bd() -> None:

    SQLModel.metadata.create_all(_get_engine())


def get_session() -> Session:
    return Session(_get_engine())
