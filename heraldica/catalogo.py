from dataclasses import dataclass
from typing import List, Optional, Callable, Dict, Any
from pathlib import Path
import json
from .esmalte import Esmalte
from .adorno import AdornoExterior
from .campo import Campo
from .mueble import Mueble
from sqlmodel import select, Session
from .db.models import Escudo as EscudoTable, Campo as CampoTable, Mueble as MuebleTable


@dataclass(frozen=True)
class Ficha:
    nombre: str
    campo: Campo
    portador: str
    adorno_exterior: Optional[AdornoExterior] = None
    provincia: str = ""
    imagen_src: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la Ficha a una representación en diccionario para la interfaz de usuario."""
        campo = self.campo

        return {
            "nombre": self.nombre or "",
            "campo": getattr(campo.esmalte, "nombre", ""),
            "muebles": [m.nombre for m in campo.muebles] if campo.muebles else [],
            "pieza_heraldica": getattr(campo.pieza_heraldica, "nombre", ""),
            "portador": self.portador or "",
            "adorno_exterior": getattr(self.adorno_exterior, "nombre", ""),
            "provincia": self.provincia or "",
            "imagen_src": self.imagen_src or "",
        }


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
    _instance: Optional["Catalogo"] = None
    _session_factory: Optional[Callable[[], Session]] = None

    def __new__(cls, session_factory: Optional[Callable[[], Session]] = None):
        """Singleton implementation with optional session factory injection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        if session_factory is not None:
            cls._session_factory = session_factory
        return cls._instance

    def __init__(self, session_factory: Optional[Callable[[], Session]] = None) -> None:
        """Initialize the catalog. Only runs once due to singleton pattern."""
        if self._initialized:
            return
        self._initialized = True
        if session_factory is not None:
            self._session_factory = session_factory
        self._fichas: List[Ficha] = listar()
        self._cargar_opciones_filtros()

    @classmethod
    def set_session_factory(cls, session_factory: Callable[[], Session]) -> None:
        """Set the session factory for database operations."""
        cls._session_factory = session_factory

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None
        cls._session_factory = None

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

    def _cargar_opciones_filtros(self):
        """Load filter options from JSON files."""
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

    def obtener_esmaltes(self) -> List[str]:
        """Get list of valid esmaltes for filtering."""
        return self.esmaltes

    def obtener_muebles(self) -> List[str]:
        """Get list of valid muebles for filtering."""
        return self.muebles

    def obtener_adornos(self) -> List[str]:
        """Get list of valid adornos for filtering."""
        return self.adornos

    def obtener_todos(self) -> List[Dict[str, Any]]:
        """Get all fichas as dictionaries."""
        return [f.to_dict() for f in self._fichas]

    def buscar_combinada(
        self, texto: str = "", esmalte: str = "", mueble: str = "", adorno: str = ""
    ) -> List[Dict[str, Any]]:
        """Perform combined search with multiple filters.

        Args:
            texto: Free text search
            esmalte: Filter by esmalte
            mueble: Filter by mueble
            adorno: Filter by adorno exterior

        Returns:
            List of fichas as dictionaries matching all filters
        """
        resultados = list(self._fichas)

        if texto and texto.strip():
            try:
                esmalte_normalizado = Esmalte(texto).nombre

                por_esmalte = [
                    f
                    for f in resultados
                    if getattr(f.campo.esmalte, "nombre", "").lower()
                    == esmalte_normalizado.lower()
                ]
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
                or (
                    f.campo.pieza_heraldica
                    and texto_lower
                    in getattr(f.campo.pieza_heraldica, "nombre", "").lower()
                )
                or (
                    f.adorno_exterior
                    and texto_lower in f.adorno_exterior.nombre.lower()
                )
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

        return [f.to_dict() for f in resultados]

    def listar_desde_bd(self) -> List[Ficha]:
        """Load catalog entries from database using injected session factory."""
        if self._session_factory is None:
            # Fallback to default session if not injected
            from .db.session import get_session, crear_bd

            crear_bd()
            session_factory = get_session
        else:
            session_factory = self._session_factory

        fichas: List[Ficha] = []
        with session_factory() as s:
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
        self._fichas = fichas
        return fichas
