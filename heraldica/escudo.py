from dataclasses import dataclass
from .campo import Campo
import unicodedata
from typing import Optional
from .adorno import AdornoExterior


def normalizar_texto(texto: str) -> str:
    return (
        unicodedata.normalize("NFKD", texto.strip().lower())
        .encode("ascii", "ignore")
        .decode("ascii")
    )


@dataclass(frozen=True)
class Escudo:
    campo: Campo
    portador: str
    adorno_exterior: Optional[AdornoExterior] = None

    def __post_init__(self):
        if not isinstance(self.campo, Campo):
            raise TypeError("Escudo requiere un Campo válido.")
        object.__setattr__(self, "portador", normalizar_texto(self.portador))
        if self.adorno_exterior and not isinstance(
            self.adorno_exterior, AdornoExterior
        ):
            raise TypeError("adorno_exterior debe ser AdornoExterior o None")
