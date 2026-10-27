import pytest

from parcelamento import parcela


@pytest.mark.parametrize("n", [0, 13])
def test_quantidade_de_parcelas_invalida(n):
    with pytest.raises(ValueError, match="^parcelas invalidas$"):
        parcela(1200, n)


@pytest.mark.parametrize(
    "n,esperado",
    [(1, 1200.0), (2, 600.0), (3, 400.0), (4, 306.0), (11, 126.55), (12, 118.0)],
)
def test_parcela_nos_limites(n, esperado):
    assert parcela(1200, n) == esperado
