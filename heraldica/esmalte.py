from dataclasses import dataclass
import importlib.resources as res
import json

with res.files("data").joinpath("mapeo_esmaltes.json").open("r", encoding="utf-8") as f:
    _CFG = json.load(f)

_VALIDOS: set[str] = {v.lower() for v in _CFG["validos"]}
_MAPEO: dict[str, str] = {
    str(k).lower(): str(v).lower() for k, v in _CFG["mapeo"].items()
}
_TIPOS: dict[str, str] = _CFG["tipos"]  

@dataclass(frozen=True)
class Esmalte:
    nombre: str
    tipo: str  = None

    def __post_init__(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ValueError("Esmalte inválido: vacío o no es texto.")
        nombre_normalizado = self.nombre.strip().lower()
        nombre_normalizado = _MAPEO.get(nombre_normalizado, nombre_normalizado)
        if nombre_normalizado not in _VALIDOS:
            raise ValueError(f"Esmalte inválido: '{self.nombre}'.")
        object.__setattr__(self, "nombre", nombre_normalizado)
        object.__setattr__(self, "tipo", _TIPOS[nombre_normalizado])