from dataclasses import dataclass
from .esmalte import Esmalte
from .mueble import Mueble
from typing import List

@dataclass(frozen=True)
class Campo:
    esmalte: Esmalte
    muebles: List[Mueble]


    def __post_init__(self):
        if not isinstance(self.esmalte, Esmalte):
            raise TypeError("Campo requiere un Esmalte válido.")
        for m in self.muebles:
            if not isinstance(m, Mueble):
                raise TypeError("Todos los muebles deben ser instancias de Mueble")