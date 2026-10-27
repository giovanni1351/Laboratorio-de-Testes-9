import pytest

from classificacao import classificar_aluno


@pytest.mark.parametrize(
    "media,presenca,esperado",
    [
        (7.0, 75, "Aprovado"),
        (10.0, 100, "Aprovado"),
        (5.0, 80, "Recuperacao"),
        (6.99, 80, "Recuperacao"),
        (0.0, 80, "Reprovado"),
        (4.99, 80, "Reprovado"),
        (8.0, 0, "Reprovado por falta"),
        (8.0, 74.99, "Reprovado por falta"),
    ],
)
def test_classificar_aluno(media, presenca, esperado):
    assert classificar_aluno(media=media, presenca=presenca) == esperado


@pytest.mark.parametrize(
    "media,presenca,msg",
    [(-0.01, 80, "Media invalida"), (10.01, 80, "Media invalida"),
     (8.0, -1, "Presenca invalida"), (8.0, 101, "Presenca invalida")],
)
def test_entradas_invalidas(media, presenca, msg):
    with pytest.raises(ValueError, match=msg):
        classificar_aluno(media, presenca)
