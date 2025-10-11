from dataclasses import dataclass
import importlib.resources as res
import json

with res.files("data").joinpath("muebles.json").open("r", encoding="utf-8") as f:
    MUEBLES_VALIDOS = json.load(f)


@dataclass(frozen=True)
class Mueble:
    nombre: str

    def __post_init__(self):
        canon = self.nombre.strip().lower()
        if canon not in MUEBLES_VALIDOS:
            raise ValueError(f"Mueble inválido: {self.nombre}")
        object.__setattr__(self, "nombre", canon)
