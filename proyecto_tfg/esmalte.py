from dataclasses import dataclass

_VALIDOS = {"azur", "gules", "sable", "sinople", "púrpura", "oro", "plata"}

@dataclass(frozen=True)
class Esmalte:
    nombre: str

    def __post_init__(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ValueError("Esmalte inválido: vacío o no es texto.")
        nombre_normalizado = self.nombre.strip().lower()
        if nombre_normalizado not in _VALIDOS:
            raise ValueError(f"Esmalte inválido: '{self.nombre}'.")
        object.__setattr__(self, "nombre", nombre_normalizado)