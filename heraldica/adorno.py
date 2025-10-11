from dataclasses import dataclass
import json
import importlib.resources as res

with res.files("data").joinpath("adornos_exteriores.json").open("r", encoding="utf-8") as f:
    _CFG = json.load(f)  # {"validos": [...], "categorias": {"mitra":"episcopal", ...}}

VALIDOS = set(_CFG["validos"])
CATEGORIAS = _CFG["categorias"]

@dataclass(frozen=True)
class AdornoExterior:
    nombre: str
    categoria: str

    def __post_init__(self):
        canon = self.nombre.strip().lower()
        if canon not in VALIDOS:
            raise ValueError(f"Adorno inválido: {self.nombre}")
        object.__setattr__(self, "nombre", canon)
        object.__setattr__(self, "categoria", CATEGORIAS[canon])
