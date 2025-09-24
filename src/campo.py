from .esmalte import Esmalte

class Campo:
    def __init__(self, esmalte: Esmalte):
        if not isinstance(esmalte, Esmalte):
            raise TypeError("Campo requiere un Esmalte válido.")
        self.esmalte = esmalte
