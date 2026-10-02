# Implementation Plan: Painel Diagnóstico e Analítico Zeppelin-AppSec

**Branch**: `001-diagnostic-dashboard` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-diagnostic-dashboard/spec.md`

---

## Summary

O objetivo desta implementação é desenvolver o sistema web do **Zeppelin-AppSec**, um instrumento analítico e executivo para diagnóstico de segurança contínua de software (DevSecOps) baseado na dissertação IFES 2026. A solução é composta por:
1. **Backend em Python com FastAPI e SQLModel**: Prover APIs RESTful tipadas para listagem das 40 afirmações atômicas, das 3 squads industriais (Modelo Purdue / ISA-95) e dos diagnósticos calculados.
2. **Módulo de Cálculo Matemático**: Implementar a lógica determinística da escala de institucionalização (AL0 a AL4) com cálculo do Grau de Adoção por agrupamento ($AD_k$) e global ($AD_{global}$).
3. **Persistência Relacional e Seeding Automático**: Banco de dados SQLite (`zeppelin.db`) com inicialização idempotente das sementes extraídas de `docs/zeppelin_appsec_40_afirmacoes.xlsx` e `docs/simulacao_zeppelin_appsec_3_squads.xlsx`.
4. **Interface e Visualização Gráfica**: Dashboard em HTML5 semântico com Tailwind CSS (CDN) e gráficos interativos via Chart.js (Radar SMAF e Barras StH) seguindo a identidade visual corporativa do Zeppelin Analytics (`docs/zeppelin_analytics_report_v1.xlsx`).

---

## Technical Context

- **Language/Version**: Python 3.10+ (ambiente validado: Python 3.13)
- **Primary Dependencies**: `fastapi`, `uvicorn`, `sqlmodel`, `pydantic` v2, `pandas`, `openpyxl`, `jinja2`
- **Storage**: SQLite relacional no arquivo local `zeppelin.db` via SQLModel / SQLAlchemy ORM
- **Testing**: `pytest`, `httpx` (para testes de integração com TestClient do FastAPI)
- **Target Platform**: Servidor Linux / multiplataforma, acessível via navegadores web modernos (desktop, tablet, mobile)
- **Project Type**: Aplicação web com backend RESTful e frontend dinâmico leve (SPA leve acoplada)
- **Performance Goals**: Carga inicial do banco de dados < 500ms; tempo de resposta de endpoints de diagnóstico < 50ms; renderização de gráficos no cliente < 200ms
- **Constraints**: Ausência de compiladores complexos de frontend (zero dependência de Node.js/npm); cálculos matemáticos com precisão de ponto flutuante idêntica à dissertação (Squad A: 20,3%; Squad B: 47,0%; Squad C: 88,7%; Média Geral: 52,0%)
- **Scale/Scope**: 40 afirmações atômicas, 3 squads industriais do Modelo Purdue, 6 dimensões SMAF, 5 estágios StH-AppSec

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio Constitucional | Requisito da Constituição | Status no Plano | Verificação |
|---|---|---|---|
| **I. Modelo Evolutivo StH-AppSec & Tripla Rastreabilidade** | 5 estágios StH (A a E), catálogo de 40 afirmações DX, mapeamento integral SMAF (6 dims), SAMM v2.0 (100%) e DSOMM v5.0.2 (250 IDs). | **PASS** | Mapeado no `models.py` (`Statement`) e alimentado diretamente a partir de `docs/zeppelin_appsec_40_afirmacoes.xlsx`. |
| **II. Modelagem Matemática & Escala AL0–AL4** | Escala de 5 níveis (AL0=0%, AL1=10%, AL2=30%, AL3=60%, AL4=100%). $AD_k = \frac{\sum peso}{n_k} \times 100\%$ e $AD_{global} = \frac{1}{6} \sum AD_k$. | **PASS** | Implementado em módulo puro de cálculo em `models.py`/serviço e validado por testes unitários com valores canônicos. |
| **III. Identidade Visual & Gráficos Padronizados** | Paleta executiva (Navy `#1B365D`, Steel `#2F5496`, Royal `#4472C4`, Verde `#A8D08D`), Radar SMAF e Barras StH via Chart.js. | **PASS** | Configurado em `static/app.js` e `templates/index.html` com Chart.js CDN respeitando rigorosamente o estilo de `docs/zeppelin_analytics_report_v1.xlsx`. |
| **IV. Arquitetura Técnica Enxuta** | Python, FastAPI, SQLModel/Pydantic, SQLite `zeppelin.db`, HTML5, Tailwind CSS via CDN, Chart.js via CDN. | **PASS** | Arquitetura monorepo direta sem complexidade de microserviços ou bundlers Node.js. |
| **V. Integridade Canônica & Seeds Obrigatórios** | Carga inicial obrigatória de 40 afirmações e 3 squads simuladas (Purdue Níveis 2, 3 e 4). | **PASS** | Implementado em `database.py` (`seed_database`) e invocado automaticamente no lifespan do FastAPI em `main.py`. |

