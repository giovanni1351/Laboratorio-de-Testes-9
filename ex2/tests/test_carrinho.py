from carrinho import total_com_desconto


def test_total_com_desconto():
    assert total_com_desconto([10, 20, 30, 40, 50]) == 141.0


def test_arredondamento_com_preco_fracionado():
    assert total_com_desconto([0, 0, 0, 0.01]) == 0.01
