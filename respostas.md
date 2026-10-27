# Lab 09 - Testes de Mutação

Usei `MS = mortos / (gerados - equivalentes)`.

# Ex 1

## a)

Com os 2 testes iniciais:

- cobertura de ramos: **64%**
- linhas que nem rodaram: **3, 5, 7 e 11**
- gerados: **36**
- mortos: **6**
- vivos: **30**
- MS = 6/36 = **16,67%**

## b)

Agrupei os vivos assim:

- **linha 2, mutantes 1-5:** não testei média inválida nem os limites 0 e 10.
- **linha 3, mutantes 6-9:** linha nem executada. São mudanças na msg `"Media invalida"`.
- **linha 4, mutantes 10-14:** não testei presença inválida nem os limites 0 e 100.
- **linha 5, mutantes 15-18:** linha nem executada. Mudanças na msg `"Presenca invalida"`.
- **linha 6, mutantes 19-20:** faltou testar o limite de presença 75.
- **linha 7, mutantes 21-23:** linha nem executada. Mudanças no retorno `"Reprovado por falta"`.
- **linha 8, mutantes 24-25:** faltou o limite de média 7.
- **linha 10, mutantes 29-30:** faltou o limite de média 5.
- **linha 11, mutantes 31-33:** linha nem executada. Mudanças no retorno `"Recuperacao"`.

Então **14 vivos** estavam em linhas não executadas: **6-9, 15-18, 21-23 e 31-33**. Os outros 16 executaram, mas os testes não pegavam o erro.

## c)

Coloquei testes pros limites de média e presença, valores inválidos, falta, recuperação e msgs de erro.

Com a comparação exata da msg (`str(exc_info.value) == msg`), ficou:

- 36 mortos
- 0 vivos
- nenhum equivalente
- **MS = 36/36 = 100%**
- cobertura de ramos = **100%**

## d)

Trocando pra `pytest.raises(ValueError, match=msg)`, ficou menor e já confere tipo + msg.

Só que `match` procura o texto dentro da msg, não compara a string inteira. Por isso voltaram 2 vivos:

- mutante 7: `"XXMedia invalidaXX"`
- mutante 16: `"XXPresenca invalidaXX"`

Resultado: **34 mortos, 2 vivos, MS bruto = 94,44%**. Pra não deixar isso passar teria que usar algo como `match=f"^{msg}$"`.

# Ex 2

## a)

O teste era só `total_com_desconto(...) > 0`.

- cobertura de ramos: **100%**
- 16 gerados, 4 mortos e 12 vivos
- **MS = 4/16 = 25%**

Ou seja, rodou tudo, mas o assert era fraco. Cobertura alta não quer dizer que o teste confere direito o resultado.

## b)

O valor certo da entrada é:

`10 + 20 + 30 + 40*0.9 + 50*0.9 = 141.0`

Troquei só o assert pra `== 141.0`. Ficaram **3 vivos**: 13, 15 e 16. Deram **13 mortos**, então MS = **81,25%**.

## c)

Os 3 vivos mexem no `round`:

- 13: `round(total, 2)` -> `round(total, None)`
- 15: `round(total, 2)` -> `round(total)`
- 16: `round(total, 2)` -> `round(total, 3)`

Nos 3, a parte alcançada. O problema foi **infectar**: como o total era 141.0, arredondar com 0, 2 ou 3 casas dava o mesmo valor. Sem diferença no estado, não tinha erro pra propagar e revelar.

## d)

Adicionei:

`total_com_desconto([0, 0, 0, 0.01]) == 0.01`

No quarto item dá `0.01 * 0.9 = 0.009`, aí o arredondamento faz diferença. Precisava de um **preço quebrado**, que gerasse mais de 2 casas depois do desconto.

Final: **16/16 mortos, MS = 100%** e cobertura de ramos continuou em 100%.

# Ex 3

## a)

Fiz os testes com `[21, 25, 19, 30, 22]`, `[18]`, `[30, 21]` e lista vazia.

A cobertura deu 100%, mas o mutmut deu **22 gerados, 11 mortos e 11 vivos**.

