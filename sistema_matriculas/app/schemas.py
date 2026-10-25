# PARTE 1 — Importações de validação
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# PARTE 2 — Dados recebidos ao cadastrar estudante
class EstudanteEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr


# PARTE 3 — Dados devolvidos pela API
class EstudanteSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr


# PARTE 4 — Dados de entrada para cursos
class CursoEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    descricao: str | None = Field(default=None, max_length=500)


# PARTE 5 — Dados de entrada para disciplinas
class DisciplinaEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    carga_horaria: int = Field(gt=0, le=2000)
    curso_id: int = Field(gt=0)


# PARTE 6 — Dados de entrada para matrículas
class MatriculaEntrada(BaseModel):
    estudante_id: int = Field(gt=0)
    disciplina_id: int = Field(gt=0)
