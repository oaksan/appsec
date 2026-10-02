# Implementation Plan: Gestão de Squads, Edição de Auditoria e Benchmark StH-AppSec

**Branch**: `002-squad-audit-management` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-squad-audit-management/spec.md`

---

## Summary

O objetivo desta feature é evoluir o sistema **Zeppelin-AppSec** para suportar a gestão ativa do ciclo de vida de auditorias de segurança e expandir as capacidades de benchmarking comparativo:
1. **Edição e Persistência de Auditoria**: Permitir alterar os níveis de maturidade (AL0 a AL4) de qualquer squad diretamente na interface web ou via API REST (`PUT /api/diagnostics/{squad_id_or_code}`), persistindo as alterações no SQLite (`zeppelin.db`) e recalculando instantaneamente os graus de adoção por dimensão ($AD_k$), por estágio, média global e gráficos.
2. **Cadastro Dinâmico de Novas Squads**: Permitir adicionar novas squads industriais via formulário modal ou API REST (`POST /api/squads`), com botão único de cadastro integrado ao lado do seletor de squads e inicialização automática das 40 afirmações com AL0 para avaliação progressiva.
3. **Matriz de Benchmarking por Estágio StH-AppSec**: Introduzir uma segunda matriz comparativa completa baseada na Tabela 4.2 da dissertação de referência (`docs/SDL.pdf`), comparando o Grau de Adoção por Estágio (Estágios A ao E) de todas as squads cadastradas em conjunto com a Média Geral da Organização, com rodapé padronizado idêntico à matriz por dimensão SMAF sob o rótulo **GRAU DE ADOÇÃO GLOBAL (AD%)**, exibindo os valores calculados de cada equipe e a média geral.
4. **Filtros por Estágio StH-AppSec no Catálogo**: Acrescentar pills de filtro por Estágio StH sob nomenclatura evolutiva padronizada (`Todos (40)`, `Reactive (3)`, `Agile (10)`, `CSI - Continuous Security Integration (8)`, `CSD - Continuous Security Deployment (9)`, `CSO - Continuous Security Operation (10)`) na seção renomeada para **"Catálogo e Auditoria Zeppelin-AppSec"**, combinando-se harmonicamente ao seletor de `Dimensão SMAF:`.
5. **Exclusão de Squad com Limpeza em Cascata**: Disponibilizar botão para exclusão da squad ativa na interface (com diálogo modal de confirmação) e endpoint REST correspondente (`DELETE /api/squads/{squad_id_or_code}`), executando remoção em cascata transacional de seus registros em `assessment_answer` e `squad` no SQLite `zeppelin.db`, selecionando automaticamente outra squad remanescente e atualizando o painel e matrizes de benchmarking em tempo real.

---

## Technical Context

- **Language/Version**: Python 3.10+ (ambiente validado: Python 3.13)
- **Primary Dependencies**: `fastapi`, `uvicorn`, `sqlmodel`, `pydantic` v2, `pandas`, `openpyxl`, `jinja2`
- **Storage**: SQLite relacional local (`zeppelin.db`) gerenciado via SQLModel / SQLAlchemy ORM
- **Testing**: `pytest`, `httpx` (TestClient do FastAPI para testes unitários, de integração e regressão)
- **Target Platform**: Servidor Linux / multiplataforma, acessível via navegadores web modernos (Chrome, Firefox, Safari, Edge)
- **Project Type**: Aplicação web com backend RESTful assíncrono e frontend dinâmico leve (HTML5, Tailwind CSS via CDN, Chart.js via CDN)
- **Performance Goals**: 
  - Criação de squad com 40 respostas em < 100ms.
  - Atualização em lote de auditoria e recálculo determinístico em < 50ms.
  - Exclusão de squad e limpeza em cascata em < 50ms.
  - Renderização instantânea dos novos scores e gráficos na interface (< 200ms).
- **Constraints**: 
  - Manter rigor matemático absoluto: pesos AL0=0.0, AL1=0.1, AL2=0.3, AL3=0.6, AL4=1.0; fórmulas $AD_k = \frac{\sum peso_i}{n_k} \times 100\%$ e $AD_{global} = \frac{1}{6} \sum AD_k$.
  - Preservar integridade dos dados das 3 squads canônicas já semeadas no banco.
  - Não permitir exclusão caso reste apenas 1 squad no sistema (impedindo que o dashboard fique órfão).
  - Não introduzir ferramentas de build JavaScript (zero npm/webpack/vite); manter código limpo em vanilla JS.
- **Scale/Scope**: Catálogo imutável de 40 afirmações, $N$ squads industriais (3 canônicas + squads adicionadas dinamicamente), 6 dimensões SMAF e 5 estágios StH-AppSec.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio Constitucional | Requisito da Constituição | Status no Plano | Verificação |
|---|---|---|---|
| **I. Modelo Evolutivo StH-AppSec & Tripla Rastreabilidade** | 5 estágios StH (A a E), catálogo de 40 afirmações DX, mapeamento integral SMAF (6 dims), SAMM v2.0 e DSOMM v5.0.2. | **PASS** | Todas as novas squads herdam os vínculos das 40 afirmações com dimensões e estágios; a nova matriz de benchmark reflete exatamente os 5 estágios da Tabela 4.2 da dissertação. |
| **II. Modelagem Matemática & Escala AL0–AL4** | Escala de 5 níveis (AL0=0.0, AL1=0.1, AL2=0.3, AL3=0.6, AL4=1.0). $AD_k = \frac{\sum peso}{n_k} \times 100\%$ e $AD_{global} = \frac{1}{6} \sum AD_k$. | **PASS** | Módulo de cálculo determinístico reutilizado para auditorias editadas e novas squads, garantindo consistência matemática em 100% dos cálculos. |
| **III. Identidade Visual & Gráficos Padronizados** | Paleta executiva (Navy `#1B365D`, Steel `#2F5496`, Royal `#4472C4`, Verde `#A8D08D`), tabelas executivas limpas. | **PASS** | Formulário modal, botão de exclusão com confirmação segura, botões de edição/salvar, pills de filtro de estágios e a nova tabela de benchmarking seguem rigorosamente a paleta e os padrões tipográficos corporativos. |
| **IV. Arquitetura Técnica Enxuta** | Python, FastAPI, SQLModel/Pydantic, SQLite `zeppelin.db`, HTML5, Tailwind CSS via CDN, Chart.js via CDN. | **PASS** | Sem novas bibliotecas ou ferramentas de empacotamento pesadas. Adição de DTOs e endpoints claros no backend e handlers em `static/app.js`. |
| **V. Integridade Canônica & Seeds Obrigatórios** | Preservação das cargas iniciais das planilhas Excel e garantia de não-regressão para as 3 squads canônicas. | **PASS** | Operações idempotentes de seed preservam squads existentes sem sobrescrever alterações do usuário se o banco já estiver inicializado. |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-squad-audit-management/
├── plan.md              # Este plano de implementação
├── research.md          # Fase 0: Pesquisa, análise de impacto e decisões de design
├── data-model.md        # Fase 1: Novos DTOs Pydantic e modelo de dados estendido
├── quickstart.md        # Fase 1: Guia prático de execução e validação dos novos fluxos
├── contracts/           # Fase 1: Especificação detalhada dos contratos de API REST
│   ├── squad-create-api.md      # POST /api/squads
│   ├── squad-delete-api.md      # DELETE /api/squads/{squad_id_or_code}
│   ├── audit-update-api.md      # PUT /api/diagnostics/{squad_id_or_code}
│   └── benchmark-stages-api.md  # GET /api/benchmark
└── checklists/
    └── requirements.md  # Checklist de validação de qualidade dos requisitos
