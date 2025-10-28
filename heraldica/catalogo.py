from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import json
from .esmalte import Esmalte
from .adorno import AdornoExterior
from .campo import Campo
from .mueble import Mueble
from sqlmodel import select
from .db.session import get_session, crear_bd
from .db.models import Escudo as EscudoTable, Campo as CampoTable, Mueble as MuebleTable


@dataclass(frozen=True)
class Ficha:
    nombre: str
    campo: Campo
    portador: str
    adorno_exterior: Optional[AdornoExterior] = None
    provincia: str = ""
    imagen_src: str = ""


_DATA = Path(__file__).resolve().parents[1] / "data" / "catalogo_demo.json"


def _crear_campo_y_adorno(
    esmalte_nombre: str,
    muebles_nombres: List[str],
    pieza_nombre: Optional[str],
    adorno_nombre: Optional[str],
):
    """Crea objetos Campo y AdornoExterior a partir de nombres.

    Args:
        esmalte_nombre: Nombre del esmalte para el campo
        muebles_nombres: Lista de nombres de muebles
        pieza_nombre: Nombre de la pieza heráldica (opcional)
        adorno_nombre: Nombre del adorno exterior (opcional)

    Returns:
        Tupla con el objeto Campo y el objeto AdornoExterior (o None)
    """
    campo = Campo(
        esmalte=Esmalte(esmalte_nombre),
        muebles=[Mueble(m) for m in muebles_nombres],
        pieza_heraldica=Esmalte(pieza_nombre) if pieza_nombre else None,
    )
    adorno = AdornoExterior(adorno_nombre) if adorno_nombre else None
    return campo, adorno


def listar() -> List[Ficha]:
    with _DATA.open(encoding="utf-8") as f:
        catalogo = json.load(f)

    fichas = []
    for item in catalogo:
        campo, adorno = _crear_campo_y_adorno(
            esmalte_nombre=item["campo"],
            muebles_nombres=item.get("muebles", []),
            pieza_nombre=item.get("pieza_heraldica"),
            adorno_nombre=item.get("adorno_exterior"),
        )
        fichas.append(
            Ficha(
                nombre=item["nombre"],
                campo=campo,
                portador=item["portador"].strip().lower(),
                adorno_exterior=adorno,
                provincia=item.get("provincia", ""),
                imagen_src=item.get("imagen_src", ""),
            )
        )
    return fichas


class Catalogo:
    def __init__(self) -> None:
        self._fichas: List[Ficha] = listar()

    def filtrar_por_esmalte(self, campo: Optional[str]) -> List[Ficha]:
        if campo is None or (isinstance(campo, str) and not campo.strip()):
            return list(self._fichas)

        try:
            canon = Esmalte(campo).nombre
        except ValueError:
            return []

        return [
            f for f in self._fichas if getattr(f.campo.esmalte, "nombre", None) == canon
        ]

    def filtrar_por_portador(self, portador: Optional[str]):
        if not portador or not portador.strip():
            return list(self._fichas)
        canon = portador.strip().lower()
        return [f for f in self._fichas if canon in f.portador]

    def filtrar_por_mueble(self, nombre: str):
        canon = nombre.strip().lower()
        return [
            f for f in self._fichas if any(m.nombre == canon for m in f.campo.muebles)
        ]

    def filtrar_por_pieza(self, nombre: str):
        canon = nombre.strip().lower()
        return [
            f
            for f in self._fichas
            if f.campo.pieza_heraldica and f.campo.pieza_heraldica.nombre == canon
        ]

    def filtrar_por_adorno(self, nombre: str):
        canon = nombre.strip().lower()
        return [
            f
            for f in self._fichas
            if f.adorno_exterior and f.adorno_exterior.nombre == canon
        ]

    def _listar_desde_bd(self) -> List[Ficha]:
        crear_bd()
        fichas: List[Ficha] = []
        with get_session() as s:
            filas = s.exec(
                select(EscudoTable, CampoTable).join(
                    CampoTable, EscudoTable.campo_id == CampoTable.id
                )
            ).all()

            campo_ids = [c.id for (_, c) in filas]
            muebles_rows = []
            if campo_ids:
                muebles_rows = s.exec(
                    select(MuebleTable).where(MuebleTable.campo_id.in_(campo_ids))
                ).all()

            muebles_por_campo: dict[int, list[str]] = {}
            for m in muebles_rows:
                muebles_por_campo.setdefault(m.campo_id, []).append(m.nombre)

            for esc_db, campo_db in filas:
                campo, adorno = _crear_campo_y_adorno(
                    esmalte_nombre=campo_db.esmalte,
                    muebles_nombres=muebles_por_campo.get(campo_db.id, []),
                    pieza_nombre=campo_db.pieza_heraldica,
                    adorno_nombre=esc_db.adorno_exterior,
                )
                fichas.append(
                    Ficha(
                        nombre=esc_db.nombre,
                        campo=campo,
                        portador=esc_db.portador,
                        adorno_exterior=adorno,
                        provincia=getattr(esc_db, "provincia", ""),
                        imagen_src=getattr(esc_db, "imagen_src", ""),
                    )
                )
        return fichas

    def recargar_desde_bd(self) -> None:
        self._fichas = self._listar_desde_bd()
