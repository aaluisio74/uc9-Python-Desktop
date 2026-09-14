distancia = int(input("Distância percorrida (Km)): "))
combustivel_gasto = float(input("Combustível gasto (litros): "))

consumo_medio = distancia / combustivel_gasto

print(f"Consumo médio: {consumo_medio:.3f} Km/l")