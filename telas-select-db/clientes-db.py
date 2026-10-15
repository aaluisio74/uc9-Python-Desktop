import sqlite3

# Conecta ao banco 
conexao = sqlite3.connect("clientes.db") 
cursor = conexao.cursor() 

# Criar a tabela clientes 
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS clientes ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    email TEXT UNIQUE NOT NULL, 
    idade INTEGER, 
    cidade TEXT 
) 
""")

# Inserir dados de exemplo 
clientes_exemplo = [ 
    ("Alessandro Formagio da Silva", "alessandro@email.com", 28, "São Paulo"), 
    ("Eric Azevedo", "eric@email.com", 35, "Rio de Janeiro"), 
    ("Gian Rosa", "gian@email.com", 42, "São Paulo"), 
    ("Gabriel Victor da Silva", "gabriel@email.com", 23, "Belo Horizonte"), 
    ("Jorge Momberger", "jorge@email.com", 31, "São Paulo"), 
    ("Marcelo Antônio", "marceloa@email.com", 29, "Curitiba"), 
    ("Thabata Kern Goulart", "thabatakg@email.com", 45, "Porto Alegre"), 
    ("Marcos Santos de Souza", "marcosss@email.com", 27, "São Paulo"), 
    ("Eduardo Rosa da Silva", "eduardo@email.com", 38, "Brasília"), 
    ("Samanta Victor da Silva", "samanta@email.com", 33, "Salvador") 
]

# Inserir os dados (usando executemany para inserir múltiplos registros) 
cursor.executemany(""" 
INSERT OR IGNORE INTO clientes (nome, email, idade, cidade) 
VALUES (?, ?, ?, ?) 
""", clientes_exemplo) 

# Confirmar as alterações 
conexao.commit() 
'''
# EXEMPLO 1: SELECT simples (todos os registros) 
cursor.execute("SELECT * FROM clientes") 
todos_clientes = cursor.fetchall() # Retorna uma lista de tuplas 

print("Todos os clientes:") 
for cliente in todos_clientes: 
    print(cliente)

# EXEMPLO 2: SELECT com campos específicos 
cursor.execute("SELECT nome, email FROM clientes") 
nomes_emails = cursor.fetchall() 
print("\nNomes e emails:") 
for nome, email in nomes_emails: 
    print(f"Nome: {nome} - Email: {email}") 

# EXEMPLO 3: SELECT com WHERE (filtro) 
cursor.execute("SELECT * FROM clientes WHERE cidade = 'São Paulo'") 
clientes_sp = cursor.fetchall() 
print(f"\nClientes de São Paulo: {len(clientes_sp)} encontrados") 

# EXEMPLO 4: SELECT com ORDER BY (ordenação) 
cursor.execute("SELECT nome, idade FROM clientes ORDER BY idade DESC") 
clientes_ordenados = cursor.fetchall() 
print("\nClientes ordenados por idade (mais velhos primeiro):") 
for nome, idade in clientes_ordenados: 
    print(f"{nome}: {idade} anos") 

# EXEMPLO 5: SELECT com LIMIT (limitar resultados) 
cursor.execute("SELECT nome FROM clientes LIMIT 5") 
primeiros_5 = cursor.fetchall() 
print("\nPrimeiros 5 clientes:") 
for cliente in primeiros_5: 
    print(cliente[0]) 

# EXEMPLO 6: SELECT com COUNT (contar registros) 
cursor.execute("SELECT COUNT(*) FROM clientes") 
total = cursor.fetchone()[0] # fetchone() retorna uma tupla com um elemento 
print(f"\nTotal de clientes: {total}") 
'''
# EXEMPLO 7: SELECT com LIKE (busca parcial) 
cursor.execute("SELECT nome FROM clientes WHERE nome LIKE '%Silva%'") 
clientes_silva = cursor.fetchall() 
print("\nClientes com 'Silva' no nome:") 
for cliente in clientes_silva: 
    print(cliente[0]) 

# Fechar a conexão 
conexao.close()
