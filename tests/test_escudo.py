import pytest
from src.esmalte import Esmalte
from src.campo import Campo
from src.escudo import Escudo

def test_escudo_valido_con_campo_azur():
    escudo = Escudo(Campo(Esmalte("azur")))
    assert escudo.campo.esmalte.nombre == "azur"

@pytest.mark.parametrize("nombre", ["rojo", "", "  ", "azul"])
def test_esmalte_invalido_impide_crear_escudo(nombre):
    with pytest.raises(ValueError):
        Escudo(Campo(Esmalte(nombre)))

def test_campo_sin_esmalte_rechazado():
    with pytest.raises(TypeError):
        Campo(None)
