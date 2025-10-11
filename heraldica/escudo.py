from dataclasses import dataclass
from .campo import Campo
import unicodedata

def normalizar_texto(texto: str) -> str:
    return unicodedata.normalize('NFKD', texto.strip().lower()).encode('ascii', 'ignore').decode('ascii')

@dataclass(frozen=True)
class Escudo:
    campo: Campo
    portador: str

    def __post_init__(self):
        if not isinstance(self.campo, Campo):
            raise TypeError("Escudo requiere un Campo válido.")
        object.__setattr__(self, "portador", normalizar_texto(self.portador))