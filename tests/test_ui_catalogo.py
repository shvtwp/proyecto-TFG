import os
import tempfile

from heraldica.catalogo import Catalogo
from heraldica.db.session import crear_bd
from scripts.importar_json_db import cargar as cargar_catalogo_desde_json
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def _setup_tmp_db():
    tmpdir = tempfile.TemporaryDirectory()
    os.environ["DATABASE_URL"] = f"sqlite:///{tmpdir.name}/test.db"
    crear_bd()
    cargar_catalogo_desde_json()
    return tmpdir

def get_test_session():
    """Crea una base SQLite temporal y devuelve una fábrica de sesiones."""
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from heraldica.db.session import crear_bd
    from scripts.importar_json_db import cargar as cargar_catalogo_desde_json

    os.environ.pop("DATABASE_URL", None)

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd) 

    engine = create_engine(f"sqlite:///{path}")

    crear_bd()
    cargar_catalogo_desde_json()

    return lambda: Session(engine)


def test_ui_repo_filtrado_basico_por_esmalte():
    td = _setup_tmp_db()
    try:
        Catalogo.reset_instance()
        repo = Catalogo()
        res = [f.to_dict() for f in repo.filtrar_por_esmalte("azur")]
        assert isinstance(res, list)
        assert any(r["nombre"].lower().startswith("la carlota") for r in res)
    finally:
        Catalogo.reset_instance()
        td.cleanup()


def test_ui_repo_por_mueble_y_adorno():
    td = _setup_tmp_db()
    try:
        Catalogo.reset_instance()
        repo = Catalogo()
        res_m = [f.to_dict() for f in repo.filtrar_por_mueble("castillo")]
        assert len(res_m) >= 1
        res_a = [f.to_dict() for f in repo.filtrar_por_adorno("corona")]
        assert isinstance(res_a, list)
    finally:
        Catalogo.reset_instance()
        td.cleanup()


def test_ui_repo_pieza_y_portador():
    td = _setup_tmp_db()
    try:
        Catalogo.reset_instance()
        repo = Catalogo()
        res_p = [f.to_dict() for f in repo.filtrar_por_pieza("oro")]
        assert len(res_p) >= 1
        res_port = [f.to_dict() for f in repo.filtrar_por_portador("bornos")]
        assert len(res_port) >= 1
    finally:
        Catalogo.reset_instance()
        td.cleanup()

def test_catalogo_inyectado_con_sesion_temporal():
    """Comprueba que Catalogo funciona con una sesión inyectada."""
    Catalogo.reset_instance()
    repo = Catalogo(session_factory=get_test_session())
    fichas = repo.obtener_todos()
    assert isinstance(fichas, list)
    Catalogo.reset_instance()
