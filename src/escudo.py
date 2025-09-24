from .campo import Campo

class Escudo:
    def __init__(self, campo: Campo):
        if not isinstance(campo, Campo):
            raise TypeError("Escudo requiere un Campo válido.")
        self.campo = campo
