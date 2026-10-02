# Research & Decisions: Gestão de Squads, Edição de Auditoria e Benchmark StH-AppSec

**Feature**: `002-squad-audit-management`
**Status**: Completed
**Date**: 2026-09-23

---

## 1. Contexto e Objetivos Técnicos

A feature `002-squad-audit-management` expande a solução Zeppelin-AppSec de um visualizador de diagnósticos para uma plataforma operacional completa de gestão contínua de maturidade AppSec, contemplando:
1. **Edição Interativa de Auditoria**: Permitir a alteração dos níveis assinalados (AL0 a AL4) para qualquer uma das 40 afirmações atômicas de uma squad.
2. **Persistência Transacional Local**: Gravação permanente em SQLite (`zeppelin.db`) das novas respostas e recálculo imediato de $AD_{SMAF}$, $AD_{StH}$ e $AD_{global}$.
3. **Cadastro de Novas Squads**: Registro de novas equipes industriais classificadas sob o Modelo Purdue (ISA-95), com inicialização automática de suas 40 práticas.
4. **Matriz de Benchmark por Estágio StH-AppSec**: Inclusão da tabela comparativa de adoção por estágio (A ao E) espelhando a Tabela 4.2 da dissertação.
5. **Filtragem por Estágio StH na Tabela**: Botões de filtro rápido por estágio StH integrados à filtragem por dimensão SMAF e busca textual.

---

## 2. Decisões Arquiteturais e Pesquisa

### Decisão 1: Formato de Atualização da Auditoria (Batch vs Item a Item)

- **Decisão**: Implementar atualização em lote (`PUT /api/diagnostics/{squad_id_or_code}`) enviando a lista completa ou parcial de respostas alteradas em uma única transação atômica.
- **Racional**:
  - Atualizar item a item geraria até 40 requisições HTTP individuais por sessão de edição, aumentando latência e risco de inconsistência.
  - Uma única requisição `PUT` processa todas as alterações dentro de uma única transação SQLite com `session.commit()`, assegurando consistência ACID e tempo de resposta inferior a 50ms.
  - O retorno do endpoint entrega imediatamente o `SquadDiagnosticSummary` recalculado, simplificando a sincronização de estado no frontend.
- **Alternativas Consideradas**:
  - *Auto-save a cada clique com `PATCH`*: Rejeitado por gerar excesso de escritas no banco e recálculos gráficos prematuros enquanto o avaliador ainda está preenchendo a tabela.

### Decisão 2: Geração de Identificador Único (`code`) para Novas Squads

- **Decisão**: Gerar o campo `code` slugificando o nome da squad (ex.: "Squad Logística" -> `squad-logistica`), garantindo unicidade por meio de sufixo numérico caso já exista (`squad-logistica-2`).
- **Racional**:
  - As URLs RESTful e seletores utilizam slugs amigáveis (`/api/diagnostics/squad-a`).
  - O backend assegura que o slug gerado respeite o limite de 50 caracteres e não colida com as squads canônicas (`squad-a`, `squad-b`, `squad-c`).
- **Alternativas Consideradas**:
  - *Usar apenas IDs inteiros*: Rejeitado para manter paridade com a convenção RESTful já adotada.

### Decisão 3: Generalização do Endpoint `/api/benchmark` para N Squads

- **Decisão**: Refatorar `GET /api/benchmark` para consultar dinamicamente todas as squads cadastradas no banco de dados (`session.exec(select(Squad)).all()`), gerando colunas dinâmicas para as squads e calculando a média geral em tempo real.
- **Racional**:
  - O endpoint original fixava apenas as 3 squads iniciais.
  - Ao cadastrar novas squads, a matriz de benchmarking deve exibir todas as equipes ativas e recalcular a média organizacional considerando o conjunto completo de times.
  - O schema da resposta fornecerá tanto a lista estruturada de squads quanto as pontuações dimensionais e de estágio por equipe.
- **Alternativas Consideradas**:
  - *Manter o benchmark restrito às 3 squads canônicas*: Rejeitado pelo requisito explícito de permitir novas squads e compará-las na matriz.

### Decisão 4: UX de Edição da Auditoria e Filtros Combinados

- **Decisão**: 
  1. Fornecer um modo alternável de edição ("Editar Auditoria" / "Salvar Alterações") na tabela de afirmações.
  2. No modo de edição, a coluna "Nível AL" substitui o badge estático por um `<select>` estilizado com os 5 níveis (AL0 a AL4), recalculando o peso visual em tempo real.
  3. Adicionar uma linha dedicada de botões de filtro por Estágio StH (`Todos`, `Reactive`, `Agile`, `CSI - Continuous Security Integration`, `CSD - Continuous Security Deployment`, `CSO - Continuous Security Operation`) na seção renomeada para **"Catálogo e Auditoria Zeppelin-AppSec"**, logo abaixo da linha de filtros com rótulo `Dimensão SMAF:`.
  4. A função de filtragem no JavaScript aplica simultaneamente: `filtro_dimensao AND filtro_estagio AND busca_texto`.
- **Racional**:
  - Permite avaliar a equipe com fluidez e ergonomia visual sem sair da tela principal.
  - A combinação de filtros permite focar, por exemplo, exclusivamente em "Testes e Verificação no Estágio CSI".

### Decisão 5: Exclusão de Squad e Limpeza em Cascata Transacional

- **Decisão**: Implementar `DELETE /api/squads/{squad_id_or_code}` com remoção atômica de todos os 40 registros em `assessment_answer` e da entidade `Squad` no SQLite, exigindo confirmação prévia no frontend através de modal/diálogo de alerta.
- **Racional**:
  - Elimina equipes de teste ou desativadas, mantendo o banco leve e consistente.
  - O hard delete com exclusão em cascata assegura que nenhuma resposta órfã permaneça em `assessment_answer`.
  - O recálculo automático pós-exclusão garante que as matrizes de benchmark e seletores reflitam imediatamente a ausência da equipe.
  - Regra de guarda: O endpoint impede a exclusão se for a única squad restante no banco, prevenindo estados nulos catastróficos no dashboard.
- **Alternativas Consideradas**:
  - *Soft delete com flag `is_active`*: Rejeitado para não sobrecarregar todas as queries e agregações de benchmarking com filtros `WHERE is_active = true`.

---

## 3. Resumo de Riscos e Mitigações

| Risco | Severidade | Mitigação |
|---|---|---|
| Sobrescrita acidental dos dados canônicos da pesquisa | Baixa | Os dados originais continuam salvos imutáveis nas planilhas em `docs/`; o banco `zeppelin.db` pode ser resetado se necessário. |
| Erro de validação de nível inválido via API | Média | Validação estrita via Pydantic (`Field(ge=0, le=4)`) e checagem de integridade relacional. |
| Travamento de concorrência no SQLite durante salvamento | Baixa | SQLite opera em modo WAL com transação curta e isolada por requisição. |

