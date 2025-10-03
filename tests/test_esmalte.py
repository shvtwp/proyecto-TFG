import pytest
from proyectotfg.esmalte import Esmalte
from proyectotfg.campo import Campo
from proyectotfg.escudo import Escudo


@pytest.mark.parametrize("nombre", ["marron", "", "  ", "fucsia"])
def test_esmalte_invalido_impide_crear_escudo(nombre):
    with pytest.raises(ValueError):
        Escudo(Campo(Esmalte(nombre)))
