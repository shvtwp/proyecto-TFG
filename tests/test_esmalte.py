import pytest
from heraldica.esmalte import Esmalte
from heraldica.campo import Campo
from heraldica.escudo import Escudo


@pytest.mark.parametrize("nombre", ["marron", "", "  ", "fucsia"])
def test_esmalte_invalido_impide_crear_escudo(nombre):
    with pytest.raises(ValueError):
        Escudo(Campo(Esmalte(nombre)))
