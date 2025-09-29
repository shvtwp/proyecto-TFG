from dataclasses import dataclass
from typing import List
from .esmalte import Esmalte

@dataclass(frozen=True)
class Ficha:
    nombre: str
    campo: Esmalte

_CATALOGO: List[Ficha] = [
    Ficha("Ejemplo Azur",    Esmalte("azur")),
    Ficha("Ejemplo Gules",   Esmalte("gules")),
    Ficha("Ejemplo Sable",   Esmalte("sable")),
    Ficha("Ejemplo Sinople", Esmalte("sinople")),
    Ficha("Ejemplo Púrpura", Esmalte("púrpura")),
    Ficha("Ejemplo Oro",     Esmalte("oro")),
    Ficha("Ejemplo Plata",   Esmalte("plata")),
]

def listar() -> List[Ficha]:
    return list(_CATALOGO)
