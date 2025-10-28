from __future__ import annotations
from typing import Any, Dict, List
from heraldica.catalogo import Catalogo
import json
from pathlib import Path


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
        self._cargar_opciones_filtros()

    def _cargar_opciones_filtros(self):
        data_dir = Path(__file__).resolve().parents[1] / "data"

        esmaltes_path = data_dir / "mapeo_esmaltes.json"
        with esmaltes_path.open(encoding="utf-8") as f:
            esmaltes_data = json.load(f)
            self.esmaltes = esmaltes_data.get("validos", [])

        muebles_path = data_dir / "muebles.json"
        with muebles_path.open(encoding="utf-8") as f:
            muebles_data = json.load(f)
            self.muebles = list(muebles_data.keys())

        adornos_path = data_dir / "adornos_exteriores.json"
        with adornos_path.open(encoding="utf-8") as f:
            adornos_data = json.load(f)
            self.adornos = adornos_data.get("validos", [])

    def obtener_esmaltes(self):
        return self.esmaltes

    def obtener_muebles(self):
        return self.muebles

    def obtener_adornos(self):
        return self.adornos

    def filtrar_por_esmalte(self, esmalte: str):
        return [_to_dict(x) for x in self._cat.filtrar_por_esmalte(esmalte)]

    def filtrar_por_mueble(self, mueble: str):
        return [_to_dict(x) for x in self._cat.filtrar_por_mueble(mueble)]

    def filtrar_por_pieza(self, pieza: str):
        return [_to_dict(x) for x in self._cat.filtrar_por_pieza(pieza)]

    def filtrar_por_adorno(self, adorno: str):
        return [_to_dict(x) for x in self._cat.filtrar_por_adorno(adorno)]

    def filtrar_por_portador(self, portador: str):
        return [_to_dict(x) for x in self._cat.filtrar_por_portador(portador)]

    def obtener_todos(self):
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

    def buscar_combinada(
        self, texto: str = "", esmalte: str = "", mueble: str = "", adorno: str = ""
    ) -> List[Dict[str, Any]]:
        resultados = list(self._cat._fichas)

        if texto and texto.strip():

            try:
                from heraldica.esmalte import Esmalte
                esmalte_normalizado = Esmalte(texto).nombre
                
                por_esmalte = [f for f in resultados 
                            if getattr(f.campo.esmalte, "nombre", "").lower() == esmalte_normalizado.lower()]
            except ValueError:
                por_esmalte = []

            texto_lower = texto.strip().lower()
            por_texto = [
                f
                for f in resultados
                if texto_lower in f.nombre.lower()
                or texto_lower in f.portador.lower()
                or (f.provincia and texto_lower in f.provincia.lower())
                or getattr(f.campo.esmalte, "nombre", "").lower() == texto_lower
                or any(texto_lower in m.nombre.lower() for m in f.campo.muebles)
                or (f.campo.pieza_heraldica and texto_lower in getattr(f.campo.pieza_heraldica, "nombre", "").lower())
                or (f.adorno_exterior and texto_lower in f.adorno_exterior.nombre.lower())
            ]

            vistos = set()
            resultados_finales = []
            for f in por_esmalte + por_texto:
                if f.nombre not in vistos:
                    vistos.add(f.nombre)
                    resultados_finales.append(f)
            resultados = resultados_finales

        if esmalte and esmalte.strip():
            esmalte_canon = esmalte.strip().lower()
            resultados = [
                f
                for f in resultados
                if getattr(f.campo.esmalte, "nombre", "").lower() == esmalte_canon
            ]

        if mueble and mueble.strip():
            mueble_canon = mueble.strip().lower()
            resultados = [
                f
                for f in resultados
                if any(m.nombre.lower() == mueble_canon for m in f.campo.muebles)
            ]

        if adorno and adorno.strip():
            adorno_canon = adorno.strip().lower()
            resultados = [
                f
                for f in resultados
                if f.adorno_exterior
                and f.adorno_exterior.nombre.lower() == adorno_canon
            ]

        return [_to_dict(f) for f in resultados]
