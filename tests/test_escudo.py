import pytest
from heraldica.esmalte import Esmalte
from heraldica.campo import Campo
from heraldica.escudo import Escudo
from heraldica.adorno import AdornoExterior

def test_escudo_valido_con_campo_azur():
    escudo = Escudo(Campo(Esmalte("azur"), muebles=[]), portador="Desconocido")
    assert escudo.campo.esmalte.nombre == "azur"

def test_portador_normalizado():
    escudo = Escudo(
        portador="Díaz de la Rosa",
        campo=Campo(esmalte=Esmalte("azur"), muebles=[])
    )
    
    assert escudo.portador == "diaz de la rosa"

def test_adorno_valido():
    escudo = Escudo(
        portador="de la rosa",
        campo=Campo(esmalte=Esmalte("azur"), muebles=[]),
        adorno_exterior=AdornoExterior("mitra")
    )
    assert escudo.adorno_exterior.nombre == "mitra"
    assert escudo.adorno_exterior.categoria == "episcopal"

def test_adorno_invalido():
    with pytest.raises(ValueError):
        AdornoExterior("corazon")