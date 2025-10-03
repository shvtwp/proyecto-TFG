from dataclasses import dataclass
from typing import List
from pathlib import Path
import json
from .esmalte import Esmalte


@dataclass(frozen=True)
class Ficha:
    nombre: str
    campo: Esmalte


_DATA = Path(__file__).resolve().parents[1] / "data" / "catalogo_demo.json"


def listar() -> List[Ficha]:
    with _DATA.open(encoding="utf-8") as f:
        catalogo = json.load(f)
    return [Ficha(item["nombre"], Esmalte(item["campo"])) for item in catalogo]
