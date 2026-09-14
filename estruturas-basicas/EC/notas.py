nota1 = float(input("Digite a primeira nota: "))
nota2 = float(input("Digite a segunda nota: "))

nota_final = nota1 + nota2

print(f"NOTA FINAL = {nota_final:.1f}")

if nota_final < 60.0:
    print("REPROVADO")