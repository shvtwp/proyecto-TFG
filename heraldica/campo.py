from dataclasses import dataclass
from .esmalte import Esmalte
from .mueble import Mueble
from typing import List, Optional

@dataclass(frozen=True)
class Campo:
    esmalte: Esmalte
    muebles: List[Mueble]
    pieza_heraldica: Optional[Esmalte] = None

    def __post_init__(self):
        if not isinstance(self.esmalte, Esmalte):
            raise TypeError("Campo requiere un Esmalte válido.")
        for m in self.muebles:
            if not isinstance(m, Mueble):
                raise TypeError("Todos los muebles deben ser instancias de Mueble")
            
        if self.pieza_heraldica:
            if not isinstance(self.pieza_heraldica, Esmalte):
                raise TypeError("pieza_heraldica debe ser un Esmalte válido")

            tipo_campo = self.esmalte.tipo
            tipo_pieza = self.pieza_heraldica.tipo
            if tipo_campo == tipo_pieza:
                raise ValueError(f"pieza_heraldica {self.pieza_heraldica.nombre} no puede estar sobre {self.esmalte.nombre}")