---

## Project Structure

### Documentation (this feature)

```text
specs/001-diagnostic-dashboard/
├── plan.md              # Este plano de implementação
├── research.md          # Fase 0: Pesquisa, análise e decisões de design
├── data-model.md        # Fase 1: Esquema de entidades SQLModel e DTOs Pydantic
├── quickstart.md        # Fase 1: Guia prático de execução e validação
├── contracts/           # Fase 1: Contratos detalhados de API REST
│   ├── statements-api.md
│   ├── squads-api.md
│   ├── diagnostics-api.md
│   └── benchmark-api.md
├── checklists/
│   └── requirements.md  # Checklist de validação de qualidade dos requisitos
└── tasks.md             # Fase 2: Lista de tarefas de implementação (gerado pelo /speckit.tasks)
```

### Source Code (repository root)

```text
.
├── models.py            # Entidades SQLModel (Squad, Statement, AssessmentAnswer) e DTOs Pydantic
├── database.py          # Conexão SQLite (zeppelin.db), session generator e carga idempotente (seed_database)
├── main.py              # Aplicação FastAPI, lifespan hook, rotas /api/* e renderização do template
├── templates/
│   └── index.html       # Dashboard responsivo em HTML5 estruturado com Tailwind CSS (CDN)
├── static/
│   └── app.js           # Gerenciamento de estado frontend, chamadas fetch e renderização Chart.js
├── tests/
│   ├── __init__.py
│   ├── test_math.py     # Testes unitários para conferência matemática estrita de ADk e ADglobal
│   ├── test_seed.py     # Testes de integridade da carga das planilhas Excel (40 itens e 3 squads)
│   └── test_api.py      # Testes de integração dos endpoints REST FastAPI com TestClient
├── requirements.txt     # Dependências Python (fastapi, uvicorn, sqlmodel, pandas, openpyxl, jinja2, pytest, httpx)
├── docs/                # Planilhas canônicas e dissertação de referência
│   ├── SDL.pdf
│   ├── simulacao_zeppelin_appsec_3_squads.xlsx
│   ├── zeppelin_appsec_40_afirmacoes.xlsx
│   └── zeppelin_analytics_report_v1.xlsx
└── zeppelin.db          # Banco de dados SQLite provisionado automaticamente no primeiro startup
```

**Structure Decision**: A estrutura monorepo plana foi escolhida pela aderência direta aos requisitos do usuário e à Constituição v1.0.0. A camada backend expõe endpoints JSON claros (`/api/*`) e serve o frontend leve via Jinja2 e arquivos estáticos, permitindo desenvolvimento rápido, facilidade de manutenção e execução com comando único.

---

## Complexity Tracking

*Nenhuma violação ou exceção aos princípios da Constituição foi identificada. O design mantém a máxima simplicidade e aderência aos requisitos.*

| Aspecto | Decisão Adotada | Justificativa |
|---|---|---|
| Gerenciador de Banco | SQLite local (`zeppelin.db`) | Portabilidade total sem dependência de containers ou bancos externos. |
| Modelagem de Dados | SQLModel | Unificação de modelos ORM e schemas Pydantic v2 sem código redundante. |
| Injeção de Dependências | `Depends(get_session)` do FastAPI | Padrão idiomático, testável e com isolamento transacional por requisição. |
| Frontend | Tailwind CSS CDN + Chart.js CDN | Zero atrito de compilação JS/CSS, mantendo alta qualidade estética e responsividade. |
