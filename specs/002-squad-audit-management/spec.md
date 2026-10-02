# Feature Specification: Gestão de Squads, Edição de Auditoria e Benchmark StH-AppSec

**Feature Branch**: `002-squad-audit-management`

**Created**: 2026-09-23

**Status**: Draft

**Input**: User description: "preciso de um botão para excluir uma squad. Renomeie 'Catálogo e Auditoria das 40 Afirmações Atômicas' por 'Catálogo e Auditoria Zeppelin-AppSec'. renomei CSI (Continuous Security Integration) por CSI - Continuous Security Integration, CSD (Continuous Security Deployment) por CSD - Continuous Security Deployment e CSO (Continuous Security Operation) por CSO - Continuous Security Operation"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Edição e Persistência da Auditoria de uma Squad (Priority: P1) 🎯 MVP

Como avaliador de segurança de aplicações, Security Champion ou líder técnico, quero alterar os níveis de institucionalização (AL0 a AL4) assinalados para qualquer uma das 40 afirmações atômicas de uma squad selecionada e salvar essas alterações de forma persistente no banco de dados local, para que o diagnóstico reflita com precisão o progresso técnico da equipe e seja preservado entre sessões.

**Why this priority**: Esta funcionalidade transforma o Zeppelin-AppSec de um visualizador de diagnósticos estáticos em um instrumento vivo de diagnóstico e gestão contínua de maturidade. É o requisito mais crítico para capacitar os usuários a realizar novas avaliações e evoluções em suas equipes.

**Independent Test**: Pode ser testado de forma independente selecionando uma squad existente (ex.: Squad A), acionando o modo de edição, alterando o nível de uma ou mais práticas (ex.: alterando AO.01 de AL3 para AL4), acionando o salvamento e recarregando a página no navegador para confirmar que os novos valores e os cálculos derivados de $AD_{SMAF}$, $AD_{StH}$ e $AD_{global}$ foram persistidos e recalculados com precisão.

**Acceptance Scenarios**:

1. **Given** que o usuário está visualizando o diagnóstico de uma squad, **When** ativa o modo de edição e altera o nível de institucionalização de uma afirmação (ex.: de AL0 para AL3), **Then** o sistema exibe feedback visual imediato do novo peso e atualiza os indicadores provisórios.
2. **Given** que o usuário realizou modificações na auditoria de uma squad, **When** clica na ação de salvar, **Then** o sistema persiste as alterações no banco de dados local, exibe confirmação de sucesso e recalcula os cards de métricas e gráficos em tempo real.
3. **Given** que uma squad teve seus dados atualizados e salvos, **When** a página é recarregada ou a squad é selecionada novamente, **Then** todos os níveis assinalados e os novos valores de Grau de Adoção são restaurados com fidelidade.

---

### User Story 2 - Cadastro e Persistência de Nova Squad (Priority: P2)

Como gestor corporativo de AppSec ou administrador do sistema, quero cadastrar uma nova squad informando nome, camada de automação industrial no Modelo Purdue (ISA-95) e escopo de atuação, inicializando automaticamente suas 40 afirmações atômicas, para que novas equipes da organização possam ser auditadas e incorporadas ao ecossistema do Zeppelin-AppSec.

**Why this priority**: Permite expandir o uso da ferramenta para além das 3 equipes industriais canônicas do estudo piloto inicial, viabilizando o monitoramento corporativo de qualquer squad da empresa.

**Independent Test**: Pode ser testado abrindo o formulário de cadastro de nova squad, preenchendo os campos obrigatórios (nome, nível Purdue, descrição), submetendo o formulário e verificando se a nova squad passa a figurar imediatamente no seletor de squads e na lista de equipes, com suas 40 afirmações atômicas prontas para receberem auditoria.

**Acceptance Scenarios**:

1. **Given** que o usuário acessa a opção de adicionar nova squad, **When** preenche o nome da squad (ex.: "Squad D"), seleciona a camada Purdue (ex.: "Nível 3 — MES") e submete o formulário, **Then** o sistema valida os dados, cria a equipe no banco de dados e inicializa suas 40 respostas com valores padrão (AL0).
2. **Given** a conclusão do cadastro de uma nova squad, **When** o usuário consulta o seletor principal de equipes, **Then** a nova squad aparece disponível para seleção imediata, carregando seu painel diagnóstico com Grau de Adoção inicial.
3. **Given** uma tentativa de cadastrar uma squad com nome em branco ou dados incompletos, **When** o formulário é submetido, **Then** o sistema impede o envio e destaca os campos obrigatórios com mensagens claras.

