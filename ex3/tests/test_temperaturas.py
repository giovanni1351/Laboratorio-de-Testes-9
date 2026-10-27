import pytest

from temperaturas import dia_do_maior, maior


@pytest.mark.parametrize(
    "temps,esperado",
    [([21, 25, 19, 30, 22], 30), ([18], 18), ([30, 21], 30)],
)
def test_maior(temps, esperado):
    assert maior(temps) == esperado


@pytest.mark.parametrize(
    "temps,esperado",
    [([21, 25, 19, 30, 22], 3), ([18], 0), ([30, 21], 0)],
)
def test_dia_do_maior(temps, esperado):
    assert dia_do_maior(temps) == esperado


@pytest.mark.parametrize("funcao", [maior, dia_do_maior])
def test_lista_vazia(funcao):
    with pytest.raises(ValueError, match="^lista vazia$"):
        funcao([])


def test_maior_no_segundo_elemento():
    assert maior([10, 30, 20]) == 30
    assert dia_do_maior([10, 30, 20]) == 1


def test_dia_do_maior_retorna_o_primeiro_em_caso_de_empate():
    assert maior([30, 30, 20]) == 30
    assert dia_do_maior([30, 30, 20]) == 0
