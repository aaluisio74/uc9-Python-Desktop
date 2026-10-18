import sqlite3
import pandas as pd # Acresentar para usar o arquivo Excel
from pathlib import Path # Acresentar para usar o arquivo Excel

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
    
    # --- TRECHO A MODIFICAR ---
    # # Cria o caminho seguro para o arquivo dentro da pasta usando uma variável.
    # caminho_csv = Path('telas-carga-massiva') / 'produtos.xlsx'
    # df = pd.read_excel(caminho_csv)

    # Cria o caminho seguro para o arquivo dentro da pasta usando uma string (texto)
    df = pd.read_excel('telas-carga-massiva/produtos.xlsx')

    
    # Converte o DataFrame para uma lista de tuplas (codigo, produto, quantidade, preco)
    produtos_brutos = [
        (row['codigo'], row['produto'], row['quantidade'], row['preco'])
        for _, row in df.iterrows()
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