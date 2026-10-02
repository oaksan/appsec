import re
import unicodedata
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

from database import engine, get_session, init_db, seed_database
from models import (
    ADOPTION_LEVEL_CODES,
    ADOPTION_LEVEL_NAMES,
    SMAF_DIMENSIONS,
    STH_STAGES,
    AnswerUpdateItem,
    AssessmentAnswer,
    AuditUpdateRequest,
    BenchmarkSquadItem,
    BenchmarkSummary,
    DimensionBenchmarkRow,
    DimensionScore,
    GlobalSummaryBenchmark,
    Squad,
    SquadCreate,
    SquadDeleteResponse,
    SquadDiagnosticSummary,
    SquadRead,
    StageBenchmarkRow,
    StageScore,
    Statement,
    StatementAssessmentDetail,
    StatementRead,
    calculate_global_adoption_degree,
    calculate_group_adoption_degree,
    get_adoption_weight,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização e carga inicial idempotente do banco SQLite
    init_db()
    with Session(engine) as session:
        seed_database(session)
    yield


app = FastAPI(
    title="Zeppelin-AppSec: Diagnóstico de Segurança Contínua",
    description="Instrumento de avaliação e diagnóstico de maturidade DevSecOps baseado no modelo StH-AppSec e Purdue.",
    version="1.0.0",
    lifespan=lifespan,
)

# Montagem de arquivos estáticos e templates Jinja2
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# -----------------------------------------------------------------------------
# Funções Auxiliares de Cálculo de Diagnóstico
# -----------------------------------------------------------------------------

def calculate_squad_diagnostic(session: Session, squad: Squad) -> SquadDiagnosticSummary:
    """Calcula todas as métricas analíticas e consolida o diagnóstico da squad."""
    statements = session.exec(select(Statement).order_by(Statement.id)).all()
    answers = session.exec(
        select(AssessmentAnswer).where(AssessmentAnswer.squad_id == squad.id)
    ).all()
    answers_by_stmt_id = {ans.statement_id: ans for ans in answers}

    # Estruturas de agregação
    dim_weights: dict[str, list[float]] = {d: [] for d in SMAF_DIMENSIONS}
    stage_weights: dict[str, list[float]] = {s["name"]: [] for s in STH_STAGES}
    stage_al_counts: dict[str, dict[str, int]] = {
        s["name"]: {"AL0": 0, "AL1": 0, "AL2": 0, "AL3": 0, "AL4": 0}
        for s in STH_STAGES
    }
    al_distribution: dict[str, int] = {
        "AL0": 0, "AL1": 0, "AL2": 0, "AL3": 0, "AL4": 0
    }
    statement_details: list[StatementAssessmentDetail] = []

    for stmt in statements:
        ans = answers_by_stmt_id.get(stmt.id)
        level_num = ans.adoption_level if ans else 0
        weight = ans.adoption_weight if ans else 0.0

        al_code = ADOPTION_LEVEL_CODES.get(level_num, "AL0")
        al_name = ADOPTION_LEVEL_NAMES.get(level_num, "Não Adotada")
        pct_label = f"{int(round(weight * 100))}%"

        al_distribution[al_code] += 1

        if stmt.smaf_dimension in dim_weights:
            dim_weights[stmt.smaf_dimension].append(weight)

        if stmt.sth_stage in stage_weights:
            stage_weights[stmt.sth_stage].append(weight)
            stage_al_counts[stmt.sth_stage][al_code] += 1

        statement_details.append(
            StatementAssessmentDetail(
                statement_code=stmt.code,
                description=stmt.description,
                smaf_dimension=stmt.smaf_dimension,
                sth_stage=stmt.sth_stage,
                sth_stage_code=stmt.sth_stage_code,
                adoption_level_code=al_code,
                adoption_level_num=level_num,
                adoption_level_name=al_name,
                adoption_weight=weight,
                adoption_degree_pct=pct_label,
                samm_ref=stmt.samm_ref,
                dsomm_ref=stmt.dsomm_ref,
            )
        )

    # 1. Pontuação das 6 dimensões SMAF
    dimension_scores: list[DimensionScore] = []
    dim_ad_raw_list: list[float] = []
    for dim_name in SMAF_DIMENSIONS:
        weights = dim_weights[dim_name]
        ad_val = calculate_group_adoption_degree(weights)
        dim_ad_raw_list.append(ad_val)
        ad_rounded = round(ad_val, 1)
        dimension_scores.append(
            DimensionScore(
                dimension=dim_name,
                total_items=len(weights),
                weight_sum=round(sum(weights), 2),
                adoption_degree=ad_rounded,
                adoption_degree_formatted=f"{ad_rounded:.1f}%",
            )
        )

    # 2. Grau de Adoção Global (Média simples das 6 dimensões SMAF)
    global_ad = calculate_global_adoption_degree(dim_ad_raw_list)
    global_ad_rounded = round(global_ad, 1)

    # 3. Pontuação dos 5 estágios StH-AppSec
    stage_scores: list[StageScore] = []
    for stg in STH_STAGES:
        stg_name = stg["name"]
        stg_code = stg["code"]
        weights = stage_weights[stg_name]
        ad_val = calculate_group_adoption_degree(weights)
        ad_rounded = round(ad_val, 1)
        stage_scores.append(
            StageScore(
                stage=stg_name,
                stage_code=stg_code,
                total_items=len(weights),
                weight_sum=round(sum(weights), 2),
                adoption_degree=ad_rounded,
                adoption_degree_formatted=f"{ad_rounded:.1f}%",
                al_counts=stage_al_counts[stg_name],
            )
        )

    # Estágio predominante (estágio mais avançado que atinge maior adoção ou maior estágio com AD >= 50%)
    predominant = stage_scores[0].stage
    best_ad = -1.0
    for stg in stage_scores:
        if stg.adoption_degree >= best_ad:
            best_ad = stg.adoption_degree
            predominant = stg.stage

    return SquadDiagnosticSummary(
        squad=SquadRead.model_validate(squad),
        global_adoption_degree=global_ad_rounded,
        global_adoption_degree_formatted=f"{global_ad_rounded:.1f}%",
        predominant_stage=predominant,
        al_distribution=al_distribution,
        dimension_scores=dimension_scores,
        stage_scores=stage_scores,
        statements=statement_details,
    )


# -----------------------------------------------------------------------------
# Rotas da API REST
# -----------------------------------------------------------------------------

@app.get("/api/statements", response_model=list[StatementRead], tags=["Afirmações"])
def list_statements(
    dimension: Optional[str] = Query(None, description="Filtrar por dimensão SMAF"),
    stage: Optional[str] = Query(None, description="Filtrar por código do estágio StH (A, B, C, D, E)"),
    session: Session = Depends(get_session),
):
    """Retorna o catálogo das 40 afirmações atômicas de segurança contínua."""
    query = select(Statement).order_by(Statement.id)
    if dimension:
        query = query.where(Statement.smaf_dimension == dimension)
    if stage:
        query = query.where(Statement.sth_stage_code == stage.upper())
    statements = session.exec(query).all()
    return statements


@app.get("/api/squads", response_model=list[SquadRead], tags=["Squads"])
def list_squads(session: Session = Depends(get_session)):
    """Retorna a lista das squads industriais cadastradas no Modelo Purdue."""
    squads = session.exec(select(Squad).order_by(Squad.id)).all()
    return squads


@app.post("/api/squads", response_model=SquadRead, status_code=201, tags=["Squads"])
def create_squad(squad_in: SquadCreate, session: Session = Depends(get_session)):
    """Cadastra uma nova squad industrial e inicializa 40 respostas com AL0."""
    name_clean = squad_in.name.strip()
    if not name_clean:
        raise HTTPException(status_code=422, detail="Nome da squad não pode ser vazio.")

    base_code = slugify(name_clean)
    if not base_code:
        base_code = "squad"

    existing = session.exec(
        select(Squad).where((Squad.code == base_code) | (Squad.name == name_clean))
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Já existe uma squad cadastrada com o código '{base_code}' ou nome '{name_clean}'.",
        )

    new_squad = Squad(
        code=base_code,
        name=name_clean,
        purdue_level=squad_in.purdue_level.strip(),
        purdue_short=squad_in.purdue_short.strip(),
        description=squad_in.description.strip(),
    )
    session.add(new_squad)
    session.commit()
    session.refresh(new_squad)

    # Inicializar as 40 afirmações atômicas com nível AL0 e peso 0.0
    statements = session.exec(select(Statement).order_by(Statement.id)).all()
    for stmt in statements:
        ans = AssessmentAnswer(
            squad_id=new_squad.id,
            statement_id=stmt.id,
            adoption_level=0,
            adoption_weight=0.0,
        )
        session.add(ans)
    session.commit()

    return new_squad


@app.delete(
    "/api/squads/{squad_id_or_code}",
    response_model=SquadDeleteResponse,
    tags=["Squads"],
)
def delete_squad(
    squad_id_or_code: str,
    session: Session = Depends(get_session),
):
    """Exclui uma squad e todas as suas 40 respostas de auditoria associadas (cascade delete)."""
    # 1. Localizar squad por id ou code
    query = select(Squad)
    if squad_id_or_code.isdigit():
        query = query.where(Squad.id == int(squad_id_or_code))
    else:
        query = query.where(Squad.code == squad_id_or_code.lower())

    squad = session.exec(query).first()
    if not squad:
        raise HTTPException(
            status_code=404,
            detail=f"Squad '{squad_id_or_code}' não encontrada.",
        )

    # 2. Guarda: não permitir excluir se for a única squad restante no sistema
    all_squads = session.exec(select(Squad.id)).all()
    if len(all_squads) <= 1:
        raise HTTPException(
            status_code=400,
            detail="Não é permitido excluir a única squad restante no sistema.",
        )

    squad_name = squad.name
    squad_code = squad.code
    squad_id = squad.id

    # 3. Exclusão em cascata: primeiro as respostas de avaliação, depois a squad
    answers = session.exec(
        select(AssessmentAnswer).where(AssessmentAnswer.squad_id == squad.id)
    ).all()
    for ans in answers:
        session.delete(ans)

    session.delete(squad)
    session.commit()

    return SquadDeleteResponse(
        message=f"Squad '{squad_name}' e suas respostas associadas foram excluídas com sucesso.",
        deleted_code=squad_code,
        deleted_id=squad_id,
    )


@app.get(
    "/api/diagnostics/{squad_id_or_code}",
    response_model=SquadDiagnosticSummary,
    tags=["Diagnóstico"],
)
def get_squad_diagnostic(
    squad_id_or_code: str,
    session: Session = Depends(get_session),
):
    """Retorna o diagnóstico consolidado de uma squad com métricas por dimensão, estágio e afirmação."""
    query = select(Squad)
    if squad_id_or_code.isdigit():
        query = query.where(Squad.id == int(squad_id_or_code))
    else:
        query = query.where(Squad.code == squad_id_or_code.lower())

    squad = session.exec(query).first()
    if not squad:
        raise HTTPException(status_code=404, detail="Squad não encontrada.")

    return calculate_squad_diagnostic(session, squad)


@app.put(
    "/api/diagnostics/{squad_id_or_code}",
    response_model=SquadDiagnosticSummary,
    tags=["Diagnóstico"],
)
def update_squad_audit(
    squad_id_or_code: str,
    audit_data: AuditUpdateRequest,
    session: Session = Depends(get_session),
):
    """Atualiza os níveis de institucionalização assinalados para as afirmações de uma squad."""
    query = select(Squad)
    if squad_id_or_code.isdigit():
        query = query.where(Squad.id == int(squad_id_or_code))
    else:
        query = query.where(Squad.code == squad_id_or_code.lower())

    squad = session.exec(query).first()
    if not squad:
        raise HTTPException(status_code=404, detail=f"Squad '{squad_id_or_code}' não encontrada.")

    # Mapear afirmações existentes
    statements = {s.code: s for s in session.exec(select(Statement)).all()}

    for item in audit_data.answers:
        stmt = statements.get(item.statement_code)
        if not stmt:
            raise HTTPException(
                status_code=422,
                detail=f"Código de afirmação '{item.statement_code}' não reconhecido no catálogo.",
            )

        ans = session.exec(
            select(AssessmentAnswer).where(
                AssessmentAnswer.squad_id == squad.id,
                AssessmentAnswer.statement_id == stmt.id,
            )
        ).first()

        weight = get_adoption_weight(item.adoption_level)
        if ans:
            ans.adoption_level = item.adoption_level
            ans.adoption_weight = weight
            session.add(ans)
        else:
            ans = AssessmentAnswer(
                squad_id=squad.id,
                statement_id=stmt.id,
                adoption_level=item.adoption_level,
                adoption_weight=weight,
            )
            session.add(ans)

    session.commit()
    return calculate_squad_diagnostic(session, squad)


@app.get("/api/benchmark", response_model=BenchmarkSummary, tags=["Benchmark"])
def get_benchmark(session: Session = Depends(get_session)):
    """Retorna o comparativo consolidado entre todas as squads cadastradas e a média da organização."""
    squads = session.exec(select(Squad).order_by(Squad.id)).all()
    if not squads:
        raise HTTPException(status_code=404, detail="Nenhuma squad cadastrada.")

    squad_diagnostics: dict[str, SquadDiagnosticSummary] = {}
    for sq in squads:
        squad_diagnostics[sq.code] = calculate_squad_diagnostic(session, sq)

    num_squads = len(squads)

    # 1. Comparativo por Dimensão SMAF
    dimension_rows: list[DimensionBenchmarkRow] = []
    for i, dim_name in enumerate(SMAF_DIMENSIONS):
        scores_dict: dict[str, float] = {}
        for sq in squads:
            score = squad_diagnostics[sq.code].dimension_scores[i].adoption_degree
            scores_dict[sq.code] = score

        avg_val = round(sum(scores_dict.values()) / num_squads, 1)
        val_a = scores_dict.get("squad-a", 0.0)
        val_b = scores_dict.get("squad-b", 0.0)
        val_c = scores_dict.get("squad-c", 0.0)

        dimension_rows.append(
            DimensionBenchmarkRow(
                dimension=dim_name,
                scores=scores_dict,
                squad_a_pct=val_a,
                squad_b_pct=val_b,
                squad_c_pct=val_c,
                average_pct=avg_val,
            )
        )

    # 2. Comparativo por Estágio StH-AppSec (Tabela 4.2 da dissertação)
    stage_rows: list[StageBenchmarkRow] = []
    for i, stg in enumerate(STH_STAGES):
        stg_name = stg["name"]
        stg_code = stg["code"]
        scores_dict = {}
        for sq in squads:
            score = squad_diagnostics[sq.code].stage_scores[i].adoption_degree
            scores_dict[sq.code] = score

        avg_val = round(sum(scores_dict.values()) / num_squads, 1)
        val_a = scores_dict.get("squad-a", 0.0)
        val_b = scores_dict.get("squad-b", 0.0)
        val_c = scores_dict.get("squad-c", 0.0)

        stage_rows.append(
            StageBenchmarkRow(
                stage=stg_name,
                stage_code=stg_code,
                scores=scores_dict,
                squad_a_pct=val_a,
                squad_b_pct=val_b,
                squad_c_pct=val_c,
                average_pct=avg_val,
            )
        )

    # 3. Resumo Global
    global_scores: dict[str, float] = {}
    for sq in squads:
        global_scores[sq.code] = squad_diagnostics[sq.code].global_adoption_degree

    org_avg = round(sum(global_scores.values()) / num_squads, 1)
    ad_a = global_scores.get("squad-a", 0.0)
    ad_b = global_scores.get("squad-b", 0.0)
    ad_c = global_scores.get("squad-c", 0.0)

    squad_items = [
        BenchmarkSquadItem(
            id=sq.id,
            code=sq.code,
            name=sq.name,
            purdue_short=sq.purdue_short,
        )
        for sq in squads
    ]

    extra_fields = {
        f"{sq.code.replace('-', '_')}_pct": score
        for sq.code, score in global_scores.items()
        if sq.code not in ("squad-a", "squad-b", "squad-c")
    }

    return BenchmarkSummary(
        squads=squad_items,
        dimensions=dimension_rows,
        stages=stage_rows,
        global_summary=GlobalSummaryBenchmark(
            squad_a_pct=ad_a,
            squad_b_pct=ad_b,
            squad_c_pct=ad_c,
            organization_average_pct=org_avg,
            scores=global_scores,
            **extra_fields,
        ),
    )


# -----------------------------------------------------------------------------
# Rotas Web (Frontend HTML5)
# -----------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard(request: Request, session: Session = Depends(get_session)):
    """Renderiza a página principal do dashboard analítico."""
    squads = session.exec(select(Squad).order_by(Squad.id)).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"squads": squads},
    )
