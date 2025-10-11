import pytest
from heraldica.campo import Campo
from heraldica.esmalte import Esmalte
from heraldica.mueble import Mueble


def test_campo_sin_esmalte_rechazado():
    with pytest.raises(TypeError):
        Campo(None)

def test_pieza_heraldica_valida():
    campo = Campo(esmalte=Esmalte("azur"), muebles=[], pieza_heraldica=Esmalte("oro"))
    assert campo.pieza_heraldica.nombre == "oro"

def test_pieza_heraldica_invalida_color():
    with pytest.raises(ValueError):
        Campo(esmalte=Esmalte("azur"), muebles=[], pieza_heraldica=Esmalte("sable")) 

def test_pieza_heraldica_invalida_metal():
    with pytest.raises(ValueError):
        Campo(esmalte=Esmalte("oro"), muebles=[], pieza_heraldica=Esmalte("plata")) 