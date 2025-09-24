import pytest
from proyecto_tfg.esmalte import Esmalte
from proyecto_tfg.campo import Campo
from proyecto_tfg.escudo import Escudo

def test_escudo_valido_con_campo_azur():
    escudo = Escudo(Campo(Esmalte("azur")))
    assert escudo.campo.esmalte.nombre == "azur"