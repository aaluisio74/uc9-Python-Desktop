import math


base = float(input("Digite a base do retângulo: "))
altura = float(input("Digite a altura do retângulo: "))

area = base * altura
perimetro = 2 * (base + altura)
diagonal = (base ** 2 + altura ** 2) ** 0.5
# diagonal = math.sqrt(base ** 2 + altura ** 2)

print("ÁREA:", f"{area:.4f}")
print("PERÍMETRO:", f"{perimetro:.4f}")
print("DIAGONAL:", f"{diagonal:.4f}")

# print(F"ÁREA: {area:.4f}")
# print(F"PERÍMETRO: {perimetro:.4f}")
# print(F"DIAGONAL: {diagonal:.4f}")