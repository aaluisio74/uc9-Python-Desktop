a = float(input("Digite a medida A: "))
b = float(input("Digite a medida B: "))
c = float(input("Digite a medida C: "))

area_quadrado = a ** 2
area_triangulo = (a * b) / 2
area_trapezio = ((a + b) * c) / 2

print(f"ÁREA DO QUADRADO: {area_quadrado:.4f}")
print(f"ÁREA DO TRIÂNGULO: {area_triangulo:.4f}")
print(f"ÁREA DO TRAPÉZIO: {area_trapezio:.4f}")