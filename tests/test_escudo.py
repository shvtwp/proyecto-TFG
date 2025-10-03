from proyectotfg.esmalte import Esmalte
from proyectotfg.campo import Campo
from proyectotfg.escudo import Escudo


def test_escudo_valido_con_campo_azur():
    escudo = Escudo(Campo(Esmalte("azur")))
    assert escudo.campo.esmalte.nombre == "azur"
