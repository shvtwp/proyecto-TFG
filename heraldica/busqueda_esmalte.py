from typing import Iterable, List, Optional
from .catalogo import Ficha
from .esmalte import Esmalte


def filtrar_por_esmalte(fichas: Iterable[Ficha], campo: Optional[str]) -> List[Ficha]:
    if campo is None or (isinstance(campo, str) and not campo.strip()):
        return list(fichas)

    try:
        canon = Esmalte(campo).nombre
    except ValueError:
        return []

    return [f for f in fichas if f.campo.nombre == canon]
