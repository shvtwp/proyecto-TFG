import os
import tempfile

from heraldica.ui_catalogo import CatalogoUI
from heraldica.db.session import crear_bd
from scripts.importar_json_db import cargar as cargar_catalogo_desde_json


def _setup_tmp_db():
    tmpdir = tempfile.TemporaryDirectory()
    os.environ["DATABASE_URL"] = f"sqlite:///{tmpdir.name}/test.db"
    crear_bd()
    cargar_catalogo_desde_json()
    return tmpdir


def test_ui_repo_filtrado_basico_por_esmalte():
    td = _setup_tmp_db()
    try:
        repo = CatalogoUI()
        res = repo.filtrar_por_esmalte("azur")
        assert isinstance(res, list)
        assert any(r["nombre"].lower().startswith("la carlota") for r in res)
    finally:
        td.cleanup()


def test_ui_repo_por_mueble_y_adorno():
    td = _setup_tmp_db()
    try:
        repo = CatalogoUI()
        res_m = repo.filtrar_por_mueble("castillo")
        assert len(res_m) >= 1
        res_a = repo.filtrar_por_adorno("corona")
        assert isinstance(res_a, list)
    finally:
        td.cleanup()


def test_ui_repo_pieza_y_portador():
    td = _setup_tmp_db()
    try:
        repo = CatalogoUI()
        res_p = repo.filtrar_por_pieza("oro")
        assert len(res_p) >= 1
        res_port = repo.filtrar_por_portador("bornos")
        assert len(res_port) >= 1
    finally:
        td.cleanup()