---

### User Story 3 - Matriz de Benchmarking por Estágio StH-AppSec (Priority: P3)

Como tomador de decisão executivo ou CISO, quero visualizar no painel de benchmarking a matriz comparativa de adoção por Estágio StH-AppSec (Estágios A ao E) em conjunto com a matriz existente por dimensão SMAF, para avaliar em qual degrau da jornada de maturidade (Reactive, Agile, CSI, CSD, CSO) cada squad se encontra e comparar com a média corporativa.

**Why this priority**: Fornece uma perspectiva evolutiva complementar à visão dimensional do SMAF, espelhando a Tabela 4.2 da dissertação de referência e permitindo diagnosticar a progressão da cultura e automação de segurança contínua.

**Independent Test**: Pode ser testado abrindo a seção de benchmark e validando a presença de duas matrizes analíticas completas: a matriz por dimensão SMAF (Governança, Arquitetura, Desenvolvimento, Construção, Testes, Operações) e a matriz por estágio StH-AppSec (Estágio A ao E), ambas exibindo os percentuais comparativos de cada equipe e a coluna de média geral.

**Acceptance Scenarios**:

1. **Given** a abertura da seção de benchmark organizacional, **When** o relatório comparativo é exibido, **Then** o sistema apresenta a matriz por dimensão SMAF e a matriz por estágio StH-AppSec lado a lado ou em seções correlacionadas.
2. **Given** a matriz por estágio StH-AppSec, **When** o usuário examina os 5 estágios (A ao E), **Then** cada linha exibe os Graus de Adoção percentuais de cada squad avaliada e a média calculada para aquele estágio específico.

---

### User Story 4 - Filtragem por Estágio StH no Catálogo Zeppelin-AppSec (Priority: P4)

Como analista de segurança ou desenvolvedor consultando o "Catálogo e Auditoria Zeppelin-AppSec", quero dispor de botões de filtro rápido por Estágio StH-AppSec (`Todos (40)`, `Reactive (3)`, `Agile (10)`, `CSI - Continuous Security Integration (8)`, `CSD - Continuous Security Deployment (9)` e `CSO - Continuous Security Operation (10)`), de forma análoga aos filtros com rótulo "Dimensão SMAF:", para auditar práticas focadas em etapas específicas do ciclo de desenvolvimento de software.

**Why this priority**: Acelera a navegação e a experiência de auditoria do usuário (DX), permitindo que times que estão trabalhando em pipelines de CI filtrem instantaneamente o Estágio C (`CSI - Continuous Security Integration`), ou times focados em produção filtrem o Estágio E (`CSO - Continuous Security Operation`).

**Independent Test**: Pode ser testado selecionando qualquer botão de filtro de estágio StH (ex.: "CSI - Continuous Security Integration (8)") e confirmando que a tabela exibe com precisão exatamente as 8 afirmações pertencentes àquele estágio, integrando-se sem atritos aos filtros de dimensão SMAF e busca por texto.

**Acceptance Scenarios**:

1. **Given** a tabela na seção "Catálogo e Auditoria Zeppelin-AppSec", **When** o usuário clica no filtro "CSI - Continuous Security Integration (8)", **Then** a tabela lista apenas as 8 afirmações atômicas correspondentes à integração contínua segura.
2. **Given** que um filtro de estágio StH está ativo, **When** o usuário combina com a busca textual ou altera para "Todos", **Then** a tabela reage imediatamente exibindo os resultados compatíveis com a seleção.

---

### User Story 5 - Exclusão de Squad com Limpeza em Cascata (Priority: P2)

Como gestor corporativo de AppSec ou líder técnico, quero dispor de um botão para excluir uma squad existente diretamente na interface com confirmação prévia, para eliminar equipes criadas por engano ou desativadas, limpando seus dados de avaliação e atualizando imediatamente as matrizes de benchmarking e o painel de diagnósticos.

**Why this priority**: Complementa o ciclo de vida de squads (Criação, Edição, Consulta e Exclusão - CRUD completo), permitindo manter a base de dados corporativa higienizada e livre de equipes testes ou duplicadas.

**Independent Test**: Pode ser testado selecionando uma squad criada (ex.: "Squad Logística"), acionando o botão de exclusão, confirmando a ação no modal/diálogo e verificando que a squad é removida do banco SQLite, retirada do `<select>`, e que as duas matrizes de benchmark são recalculadas sem a presença da squad excluída.

