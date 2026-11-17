# PARTE 1 - Importações
from datetime import datetime

from sqlalchemy import (
    String, Integer, ForeignKey, DateTime,
    UniqueConstraint, CheckConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# PARTE 2 — Modelo Estudante
class Estudante(Base):
    __tablename__ = "estudantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    ativo: Mapped[bool] = mapped_column(
    default=True,
    nullable=False
    )


    # Um estudante pode ter várias matrículas.
    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="estudante"
    )


# PARTE 3 — Modelo Curso
class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    descricao: Mapped[str | None] = mapped_column(String(500))

    # Um curso possui várias disciplinas.
    disciplinas: Mapped[list["Disciplina"]] = relationship(
        back_populates="curso"
    )


# PARTE 4 — Modelo Disciplina
class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    carga_horaria: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.id"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "nome", "curso_id",
            name="uq_disciplina_nome_curso"
        ),
        CheckConstraint(
            "carga_horaria > 0",
            name="ck_disciplina_carga_positiva"
        ),
    )

    curso: Mapped["Curso"] = relationship(
        back_populates="disciplinas"
    )

    # Uma disciplina pode ter várias matrículas.
    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="disciplina"
    )


# PARTE 5 — Modelo Matricula
class Matricula(Base):
    __tablename__ = "matriculas"

    id: Mapped[int] = mapped_column(primary_key=True)

    estudante_id: Mapped[int] = mapped_column(
        ForeignKey("estudantes.id"), nullable=False
    )
    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id"), nullable=False
    )

    data_matricula: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="ativa", nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "estudante_id", "disciplina_id",
            name="uq_matricula_estudante_disciplina"
        ),
        CheckConstraint(
            "status IN ('ativa', 'cancelada')",
            name="ck_matricula_status"
        ),
    )

    estudante: Mapped["Estudante"] = relationship(
        back_populates="matriculas"
    )
    disciplina: Mapped["Disciplina"] = relationship(
        back_populates="matriculas"
    )


# PARTE 6 — Modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    senha_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    papel: Mapped[str] = mapped_column(
        String(20), default="consulta", nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "papel IN ('admin', 'consulta')",
            name="ck_usuario_papel"
        ),
    )
