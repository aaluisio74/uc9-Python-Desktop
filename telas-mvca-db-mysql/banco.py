import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        # Configuração no Notebook do Professor.
        conexao = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="sistema_login"
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def validar_login(usuario, senha):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        query = "SELECT * FROM usuarios WHERE usuario = %s AND senha = %s"
        cursor.execute(query, (usuario, senha))
        resultado = cursor.fetchone() ## Dados ou None
        cursor.close();
        conexao.close();
        return resultado is not None # Terceiro Princípio (Guri e o Fantasma): Explícito é melhor que implícito.
    return False

def cadastrar_usuario(usuario, senha):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)"
            cursor.execute(query, (usuario, senha))
            conexao.commit()
            cursor.close();
            conexao.close();
            return True, "Usuário cadastrado com sucesso!"
        except Error as e:
            conexao.close()
            if e.errno == 1062:
                return False,
            return False, f"Erro ao cadastrar: {e}"
        return False, "Erro na conexão com o banco de dados."

    return False