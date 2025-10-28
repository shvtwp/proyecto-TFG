from __future__ import annotations
from typing import Any, Dict, List
from heraldica.catalogo import Catalogo


def _to_str(x: Any) -> str:
    if x is None:
        return ""

    if hasattr(x, "nombre"):
        v = getattr(x, "nombre")
        return "" if v is None else str(v)
    return str(x)


def _to_list_str(xs: Any) -> List[str]:
    if not xs:
        return []
    result = []
    for x in xs:
        s = _to_str(x)
        if s:
            result.append(s)
    return result


def _campo_to_str(campo_obj: Any) -> str:
    """
    Campo -> texto. Si Campo.esmalte existe y tiene nombre, devolver ese nombre (ej. 'gules').
    Acepta también strings o dicts.
    """
    if campo_obj is None:
        return ""
    if isinstance(campo_obj, dict):
        if "esmalte" in campo_obj:
            e = campo_obj["esmalte"]
            if isinstance(e, dict) and "nombre" in e:
                return str(e["nombre"])
            return _to_str(e)
        if "nombre" in campo_obj:
            return str(campo_obj["nombre"])
        return _to_str(campo_obj)
    if isinstance(campo_obj, str):
        return campo_obj
    if hasattr(campo_obj, "esmalte"):
        e = getattr(campo_obj, "esmalte")
        if hasattr(e, "nombre"):
            return str(getattr(e, "nombre"))
        return _to_str(e)
    if hasattr(campo_obj, "nombre"):
        return str(getattr(campo_obj, "nombre"))

    return _to_str(campo_obj)


def _normalize_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "nombre": _to_str(d.get("nombre")),
        "campo": _campo_to_str(d.get("campo")),
        "muebles": _to_list_str(d.get("muebles")),
        "pieza_heraldica": _to_str(d.get("pieza_heraldica")),
        "portador": _to_str(d.get("portador")),
        "adorno_exterior": _to_str(d.get("adorno_exterior")),
        "provincia": _to_str(d.get("provincia")),
        "imagen_src": _to_str(d.get("imagen_src")),
    }


def _to_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
        raw = obj.to_dict()
        return _normalize_dict(raw)

    # Acceder correctamente a la estructura de Ficha
    campo_obj = getattr(obj, "campo", None)

    d = {
        "nombre": getattr(obj, "nombre", ""),
        "campo": campo_obj,
        "muebles": getattr(campo_obj, "muebles", []) if campo_obj else [],
        "pieza_heraldica": getattr(campo_obj, "pieza_heraldica", None)
        if campo_obj
        else None,
        "portador": getattr(obj, "portador", ""),
        "adorno_exterior": getattr(obj, "adorno_exterior", None),
        "provincia": getattr(obj, "provincia", ""),
        "imagen_src": getattr(obj, "imagen_src", None),
    }
    return _normalize_dict(d)


class CatalogoUI:
    def __init__(self) -> None:
        self._cat = Catalogo()
        self._cat.recargar_desde_bd()

    def _aplicar_filtro(self, metodo_filtro, *args):
        """Aplica un método de filtro del catálogo y convierte los resultados a diccionarios."""
        return [_to_dict(x) for x in metodo_filtro(*args)]

    def filtrar_por_esmalte(self, esmalte: str):
        return self._aplicar_filtro(self._cat.filtrar_por_esmalte, esmalte)

    def filtrar_por_mueble(self, mueble: str):
        return self._aplicar_filtro(self._cat.filtrar_por_mueble, mueble)

    def filtrar_por_pieza(self, pieza: str):
        return self._aplicar_filtro(self._cat.filtrar_por_pieza, pieza)

    def filtrar_por_adorno(self, adorno: str):
        return self._aplicar_filtro(self._cat.filtrar_por_adorno, adorno)

    def filtrar_por_portador(self, portador: str):
        return self._aplicar_filtro(self._cat.filtrar_por_portador, portador)

    def obtener_todos(self):
        """Devuelve todos los escudos del catálogo"""
        return [_to_dict(x) for x in self._cat._fichas]

    def buscar_libre(self, q: str):
        if not q:
            return self.obtener_todos()

        buckets = [
            self.filtrar_por_esmalte(q),
            self.filtrar_por_mueble(q),
            self.filtrar_por_pieza(q),
            self.filtrar_por_adorno(q),
            self.filtrar_por_portador(q),
        ]
        seen, out = set(), []
        for b in buckets:
            for r in b:
                k = r.get("nombre")
                if k not in seen:
                    seen.add(k)
                    out.append(r)
        return out
