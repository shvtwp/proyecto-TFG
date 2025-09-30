import pytest
from proyecto_tfg.esmalte import Esmalte
from proyecto_tfg.campo import Campo
from proyecto_tfg.escudo import Escudo

@pytest.mark.parametrize("nombre", ["marron", "", "  ", "fucsia"])
def test_esmalte_invalido_impide_crear_escudo(nombre):
    with pytest.raises(ValueError):
        Escudo(Campo(Esmalte(nombre)))