**Acceptance Scenarios**:

1. **Given** que o usuário está visualizando os dados de uma squad, **When** clica no botão "Excluir Squad" e confirma a operação, **Then** o sistema remove a squad e todas as suas 40 respostas associadas do banco de dados local SQLite `zeppelin.db`.
2. **Given** a confirmação da exclusão, **When** a remoção é processada com sucesso, **Then** o sistema seleciona automaticamente outra squad disponível (ex.: a primeira squad da lista), recarrega o painel diagnóstico e recalcula as matrizes de benchmark por dimensão SMAF e estágio StH sem refresh de página.
3. **Given** que o usuário clicou no botão "Excluir Squad", **When** rejeita ou cancela a confirmação, **Then** a operação é abortada sem qualquer alteração no banco de dados e os dados da squad permanecem intactos.

---

### Edge Cases

- **Tentativa de salvar auditoria sem selecionar nível em alguma prática**: O sistema deve garantir que todas as 40 práticas possuam um nível válido assinalado (entre AL0 e AL4) antes de confirmar o salvamento.
- **Nome de squad duplicado**: O sistema deve validar a unicidade do identificador da squad e notificar o usuário amigavelmente caso já exista uma equipe com identificador similar.
- **Exclusão de squad em uso**: Ao excluir a squad atualmente ativa em tela, o sistema deve transicionar suavemente para a próxima squad disponível para evitar estados nulos ou inconsistências visuais no painel.
- **Tentativa de excluir quando resta apenas uma squad**: O sistema deve alertar o usuário e impedir a exclusão se for a única squad remanescente no sistema para manter a consistência do painel.
- **Interrupção de conexão durante o salvamento**: Em caso de falha de rede ou de comunicação com o servidor local, os dados alterados em tela devem ser preservados e um alerta amigável de erro deve ser apresentado, permitindo nova tentativa de envio sem perda do progresso preenchido.
- **Múltiplos filtros combinados sem correspondência**: Caso a combinação de filtro de dimensão SMAF, filtro de estágio StH e termo de busca textual resulte em zero itens, a tabela deve apresentar uma mensagem orientativa e um botão para redefinir os filtros.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE permitir a criação de novas squads através de formulário interativo, capturando nome, nível de automação industrial no Modelo Purdue (ISA-95: Nível 2 OT, Nível 3 MES, Nível 4 ERP ou categorias equivalentes) e descrição operacional.
- **FR-002**: Ao criar uma nova squad, o sistema DEVE inicializar automaticamente registros de avaliação para todas as 40 afirmações atômicas no banco de dados local com nível inicial padrão AL0 (Não Adotada, peso 0,00).
- **FR-003**: O sistema DEVE fornecer funcionalidade de edição da avaliação de uma squad existente, permitindo que o usuário altere interativamente o nível de institucionalização (AL0 a AL4) de qualquer uma das 40 afirmações atômicas.
- **FR-004**: O sistema DEVE fornecer mecanismo de persistência que salve as alterações de auditoria no banco de dados relacional local (`zeppelin.db`), garantindo a preservação dos dados após recarregamento da página e reinicialização da aplicação.
- **FR-005**: Ao salvar uma auditoria, o sistema DEVE recalcular e atualizar dinamicamente no painel o Grau de Adoção Global ($AD_{global}$), as pontuações das 6 dimensões SMAF, as pontuações dos 5 estágios StH-AppSec e os cartões de métricas.
- **FR-006**: O sistema DEVE manter a matriz de benchmarking de adoção por dimensão SMAF existente.
- **FR-007**: O sistema DEVE adicionar uma segunda matriz de benchmarking consolidada, comparando o Grau de Adoção por Estágio StH-AppSec (Estágios A ao E) entre as squads cadastradas e a média geral da organização, em consonância com a Tabela 4.2 da dissertação de referência. A última linha desta tabela DEVE ser formatada e calculada identicamente à matriz por dimensão SMAF, sob o rótulo **GRAU DE ADOÇÃO GLOBAL (AD%)**, exibindo o Grau de Adoção Global de cada squad e a média geral organizacional na última coluna.
- **FR-008**: Na seção **"Catálogo e Auditoria Zeppelin-AppSec"**, o sistema DEVE exibir o rótulo **"Dimensão SMAF:"** antes das pills de dimensões, e disponibilizar controles de filtro rápido por Estágio StH-AppSec nomeados por sua nomenclatura: `Todos (40)`, `Reactive (3)`, `Agile (10)`, `CSI - Continuous Security Integration (8)`, `CSD - Continuous Security Deployment (9)` e `CSO - Continuous Security Operation (10)`.
- **FR-009**: O sistema DEVE validar os dados submetidos na edição de auditoria, rejeitando requisições com níveis fora da escala oficial AL0 a AL4 (pesos 0.0, 0.1, 0.3, 0.6, 1.0).
- **FR-010**: O sistema DEVE manter a integridade histórica dos dados canônicos iniciais das Squads A, B e C, permitindo que sejam editados ou que novas squads coexistam no mesmo banco de dados relacional.
- **FR-011**: O seletor de squads da interface DEVE atualizar dinamicamente sua listagem sempre que uma nova squad for adicionada ou excluída, mantendo um único botão **"+ Nova Squad"** alinhado ao lado do campo de seleção.
- **FR-012**: O sistema DEVE fornecer funcionalidade para excluir uma squad existente através de botão de exclusão na interface e endpoint REST correspondente (`DELETE /api/squads/{squad_id_or_code}`), removendo em cascata todos os seus registros de avaliação (`assessment_answer`) do banco de dados local SQLite.
- **FR-013**: A exclusão de uma squad DEVE solicitar confirmação prévia do usuário para prevenir perda acidental de dados. Após a exclusão confirmada, o sistema DEVE remover a squad do seletor, selecionar automaticamente outra squad remanescente, recarregar o diagnóstico e atualizar dinamicamente as matrizes de benchmarking e gráficos sem recarga da página.

