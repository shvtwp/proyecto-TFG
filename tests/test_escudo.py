from heraldica.esmalte import Esmalte
from heraldica.campo import Campo
from heraldica.escudo import Escudo


def test_escudo_valido_con_campo_azur():
    escudo = Escudo(Campo(Esmalte("azur")))
    assert escudo.campo.esmalte.nombre == "azur"

def test_portador_normalizado():
    escudo = Escudo(
        portador="Díaz de la Rosa",
        campo=Campo(esmalte=Esmalte("azur"), muebles=[])
    )
    
    assert escudo.portador == "diaz de la rosa"

