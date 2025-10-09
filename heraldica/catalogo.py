from dataclasses import dataclass
from typing import List
from pathlib import Path
import json
from .esmalte import Esmalte
from typing import Optional, Union


@dataclass(frozen=True)
class Ficha:
    nombre: str
    campo: Esmalte


_DATA = Path(__file__).resolve().parents[1] / "data" / "catalogo_demo.json"


def listar() -> List[Ficha]:
    with _DATA.open(encoding="utf-8") as f:
        catalogo = json.load(f)
    return [Ficha(item["nombre"], Esmalte(item["campo"])) for item in catalogo]

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
        
        return [f for f in self._fichas if getattr(f.campo, "nombre", None) == canon]
