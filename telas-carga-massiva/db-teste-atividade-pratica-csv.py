import sqlite3
import csv # Acresentar para usar o arquivo CSV
from pathlib import Path # Acresentar para usar o arquivo CSV

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
    produtos_brutos = []

    # Cria o caminho seguro para o arquivo dentro da pasta usando uma string (texto).
    with open('telas-carga-massiva/produtos.csv', mode='r', encoding='utf-8') as f:
        leitor = csv.DictReader(f, delimiter=';')
        for linha in leitor:
            codigo = int(linha['codigo'])
            nome = linha['produto']
            quantidade = int(linha['quantidade'])
            # Substitui a vírgula do preço por ponto antes de converter para float
            preco = float(linha['preco'].replace(',','.'))
            
            produtos_brutos.append((codigo, nome, quantidade, preco))

# OU
#     # Cria o caminho seguro para o arquivo dentro da pasta usando uma variável.
#     caminho_csv = Path('telas-carga-massiva') / 'produtos.csv'
    
#     with open(caminho_csv, mode='r', encoding='utf-8') as f:
#         leitor = csv.DictReader(f, delimiter=';')
#         for linha in leitor:
#             codigo = int(linha['codigo'])
#             nome = linha['produto']
#             quantidade = int(linha['quantidade'])
#             # Substitui a vírgula do preço por ponto antes de converter para float
#             preco = float(linha['preco'].replace(',','.'))
            
#             produtos_brutos.append((codigo, nome, quantidade, preco))

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