import os
import sys
import pathlib
import tempfile

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from heraldica.db.session import crear_bd
from heraldica.catalogo import Catalogo
from scripts.importar_json_db import cargar as cargar_catalogo_desde_json


def test_carga_json_y_busquedas_basicas():
    with tempfile.TemporaryDirectory() as d:
        os.environ["DATABASE_URL"] = f"sqlite:///{d}/test.db"

        crear_bd()
        cargar_catalogo_desde_json()

        cat = Catalogo()
        cat.recargar_desde_bd()

        res_esmalte = cat.filtrar_por_esmalte("azur")
        assert any(f.nombre.lower().startswith("la carlota") for f in res_esmalte)

        res_mueble = cat.filtrar_por_mueble("castillo")
        assert len(res_mueble) >= 1

        res_pieza = cat.filtrar_por_pieza("oro")
        assert len(res_pieza) >= 1

        res_adorno = cat.filtrar_por_adorno("corona")
        assert isinstance(res_adorno, list)

        res_portador = cat.filtrar_por_portador("bornos")
        assert len(res_portador) >= 1
