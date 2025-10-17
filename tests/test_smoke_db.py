import os
import tempfile
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from heraldica.db.session import crear_bd, get_session
from heraldica.db.models import Campo, Mueble, Escudo
from sqlmodel import select


def test_guardar_y_leer_escudo():
    with tempfile.TemporaryDirectory() as d:
        os.environ["DATABASE_URL"] = f"sqlite:///{d}/test.db"
        crear_bd()
        with get_session() as s:
            c = Campo(esmalte="gules")
            s.add(c)
            s.commit()
            s.refresh(c)
            s.add(Mueble(campo_id=c.id, nombre="castillo"))
            s.commit()
            s.add(Escudo(nombre="E1", portador="familia roja", campo_id=c.id))
            s.commit()

            res = s.exec(select(Escudo).where(Escudo.portador == "familia roja")).all()
            assert [e.nombre for e in res] == ["E1"]
