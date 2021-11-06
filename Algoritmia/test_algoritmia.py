import pytest
from Algoritmia import canSplit


@pytest.mark.parametrize(
    "matriz, expected",
    # Casos de prueba
    # es una lista de tuplas, donde cada tupla es una prueba que se hara
    # dicha tupla tiene el siguiente formato (matriz, resultado esperado)
    [
        ([[1,1],[1,1]],1),
        ([[2,2,4],[2,2,4],[2,2,4]],1),
        ([[1,2,3],[2,3,2]], 0),
        ([[2,3,4,1],[2,3,4,1],[]],0)

    ]
)
def test_multi_canSplit(matriz, expected):
    assert canSplit(matriz) == expected
