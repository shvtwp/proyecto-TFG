from heraldica.catalogo import listar, Ficha, Catalogo
from heraldica.esmalte import Esmalte
from heraldica.campo import Campo


def test_catalogo_no_vacio_y_usa_esmalte():
    escudos = listar()
    assert len(escudos) >= 1
    assert all(isinstance(f, Ficha) for f in escudos)
    assert all(isinstance(f.campo, Campo) for f in escudos)
    assert all(isinstance(f.campo.esmalte, Esmalte) for f in escudos)


def test_filtra_por_esmalte_valido():
    cat = Catalogo()
    r = cat.filtrar_por_esmalte("azur")
    assert len(r) >= 1 and all(f.campo.esmalte.nombre == "azur" for f in r)


def test_sin_criterio_devuelve_todo():
    cat = Catalogo()
    r = cat.filtrar_por_esmalte(None)
    assert len(r) == len(cat._fichas)


def test_criterio_no_valido_devuelve_vacio():
    cat = Catalogo()
    r = cat.filtrar_por_esmalte("fucsia")
    assert r == []


def test_mapea_a_canonico():
    cat = Catalogo()
    r = cat.filtrar_por_esmalte("azul")
    assert len(r) >= 1 and all(f.campo.esmalte.nombre == "azur" for f in r)


def test_filtra_por_portador():
    cat = Catalogo()
    r = cat.filtrar_por_portador("desconocido")
    assert all("desconocido" in f.portador for f in r)


def test_filtra_por_mueble():
    cat = Catalogo()
    r = cat.filtrar_por_mueble("leon")
    assert all(any(m.nombre == "leon" for m in f.campo.muebles) for f in r)


def test_filtra_por_pieza_heraldica():
    cat = Catalogo()
    r = cat.filtrar_por_pieza("oro")
    assert all(f.campo.pieza_heraldica.nombre == "oro" for f in r)


def test_filtra_por_adorno():
    cat = Catalogo()
    r = cat.filtrar_por_adorno("mitra")
    assert all(f.adorno_exterior.nombre == "mitra" for f in r)
