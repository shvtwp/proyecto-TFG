from dataclasses import dataclass
import importlib.resources as res
import json

# Leemos JSON de adornos
with res.files("data").joinpath("adornos_exteriores.json").open("r", encoding="utf-8") as f:
    _CFG = json.load(f)

_VALIDOS = set(_CFG["validos"])
_CATEGORIAS = _CFG["categorias"]

@dataclass(frozen=True)
class AdornoExterior:
    nombre: str
    categoria: str = None

    def __post_init__(self):
        canon = self.nombre.strip().lower()
        if canon not in _VALIDOS:
            raise ValueError(f"Adorno inválido: {self.nombre}")
        object.__setattr__(self, "nombre", canon)
        object.__setattr__(self, "categoria", _CATEGORIAS[canon])
