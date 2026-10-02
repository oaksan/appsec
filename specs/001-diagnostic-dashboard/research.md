# Research & Decisions: Painel Diagnóstico e Analítico Zeppelin-AppSec

**Feature**: `001-diagnostic-dashboard`
**Status**: Completed
**Date**: 2026-09-23

---

## 1. Contexto e Objetivos Técnicos

O projeto Zeppelin-AppSec requer a disponibilização de uma solução web ágil, determinística e desacoplada, composta por:
1. Backend em Python com FastAPI e SQLModel/Pydantic persistindo em SQLite (`zeppelin.db`).
2. Módulo de cálculo matemático rigoroso para a escala de institucionalização (AL0 a AL4) e Grau de Adoção ($AD_k$ e $AD_{global}$).
3. Injeção de dependência e carga inicial automatizada (seeding idempotente) a partir de planilhas Excel canônicas (`docs/zeppelin_appsec_40_afirmacoes.xlsx` e `docs/simulacao_zeppelin_appsec_3_squads.xlsx`).
4. Interface moderna em HTML5 com Tailwind CSS (CDN) e gráficos interativos via Chart.js (Radar SMAF e Barras StH) seguindo a identidade visual corporativa do Zeppelin Analytics.

---

## 2. Decisões Arquiteturais e Pesquisa

### Decisão 1: Gerenciamento do Ciclo de Vida do Banco de Dados e Injeção de Dependências

- **Decisão**: Utilizar o gerenciador de ciclo de vida assíncrono `@asynccontextmanager` do FastAPI (`lifespan`) acoplado ao padrão de gerador de sessões `get_session` com `Depends(get_session)`.
- **Racional**:
  - Os eventos legados `@app.on_event("startup")` foram descontinuados nas versões recentes do FastAPI.
  - O `lifespan` garante que o arquivo `zeppelin.db`, as tabelas e os dados de seed sejam verificados e provisionados antes do atendimento à primeira requisição HTTP.
  - O gerador `get_session` fornece escopo de transação unitário por requisição com fechamento automático no bloco `finally`, prevenindo conexões presas e concorrência indevida no SQLite.
- **Alternativas Consideradas**:
  - *Inicialização manual por script CLI antes de subir a aplicação*: Rejeitado porque aumentaria o atrito de uso e violaria o requisito de inicialização automática ao rodar o servidor.
  - *ORM SQLAlchemy puro sem SQLModel*: Rejeitado pela Constituição v1.0.0, que estabelece SQLModel para unificar validação Pydantic e modelo de banco em classes únicas.

### Decisão 2: Estratégia de Carga de Sementes (Seeding) a partir de Planilhas Excel

- **Decisão**: Implementar a função `seed_database(session)` utilizando `openpyxl` / `pandas` com verificação de idempotência (checagem de contagem prévia de registros).
- **Racional**:
  - `openpyxl` é nativo para leitura direta de planilhas `.xlsx` com células mescladas, fórmulas e estilos preservados.
  - A planilha `docs/zeppelin_appsec_40_afirmacoes.xlsx` possui 40 linhas estruturadas na aba `Afirmações Atômicas`.
  - A planilha `docs/simulacao_zeppelin_appsec_3_squads.xlsx` possui as abas `Squad A`, `Squad B` e `Squad C`, onde a coluna D contém o nível numérico assinalado (0 a 4).
  - O seeder mapeia o valor numérico para a escala (`AL0`, `AL1`, `AL2`, `AL3`, `AL4`) e armazena os pesos numéricos oficiais (0.0, 0.1, 0.3, 0.6, 1.0).
  - A idempotência é garantida checando se já existem 40 afirmações e as 3 squads; se presentes, a carga é ignorada, mantendo o tempo de startup abaixo de 100ms.
- **Alternativas Consideradas**:
  - *Converter as planilhas para JSON estático previamente*: Rejeitado para preservar as planilhas originais fornecidas em `docs/` como fonte canônica viva do projeto.

### Decisão 3: Módulo de Cálculo Matemático do Grau de Adoção ($AD$)