Vivos que apareceram no `mutmut show`:

- `maior_2`, `maior_3`, `maior_4`: mudam a msg da lista vazia.
- `maior_7`: `temps[1:]` -> `temps[2:]`.
- `maior_8`: `>` -> `>=`.
- `dia_do_maior_2`, `dia_do_maior_3`, `dia_do_maior_4`: mudam a msg da lista vazia.
- `dia_do_maior_9`: `range(1, len(temps))` -> `range(len(temps))`.
- `dia_do_maior_11`: começa no índice 2 em vez de 1.
- `dia_do_maior_12`: `>` -> `>=`.

## b)

**Equivalentes:**

- `maior_8`: se as temps forem iguais, trocar `m` pelo mesmo valor não muda o retorno.
- `dia_do_maior_9`: a iteração extra compara `temps[0] > temps[0]`, que sempre é falso. Não muda `pos`.

**Não equivalentes:**

- os 6 mutantes de msg: mudam a msg esperada.
- `maior_7`: pula o segundo item. Em `[10, 30, 20]` retorna 10, mas devia ser 30.
- `dia_do_maior_11`: pula a posição 1. Em `[10, 30, 20]` retorna 0, mas devia ser 1.
- `dia_do_maior_12`: em empate pega o último máximo. Em `[30, 30, 20]` retorna 1, mas devia retornar o primeiro, posição 0.

## c)

Adicionei teste da msg, máximo no segundo elemento e máximos repetidos.

- MS antes, sem descontar eq: 11/22 = **50%**
- MS antes, descontando os 2 eq: 11/(22-2) = **55%**
- depois: 20 mortos e só os 2 eq vivos
- **MS final = 20/(22-2) = 100%**

## d)

Em `maior`, `>` virar `>=` não muda nada porque num empate o valor continua igual.

Em `dia_do_maior` muda, porque o retorno é a posição. Com `>=`, num empate ele escolhe o último dia, mas o enunciado pede o primeiro.

# Ex 4

## a)

Usei valor 1200 e testes nos limites de `n`:

| n | motivo | esperado |
|---:|---|---:|
| 0 | abaixo do mínimo | ValueError |
| 1 | mínimo válido | 1200.00 |
| 2 | caso sem juros | 600.00 |
| 3 | último sem juros | 400.00 |
| 4 | primeiro com juros | 306.00 |
| 11 | quase no máximo + arredondamento | 126.55 |
| 12 | máximo válido | 118.00 |
| 13 | acima do máximo | ValueError |

Também conferi a msg `"parcelas invalidas"` nos casos inválidos.

## b)

- cobertura de ramos: **100%**
- 27 gerados, 25 mortos e 2 vivos
- MS bruto = 25/27 = **92,59%**

## c)

Vivos:

- **mutante 7:** msg virou `"XXparcelas invalidasXX"`. Não é eq. Ele passou porque `match` acha substring. Coloquei `^parcelas invalidas$` e matei.
- **mutante 9:** `n <= 3` virou `n < 3`. É **equivalente**. Só muda o caminho quando `n = 3`, mas no else dá `0.02 * (3-3) = 0`, então o resultado continua igual.

Final: **26 mortos e 1 eq vivo**.

**MS = 26/(27-1) = 100%.**

## d)

Juntei 2 mutantes de 1ª ordem que os testes já matavam: `n > 12` -> `n >= 12` e juros `0.02` -> `0.03`.

```python
def parcela_segunda_ordem(valor, n):
    if n < 1 or n >= 12:
        raise ValueError("parcelas invalidas")
    if n <= 3:
        juros = 0
    else:
        juros = 0.03 * (n - 3)
    total = valor * (1 + juros)
    return round(total / n, 2)
```

## e)

Sim, a suíte mata. O teste com `n = 12` espera 118.0, mas o mutante lança ValueError. O caso `n = 4` também pega a mudança nos juros.

Isso bate com o efeito de acoplamento do Offutt (1992): testes que matam falhas simples geralmente também matam combinações delas. Não é garantia pra todo mutante de 2ª ordem, mas aqui funcionou.
