largura = float(input("Digite a largura do terreno (metros): "))
comprimento = float(input("Digite o comprimento do terreno (metros): "))
metro_quadrado = float(input("Digite o preço do metro quadrado (reais): "))

area = largura * comprimento
preco_total = area * metro_quadrado

print(f"A área do terreno é: {area:.2f} metros quadrados")
print(f"O preço total do terreno é: R$ {preco_total:.2f}")