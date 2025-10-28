"""Tests for Catalogo singleton pattern and dependency injection."""

import os
import tempfile
from heraldica.catalogo import Catalogo
from heraldica.db.session import crear_bd, get_session
from scripts.importar_json_db import cargar as cargar_catalogo_desde_json


def test_catalogo_singleton_same_instance():
    """Verify that Catalogo returns the same instance."""
    # Reset singleton before test
    Catalogo.reset_instance()

    cat1 = Catalogo()
    cat2 = Catalogo()

    assert cat1 is cat2, "Catalogo should return the same instance"


def test_catalogo_singleton_reset():
    """Verify that reset_instance creates a new instance."""
    Catalogo.reset_instance()
    cat1 = Catalogo()

    Catalogo.reset_instance()
    cat2 = Catalogo()

    assert cat1 is not cat2, "After reset, a new instance should be created"


def test_catalogo_session_factory_injection():
    """Verify that session factory can be injected."""
    # Setup temporary database
    tmpdir = tempfile.TemporaryDirectory()
    try:
        os.environ["DATABASE_URL"] = f"sqlite:///{tmpdir.name}/test.db"
        crear_bd()
        cargar_catalogo_desde_json()

        # Reset and inject session factory
        Catalogo.reset_instance()
        cat = Catalogo(session_factory=get_session)

        # Verify it can load from database
        cat.recargar_desde_bd()

        # Should have loaded data from DB
        assert len(cat._fichas) > 0, "Should load data from database"

    finally:
        tmpdir.cleanup()


def test_catalogo_set_session_factory():
    """Verify that session factory can be set via class method."""
    Catalogo.reset_instance()
    Catalogo.set_session_factory(get_session)

    # Create instance to verify factory was set
    Catalogo()
    assert Catalogo._session_factory is get_session


def test_catalogo_fallback_to_default_session():
    """Verify that Catalogo falls back to default session when none injected."""
    Catalogo.reset_instance()
    # Create instance to verify no crash
    Catalogo()

    # Should work with default session (may create DB if needed)
    # This just verifies it doesn't crash
    assert Catalogo._session_factory is None, "Should start with no injected factory"
