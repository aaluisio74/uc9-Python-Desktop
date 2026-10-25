# ARQUIVO PARA CRIAR O PRIMEIRO ADMINISTRADOR.
from getpass import getpass

from sqlalchemy import select

from .database import obter_sessao
from .models import Usuario
from .security import gerar_hash


def criar_admin():
    username = input("Nome do administrador: ").strip()
    senha = getpass("Senha do administrador: ")
    confirmar = getpass("Confirme a senha: ")

    if not username:
        print("Erro: informe um nome de usuário.")
        return

    if len(username) > 50:
        print("Erro: o usuário deve ter até 50 caracteres.")
        return

    if not senha:
        print("Erro: a senha não pode ficar vazia.")
        return

    if senha != confirmar:
        print("Erro: as senhas não coincidem.")
        return

    gerador = obter_sessao()
    db = next(gerador)

    try:
        existente = db.scalars(
            select(Usuario).where(
                Usuario.username == username
            )
        ).first()

        if existente is not None:
            print("Esse usuário já está cadastrado.")
            return

        usuario = Usuario(
            username=username,
            senha_hash=gerar_hash(senha),
            papel="admin",
        )

        db.add(usuario)
        db.commit()

        print("Administrador cadastrado com sucesso!")
        print(f"Usuário: {username}")
        print("Agora você pode testar o login.")

    except Exception:
        db.rollback()
        raise

    finally:
        gerador.close()


if __name__ == "__main__":
    criar_admin()
