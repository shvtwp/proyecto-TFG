from heraldica.esmalte import Esmalte
from heraldica.campo import Campo
from heraldica.escudo import Escudo


def test_escudo_valido_con_campo_azur():
    escudo = Escudo(Campo(Esmalte("azur")))
    assert escudo.campo.esmalte.nombre == "azur"