```

### Source Code (repository root)

```text
.
├── models.py            # DTOs: SquadCreate, AnswerUpdateItem, AuditUpdateRequest, BenchmarkSquadItem, StageBenchmarkRow, BenchmarkSummary estendido
├── database.py          # Conexão SQLite (zeppelin.db) e rotinas de persistência
├── main.py              # Endpoints: POST /api/squads, DELETE /api/squads/{squad_id_or_code}, PUT /api/diagnostics/{squad_id_or_code}, GET /api/benchmark
├── templates/
│   └── index.html       # Renomeação do Catálogo, botão/modal de Nova Squad, botão/modal de Exclusão de Squad, pills de filtro de Estágio StH e tabelas de Benchmark
├── static/
│   └── app.js           # Lógica cliente para edição interativa (dropdowns AL), submit de auditoria, modal de nova squad, exclusão com confirmação e reload dinâmico
├── tests/
│   ├── test_math.py     # Testes de rigor matemático
│   ├── test_seed.py     # Testes de integridade da carga inicial
│   └── test_api.py      # Testes de API: criação de squad, exclusão de squad com cascade, edição de respostas, persistência e benchmarking dinâmico
└── zeppelin.db          # Base de dados SQLite local
```

**Structure Decision**: Mantém-se o modelo monorepo direto e consolidado, expandindo os módulos existentes (`models.py`, `main.py`, `templates/index.html`, `static/app.js` e `tests/test_api.py`) sem fragmentação desnecessária.

---

## Complexity Tracking

*Nenhuma violação aos princípios da Constituição foi identificada.*

| Decisão | Alternativa Rejeitada | Justificativa |
|---|---|---|
| Adicionar 40 respostas AL0 imediatamente na criação de Squad | Criar respostas sob demanda ao avaliar cada afirmação | Garante consistência relacional estrita: toda squad tem exatamente 40 respostas no banco, facilitando joins, cálculos estatísticos e benchmarking. |
| Atualização em lote via `PUT /api/diagnostics/{code}` | Atualizações granulares via `PATCH /api/answers/{id}` por item | Evita dezenas de requisições de rede individuais ao salvar uma auditoria; permite salvar o estado completo da avaliação de uma vez e receber o diagnóstico consolidado recalculado. |
| Exclusão atômica com limpeza em cascata via `DELETE /api/squads/{code}` | Soft delete (`is_active = false`) | Hard delete com remoção em cascata de `assessment_answer` e `squad` garante que agregações de benchmark e seletores reflitam os dados reais sem poluir o schema relacional com flags booleanas extras. |
| Benchmarking dinâmico com colunas por squad na mesma resposta | Endpoints separados para cada tabela de benchmark | O endpoint `GET /api/benchmark` já centraliza a visão executiva organizacional. Retornar tanto dimensões quanto estágios em uma única requisição reduz a latência e simplifica o frontend. |