- **Decisão**: Encapsular a lógica matemática em funções puras independentes de banco e reutilizáveis pela camada de serviço/API e pela suíte de testes unitários.
- **Racional**:
  - A fórmula por agrupamento $k$ é:
    $$AD_k = \frac{\sum_{i \in k} peso(AL_i)}{n_k} \times 100\%$$
  - A fórmula global da squad é a média simples das 6 dimensões SMAF:
    $$AD_{global} = \frac{1}{6} \sum_{k \in SMAF} AD_k$$
  - A dissertação estabelece um critério de aceitação não-negociável: $AD_{global}$ da Squad A = 20,3%, Squad B = 47,0%, Squad C = 88,7% e Média Geral = 52,0%.
  - O cálculo desacoplado em módulo dedicado permite testar exaustivamente arredondamentos decimais e casos de borda com `pytest`.
- **Alternativas Consideradas**:
  - *Calcular tudo diretamente no banco com queries SQL aggregators (`AVG`)*: Rejeitado porque o SQLite pode ter variações sutis de arredondamento de float em comparação com as fórmulas exatas do Excel (`AVERAGEIFS`), além de dificultar testes unitários isolados da camada de persistência.

### Decisão 4: Representações Gráficas e Identidade Visual (Chart.js)

- **Decisão**: Utilizar a biblioteca Chart.js (v4.x via CDN) renderizada dinamicamente em `<canvas>` HTML5 com temas de cores configurados via variáveis de identidade corporativa.
- **Racional**:
  - Gráfico Radar (SMAF): 6 vértices representando as 6 dimensões SMAF em ordem lógica. Escala radial (`r: { min: 0, max: 100, ticks: { stepSize: 20 } }`).
  - Gráfico de Barras Empilhadas (StH-AppSec): Eixo X contendo os 5 estágios (Estágio A ao E), com 5 séries empilhadas representando o número de práticas classificadas em AL0, AL1, AL2, AL3 e AL4.
  - Paleta cromática corporativa:
    - Navy Blue (`#1B365D`): Séries principais, cabeçalhos, destaque institucional.
    - Steel Blue (`#2F5496`): Linhas e eixos secundários.
    - Royal Blue (`#4472C4`): Cor de destaque interativa e preenchimento de área do radar com alpha (`rgba(68, 114, 196, 0.25)`).
    - Sucesso / Verde Sálvia (`#A8D08D` / `#E2EFDA`): Indicador de práticas em AL4 e atingimento de metas.
- **Alternativas Consideradas**:
  - *Plotly.js*: Rejeitado por possuir pacote pesado (> 3MB) desnecessário para gráficos bidimensionais padrão.
  - *D3.js*: Rejeitado pela alta complexidade de código imperativo comparado à facilidade declarativa e suporte responsivo do Chart.js.

### Decisão 5: Arquitetura de Frontend e Comunicação com a API

- **Decisão**: Arquitetura monorepo enxuta servida pelo FastAPI, com HTML5 semântico estruturado em Jinja2 (`templates/index.html`), Tailwind CSS via CDN e JavaScript modular vanilla (`static/app.js`).
- **Racional**:
  - Elimina a necessidade de pipelines de compilação Node.js, `npm`, webpack ou Vite, garantindo execução com um único comando (`uvicorn main:app`).
  - `static/app.js` encapsula um gerenciador de estado leve que realiza chamadas `fetch()` para a API REST do FastAPI e atualiza os cartões de métricas, tabela de 40 afirmações e instâncias dos gráficos Chart.js sem recarregar a página.
- **Alternativas Consideradas**:
  - *React/Vue SPA separado*: Rejeitado por violar o princípio de simplicidade operacional da Constituição v1.0.0.

---

## 3. Resumo de Riscos e Mitigações

| Risco Identificado | Severidade | Estratégia de Mitigação |
|---|---|---|
| Inconsistência nos cálculos de AD entre sistema e Excel | Alta | Testes unitários com tolerância rigorosa (`pytest.approx(..., abs=0.1)`) contra os valores das Tabelas 4.1 e 4.2 da dissertação. |
| Lentidão na leitura dos arquivos Excel a cada inicialização | Média | Execução do seeder com verificação prévia de existência de registros na tabela do SQLite (`SELECT count(*)`). |
| Concorrência de escrita no SQLite durante requisições simultâneas | Baixa | Utilização do modo WAL (`PRAGMA journal_mode=WAL;`) e `check_same_thread=False` na engine do SQLite. |

