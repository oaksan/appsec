from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, UniqueConstraint

# -----------------------------------------------------------------------------
# Constantes do Modelo de Institucionalização e Domínio
# -----------------------------------------------------------------------------

ADOPTION_LEVEL_WEIGHTS: dict[int, float] = {
    0: 0.0,   # AL0 - Não Adotada
    1: 0.1,   # AL1 - Abandonada
    2: 0.3,   # AL2 - Projeto / Produto
    3: 0.6,   # AL3 - Processo Definido
    4: 1.0,   # AL4 - Institucionalizada
}

ADOPTION_LEVEL_NAMES: dict[int, str] = {
    0: "Não Adotada",
    1: "Abandonada",
    2: "Projeto / Produto",
    3: "Processo Definido",
    4: "Institucionalizada",
}

ADOPTION_LEVEL_CODES: dict[int, str] = {
    0: "AL0",
    1: "AL1",
    2: "AL2",
    3: "AL3",
    4: "AL4",
}

SMAF_DIMENSIONS: list[str] = [
    "Governança",
    "Arquitetura e Design",
    "Desenvol. e Revisão",
    "Construção e Impl.",
    "Testes e Verificação",
    "Operações e Obs.",
]

STH_STAGES: list[dict[str, str]] = [
    {"code": "A", "name": "Estágio A (Reactive)"},
    {"code": "B", "name": "Estágio B (Agile)"},
    {"code": "C", "name": "Estágio C (CSI)"},
    {"code": "D", "name": "Estágio D (CSD)"},
    {"code": "E", "name": "Estágio E (CSO)"},
]

# -----------------------------------------------------------------------------
# Entidades Relacionais (Tabelas SQLModel)
# -----------------------------------------------------------------------------

class Squad(SQLModel, table=True):
    __tablename__ = "squad"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True, max_length=50)
    name: str = Field(max_length=100)
    purdue_level: str = Field(max_length=100)
    purdue_short: str = Field(max_length=50)
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Statement(SQLModel, table=True):
    __tablename__ = "statement"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True, max_length=20)
    description: str
    sth_stage: str = Field(max_length=50)
    sth_stage_code: str = Field(index=True, max_length=5)
    smaf_dimension: str = Field(index=True, max_length=50)
    samm_ref: str
    dsomm_ref: str


