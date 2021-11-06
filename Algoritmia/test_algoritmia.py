import pytest
from Algoritmia import canSplit


@pytest.mark.parametrize(
    "matriz, expected",
    [
        ([[1,1],[1,1]],1),
        ([[2,2,4],[2,2,4],[2,2,4]],1),
        ([[1,2,3],[2,3,2]], 0),
        ([[2,3,4,1],[2,3,4,1],[]],1)

    ]
)
def test_multi_canSplit(matriz, expected):
    assert canSplit(matriz) == expected
