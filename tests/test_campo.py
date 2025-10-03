import pytest
from proyectotfg.campo import Campo


def test_campo_sin_esmalte_rechazado():
    with pytest.raises(TypeError):
        Campo(None)