class AssessmentAnswer(SQLModel, table=True):
    __tablename__ = "assessment_answer"
    __table_args__ = (
        UniqueConstraint("squad_id", "statement_id", name="uq_squad_statement"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    squad_id: int = Field(foreign_key="squad.id", index=True)
    statement_id: int = Field(foreign_key="statement.id", index=True)
    adoption_level: int = Field(ge=0, le=4)
    adoption_weight: float


# -----------------------------------------------------------------------------
# Esquemas Pydantic para APIs e Transferência de Dados (DTOs)
# -----------------------------------------------------------------------------

class StatementRead(BaseModel):
    id: int
    code: str
    description: str
    sth_stage: str
    sth_stage_code: str
    smaf_dimension: str
    samm_ref: str
    dsomm_ref: str

    model_config = ConfigDict(from_attributes=True)


class SquadRead(BaseModel):
    id: int
    code: str
    name: str
    purdue_level: str
    purdue_short: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class SquadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Nome de exibição da squad")
    purdue_level: str = Field(min_length=3, max_length=100, description="Camada do Modelo Purdue (ISA-95)")
    purdue_short: str = Field(min_length=2, max_length=50, description="Rótulo curto da camada Purdue (ex: N2 OT, N3 MES)")
    description: str = Field(default="", max_length=500, description="Descrição do escopo operacional")


class AnswerUpdateItem(BaseModel):
    statement_code: str = Field(description="Código atômico da afirmação (ex: AO.01, ARQ.01)")
    adoption_level: int = Field(ge=0, le=4, description="Nível de institucionalização assinalado (0 a 4)")


class AuditUpdateRequest(BaseModel):
    answers: list[AnswerUpdateItem] = Field(min_length=1, max_length=40, description="Lista de respostas a serem atualizadas")


class DimensionScore(BaseModel):
    dimension: str
    total_items: int
    weight_sum: float
    adoption_degree: float          # Valor percentual (ex: 36.7)
    adoption_degree_formatted: str  # Ex: "36.7%"


class StageScore(BaseModel):
    stage: str
    stage_code: str
    total_items: int
    weight_sum: float
    adoption_degree: float          # Valor percentual (ex: 60.0)
    adoption_degree_formatted: str  # Ex: "60.0%"
    al_counts: dict[str, int]


class StatementAssessmentDetail(BaseModel):
    statement_code: str
    description: str
    smaf_dimension: str
    sth_stage: str
    sth_stage_code: str
    adoption_level_code: str  # "AL0" a "AL4"
    adoption_level_num: int   # 0 a 4
    adoption_level_name: str  # "Não Adotada", "Processo Definido", etc.
    adoption_weight: float    # 0.0, 0.1, 0.3, 0.6, 1.0
    adoption_degree_pct: str  # "0%", "10%", "30%", "60%", "100%"
    samm_ref: str
    dsomm_ref: str


class SquadDiagnosticSummary(BaseModel):
    squad: SquadRead
    global_adoption_degree: float
    global_adoption_degree_formatted: str
    predominant_stage: str
    al_distribution: dict[str, int]
    dimension_scores: list[DimensionScore]
    stage_scores: list[StageScore]
    statements: list[StatementAssessmentDetail]


class BenchmarkSquadItem(BaseModel):
    id: int
    code: str
    name: str
    purdue_short: str

    model_config = ConfigDict(from_attributes=True)


class DimensionBenchmarkRow(BaseModel):
    dimension: str
    scores: dict[str, float] = Field(default_factory=dict)
    squad_a_pct: float = 0.0
    squad_b_pct: float = 0.0
    squad_c_pct: float = 0.0
    average_pct: float = 0.0


class StageBenchmarkRow(BaseModel):
    stage: str
    stage_code: str = ""
    scores: dict[str, float] = Field(default_factory=dict)
    squad_a_pct: float = 0.0
    squad_b_pct: float = 0.0
    squad_c_pct: float = 0.0
    average_pct: float = 0.0


class GlobalSummaryBenchmark(BaseModel):
    model_config = ConfigDict(extra="allow")

    squad_a_pct: float = 0.0
    squad_b_pct: float = 0.0
    squad_c_pct: float = 0.0
    organization_average_pct: float = 0.0
    scores: dict[str, float] = Field(default_factory=dict)


class BenchmarkSummary(BaseModel):
    squads: list[BenchmarkSquadItem] = Field(default_factory=list)
    dimensions: list[DimensionBenchmarkRow]
    stages: list[StageBenchmarkRow]
    global_summary: GlobalSummaryBenchmark


class SquadDeleteResponse(BaseModel):
    message: str
    deleted_code: str
    deleted_id: int


# -----------------------------------------------------------------------------
# Módulo de Cálculo Matemático e Lógica de Domínio
# -----------------------------------------------------------------------------

def get_adoption_weight(level: int) -> float:
    """Retorna o peso numérico correspondente ao nível de institucionalização (AL0 a AL4)."""
    if level not in ADOPTION_LEVEL_WEIGHTS:
        raise ValueError(f"Nível de adoção inválido: {level}. Deve ser entre 0 e 4.")
    return ADOPTION_LEVEL_WEIGHTS[level]


def calculate_group_adoption_degree(weights: list[float]) -> float:
    """
    Calcula o Grau de Adoção de um agrupamento k (ADk) conforme fórmula 3.1 da dissertação:
    ADk = (sum(peso_i) / n_k) * 100%
    """
    if not weights:
        return 0.0
    return (sum(weights) / len(weights)) * 100.0


def calculate_global_adoption_degree(dimension_ad_percentages: list[float]) -> float:
    """
    Calcula o Grau de Adoção Global da squad (ADglobal) conforme fórmula 3.2 da dissertação:
    ADglobal = (1 / 6) * sum(ADk) para as 6 dimensões SMAF.
    """
    if not dimension_ad_percentages:
        return 0.0
    return sum(dimension_ad_percentages) / len(dimension_ad_percentages)

