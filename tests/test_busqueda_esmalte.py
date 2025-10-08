from heraldica.catalogo import listar
from heraldica.busqueda_esmalte import filtrar_por_esmalte


def test_filtra_por_esmalte_valido():
    fichas = listar()
    r = filtrar_por_esmalte(fichas, "azur")
    assert len(r) >= 1 and all(f.campo.nombre == "azur" for f in r)


def test_sin_criterio_devuelve_todo():
    fichas = listar()
    r = filtrar_por_esmalte(fichas, None)
    assert len(r) == len(fichas)


def test_criterio_no_valido_devuelve_vacio():
    fichas = listar()
    r = filtrar_por_esmalte(fichas, "fucsia")
    assert r == []


def test_mapea_a_canonico():
    fichas = listar()
    r = filtrar_por_esmalte(fichas, "azul")
    assert len(r) >= 1 and all(f.campo.nombre == "azur" for f in r)
