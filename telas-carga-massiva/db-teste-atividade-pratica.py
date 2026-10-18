import sqlite3


def main():
    # 1. Conectar ao banco de dados (será criado um arquivo chamado 'loja.db')
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()

    # 2. Criar a tabela 'produtos'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            codigo INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    """)
    conn.commit()

    # 3. Lista Python com os produtos (incluindo um produto com preço inválido para teste)
    produtos_brutos = [
        (101, "Teclado", 20, 75.00),
        (102, "Mouse", 30, 45.00),
        (103, "Monitor", 10, 850.00),
        (104, "Headset", 15, 120.00),
        (
            105,
            "Webcam (Teste Inválido)",
            5,
            -15.00,
        ),  # Preço negativo para testar a validação
    ]

    # 4. Validar se a quantidade é positiva e o preço é maior que zero
    produtos_validados = []

    print("--- PROCESSANDO VALIDAÇÃO DE PRODUTOS ---")
    for codigo, nome, quantidade, preco in produtos_brutos:
        if quantidade > 0 and preco > 0:
            produtos_validados.append((codigo, nome, quantidade, preco))
            print(f"✔ [APROVADO] {nome} (Código: {codigo}) passou na validação.")
        else:
            print(
                f"❌ [REJEITADO] {nome} (Código: {codigo}) possui dados inválidos"
                f" (Qtd: {quantidade}, Preço: R$ {preco:.2f}). Importação"
                " bloqueada."
            )

    print("-" * 50)

    # 5. Inserir os produtos validados usando executemany()
    if produtos_validados:
        cursor.executemany(
            """
                INSERT OR REPLACE INTO produtos (codigo, nome, quantidade, preco)
                VALUES (?, ?, ?, ?)
            """,
            produtos_validados,
        )
        conn.commit()
        print(f"Total de {len(produtos_validados)} produtos importados com sucesso!\n")

    # 6. Consultar e exibir os produtos cadastrados
    cursor.execute("SELECT codigo, nome, quantidade, preco FROM produtos")
    produtos_cadastrados = cursor.fetchall()

    print("=== RELATÓRIO DE PRODUTOS CADASTRADOS NO BANCO ===")
    print(f"{'Código':<8} | {'Produto':<25} | {'Qtd':<5} | {'Preço (R$)'}")
    print("-" * 55)

    for codigo, nome, quantidade, preco in produtos_cadastrados:
        # Formatando o preço para o padrão brasileiro com vírgula
        preco_formatado = f"{preco:.2f}".replace(".", ",")
        print(
            f"{codigo:<8} | {nome:<25} | {quantidade:<5} | R$ {preco_formatado}"
        )

    # Fechar a conexão com o banco de dados
    conn.close()


if __name__ == "__main__":
    main()