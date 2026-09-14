nome = input("Nome: ")
valor_por_hora = float(input("Valor por hora: "))
horas_trabalhadas = int(input("Horas trabalhadas: "))

pagamento = valor_por_hora * horas_trabalhadas

print(f"O pagamento para {nome} deve ser: R$ {pagamento:.2f}")