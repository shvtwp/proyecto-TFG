_VALIDOS = {"azur", "gules", "sable", "sinople", "púrpura", "oro", "plata"}

class Esmalte:
    def __init__(self, nombre: str):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Esmalte inválido: vacío o no es texto.")
        normal = nombre.strip().lower()
        if normal not in _VALIDOS:
            raise ValueError(f"Esmalte inválido: '{nombre}'.")
        self.nombre = normal
