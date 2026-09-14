preco_unitario = float(input("Digite o preço unitário do produto: "))
quantidade = int(input("Digite a quantidade comprada: "))
dinheiro_recebido = float(input("Digite o valor em dinheiro recebido: "))

troco = dinheiro_recebido - (preco_unitario * quantidade)

print(f"TROCO = R$ {troco:.2f}")