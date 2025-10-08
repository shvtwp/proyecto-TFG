from dataclasses import dataclass
from .esmalte import Esmalte


@dataclass(frozen=True)
class Campo:
    esmalte: Esmalte

    def __post_init__(self):
        if not isinstance(self.esmalte, Esmalte):
            raise TypeError("Campo requiere un Esmalte válido.")
