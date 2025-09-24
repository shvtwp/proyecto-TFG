from dataclasses import dataclass
from .campo import Campo

@dataclass(frozen=True)
class Escudo:
    campo: Campo

    def __post_init__(self):
        if not isinstance(self.campo, Campo):
            raise TypeError("Escudo requiere un Campo válido.")