### Key Entities

- **Squad (Equipe de Engenharia)**: Entidade que representa a equipe avaliada. Atributos: identificador numérico, código textual (slug unívoco), nome descritivo, nível Purdue, rótulo curto Purdue, descrição detalhada e timestamp de criação.
- **Afirmação Atômica (Item do Catálogo)**: Entidade com as 40 práticas técnicas imutáveis. Atributos: código (ex.: AO.01), declaração simplificada voltada a DX, dimensão SMAF, estágio StH, referências SAMM e DSOMM.
- **Resposta de Avaliação (Assessment Answer)**: Entidade que associa uma squad a uma afirmação. Atributos: identificador da squad, identificador da afirmação, nível assinalado (inteiro 0 a 4) e peso matemático correspondente (0.0 a 1.0).
- **Matriz de Benchmark StH-AppSec**: Estrutura analítica que consolida o Grau de Adoção de cada estágio StH (A ao E) para todas as squads ativas e calcula a média geral da organização para cada estágio.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O salvamento das alterações de uma auditoria completa (40 itens) é processado e persistido no banco de dados local em menos de 1 segundo.
- **SC-002**: O recálculo de todas as métricas ($AD_{global}$, dimensões SMAF e estágios StH) e a re-renderização dos gráficos ocorrem de forma imediata na interface após a confirmação do salvamento.
- **SC-003**: A matriz de benchmark por estágio StH-AppSec reflete 100% de precisão matemática para os 5 estágios evolutivos de todas as squads registradas.
- **SC-004**: O cadastro de uma nova squad é concluído em formulário de passo único em menos de 30 segundos pelo usuário, ficando imediatamente disponível no seletor de squads.
- **SC-005**: Os filtros rápidos de dimensão SMAF e estágio StH respondem instantaneamente (< 100ms) ao clique do usuário, sem recarga de página.
- **SC-006**: A exclusão de uma squad e a limpeza em cascata de suas 40 respostas associadas é processada no banco local em menos de 500ms, atualizando o seletor e as matrizes de benchmark instantaneamente.

---

## Assumptions

- O banco de dados local utilizado para persistência continuará sendo o arquivo SQLite `zeppelin.db` do projeto.
- As novas squads cadastradas utilizam a mesma base imutável das 40 afirmações atômicas de segurança contínua formalizadas na Constituição do projeto.
- A edição da auditoria permite modificar qualquer uma das 40 afirmações de uma squad simultaneamente ou individualmente, com submissão em lote (batch update) para garantir consistência transacional atômica.
- A exclusão de uma squad remove deterministicamente a entidade `Squad` e todos os seus registros associados em `assessment_answer` através de exclusão em cascata transacional no SQLite `zeppelin.db`.
