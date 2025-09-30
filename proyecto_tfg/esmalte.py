from dataclasses import dataclass

_VALIDOS = {"azur", "gules", "sable", "sinople", "púrpura", "oro", "plata"}

_MAPEO = {
    "azul": "azur",
    "rojo": "gules",
    "negro": "sable",
    "verde": "sinople",
    "morado": "púrpura", "violeta": "púrpura", "purpura": "púrpura",
    "amarillo": "oro", "dorado": "oro",
    "blanco": "plata", "plateado": "plata",
}

@dataclass(frozen=True)
class Esmalte:
    nombre: str

    def __post_init__(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ValueError("Esmalte inválido: vacío o no es texto.")
        nombre_normalizado = self.nombre.strip().lower()
        nombre_normalizado = _MAPEO.get(nombre_normalizado, nombre_normalizado)
        if nombre_normalizado not in _VALIDOS:
            raise ValueError(f"Esmalte inválido: '{self.nombre}'.")
        object.__setattr__(self, "nombre", nombre_normalizado)