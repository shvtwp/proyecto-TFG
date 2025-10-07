from heraldica.catalogo import listar, Ficha
from heraldica.esmalte import Esmalte


def test_catalogo_no_vacio_y_usa_esmalte():
    escudos = listar()
    assert len(escudos) >= 1
    assert all(isinstance(f, Ficha) for f in escudos)
    assert all(isinstance(f.campo, Esmalte) for f in escudos)
