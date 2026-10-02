# Feature Specification: Painel Diagnóstico e Analítico Zeppelin-AppSec

**Feature Branch**: `001-diagnostic-dashboard`

**Created**: 2026-09-23

**Status**: Draft

**Input**: User description: "Endpoints para listar as 40 afirmações, listar as 3 squads (Purdue Níveis 2, 3 e 4) e obter o diagnóstico consolidado; Módulo de cálculo matemático de AL Dimensão SMAF e Estágios StH-AppSec; Dashboard responsivo com seletor de squad, cards de métricas; Gráficos: Radar SMAF, Barras StH (AL por estágio do StH-AppSec); Fontes de dados: docs/zeppelin_analytics_report_v1.xlsx e docs/simulacao_zeppelin_appsec_3_squads.xlsx."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnóstico e Métricas Executivas por Squad (Priority: P1)

Como gestor de AppSec, engenheiro de segurança ou líder técnico de squad, quero selecionar uma equipe industrial (Squad A - N2 OT, Squad B - N3 MES ou Squad C - N4 ERP) para visualizar instantaneamente seu diagnóstico consolidado de maturidade, incluindo o Grau de Adoção Global ($AD_{global}$) e os cartões de métricas fundamentais, para compreender com precisão a postura e o estágio de segurança contínua da equipe.

**Why this priority**: Esta é a funcionalidade central e o valor primário do Zeppelin-AppSec. Sem a capacidade de consultar e visualizar as métricas de maturidade consolidadas de uma squad específica, a ferramenta não atinge seu propósito diagnóstico.

**Independent Test**: Pode ser testado de forma independente acessando o painel, selecionando individualmente cada uma das três equipes industriais e validando se os cartões de métricas exibem com exatidão os valores consolidados de Grau de Adoção Global (Squad A: 20,3%; Squad B: 47,0%; Squad C: 88,7%) e a contagem de afirmações em cada nível da escala de institucionalização.

**Acceptance Scenarios**:

1. **Given** que o usuário está no painel de diagnóstico, **When** seleciona a "Squad A (Nível 2 OT - Controle de Processos)", **Then** o sistema exibe o Grau de Adoção Global de 20,3% e destaca a concentração de práticas em estágios reativos/iniciais (AL0 a AL2).
2. **Given** que o usuário está visualizando a Squad A, **When** altera a seleção para a "Squad B (Nível 3 MES - Gestão de Operações)", **Then** o sistema atualiza dinamicamente as métricas para exibir o Grau de Adoção Global de 47,0% e a distribuição intermediária de práticas.
3. **Given** que o usuário seleciona a "Squad C (Nível 4 ERP - TI Corporativa)", **Then** o sistema exibe o Grau de Adoção Global de 88,7% com predominância de práticas institucionalizadas (AL4).

---

### User Story 2 - Visualização Gráfica Analítica via Radar SMAF e Barras StH (Priority: P2)

Como tomador de decisão ou analista de segurança, quero visualizar a distribuição de maturidade da squad através de representações gráficas padronizadas (Gráfico Radar cobrindo as 6 Dimensões SMAF e Gráfico de Barras com os níveis AL0 a AL4 por Estágio StH-AppSec), para identificar visualmente assimetrias de segurança, pontos fracos e avanços na jornada evolutiva.

**Why this priority**: A visualização gráfica executiva é indispensável para sintetizar 40 variáveis técnicas em insights acionáveis imediatos para a liderança e para os times de desenvolvimento, permitindo diagnosticar deficiências em dimensões críticas em poucos segundos.

**Independent Test**: Pode ser testado de forma independente verificando se, ao carregar os dados de qualquer squad, o gráfico Radar plota com precisão os 6 eixos dimensionais fixados em escala de 0% a 100% e o gráfico de Barras exibe a contagem exata de práticas em cada um dos 5 estágios evolutivos (A ao E) discriminadas pelos níveis AL0 a AL4.

**Acceptance Scenarios**:

1. **Given** uma squad selecionada, **When** o painel renderiza o gráfico Radar SMAF, **Then** são exibidos os Graus de Adoção específicos nas 6 dimensões (Governança, Arquitetura e Design, Desenvol. e Revisão, Construção e Impl., Testes e Verificação, Operações e Obs.) em uma teia radial delimitada entre 0% e 100%.
2. **Given** o gráfico de Barras StH-AppSec em exibição, **When** o usuário examina os 5 estágios (Estágio A - Reactive, Estágio B - Agile, Estágio C - CSI, Estágio D - CSD, Estágio E - CSO), **Then** cada coluna ilustra a quantidade de afirmações categorizadas por nível de adoção (AL0 a AL4) com diferenciação cromática padronizada e legenda explicativa.

---

### User Story 3 - Consulta e Rastreabilidade do Catálogo das 40 Afirmações Atômicas (Priority: P3)

Como desenvolvedor de software ou Security Champion, quero consultar a lista completa das 40 afirmações atômicas do instrumento, com filtros por dimensão SMAF e estágio StH-AppSec, visualizando a redação simplificada voltada à Experiência do Desenvolvedor (DX) e as referências normativas (OWASP SAMM v2.0 e OWASP DSOMM v5.0.2), para compreender o embasamento de cada item avaliado e orientar planos de ação técnicos.

**Why this priority**: Assegura a transparência metodológica e o valor educativo do instrumento, permitindo que os engenheiros compreendam exatamente o que cada item avalia sem ambiguidade e encontrem as referências nos padrões internacionais de mercado.

**Independent Test**: Pode ser testado de forma independente acessando a visão de catálogo, aplicando filtros por dimensão ou estágio e conferindo se todas as 40 afirmações atômicas são apresentadas com seus códigos únicos, declarações DX e mapeamentos normativos correspondentes.

**Acceptance Scenarios**:

1. **Given** a consulta ao catálogo de afirmações, **When** o usuário filtra pela dimensão "Arquitetura e Design", **Then** são retornadas exatamente as 8 afirmações atômicas dessa dimensão (ARQ.01 a ARQ.04, ARQ.05 a ARQ.08).
2. **Given** a listagem de uma afirmação atômica específica (por exemplo, "ARQ.04"), **When** o usuário inspeciona seus detalhes, **Then** o sistema apresenta a descrição voltada a DX e as referências aos IDs do OWASP DSOMM v5.0.2 e ao OWASP SAMM v2.0.

---

### User Story 4 - Comparativo e Benchmark Industrial Global (Priority: P4)

Como diretor técnico ou CISO corporativo, quero visualizar uma tabela e gráfico comparativo consolidando os diagnósticos das três squads industriais lado a lado com a média geral da organização, para avaliar como a maturidade varia entre as camadas de chão de fábrica (OT), sistemas de manufatura (MES) e TI corporativa (ERP).

**Why this priority**: Viabiliza o benchmarking interno e a análise estratégica multicamadas orientada ao Modelo Purdue, fornecendo subsídios para distribuição de orçamento e priorização de programas corporativos de capacitação em AppSec.

**Independent Test**: Pode ser testado de forma independente selecionando a visão de panorama corporativo / comparativo e verificando se a tabela consolidada reflete a média geral das 6 dimensões e a discriminação entre as 3 squads (20,3% vs 47,0% vs 88,7% e média global de 52,0%).

**Acceptance Scenarios**:

1. **Given** a visão comparativa de benchmarking, **When** o relatório consolidado é carregado, **Then** uma tabela comparativa exibe as 6 dimensões SMAF com as pontuações individuais das Squads A, B e C e a coluna de média geral.
2. **Given** a exibição do comparativo, **When** o usuário analisa o Grau de Adoção Global ($AD_{global}$), **Then** a média geral da organização é confirmada como 52,0%.

---

### Edge Cases

- **Ausência de dados para uma squad**: Caso os dados de uma squad não estejam inicializados, o sistema deve exibir uma mensagem instrutiva amigável informando a necessidade de carga inicial (seeding) sem falhas silenciosas ou erros de tela em branco.
- **Valores inválidos ou corrompidos na escala de adoção**: Caso uma resposta possua valor fora do intervalo de AL0 a AL4, o módulo matemático deve rejeitar o registro, registrar um log de auditoria e impedir o cálculo distorcido de médias.
- **Telas com resolução reduzida (smartphones e tablets)**: O layout do dashboard deve reorganizar os cards de métricas em coluna única e adaptar a escala dos gráficos Chart.js para evitar corte de rótulos e sobreposição de textos em telas com largura inferior a 768px.
- **Navegação rápida entre squads**: A alternância sequencial e rápida entre squads no seletor do dashboard não deve gerar condições de corrida na renderização dos gráficos nem apresentar dados desatualizados de seleções anteriores.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE fornecer mecanismo de consulta estruturado para listar as 40 afirmações atômicas de segurança, contendo código único, declaração simplificada voltada a DX, estágio StH-AppSec, dimensão SMAF, referências do OWASP SAMM v2.0 e referências de atividades do OWASP DSOMM v5.0.2.
- **FR-002**: O sistema DEVE fornecer mecanismo de consulta estruturado para listar as 3 squads industriais canônicas, classificadas segundo os níveis de automação do Modelo Purdue (ISA-95): Squad A (Nível 2 — OT / Controle de Processos), Squad B (Nível 3 — MES / Gestão de Operações) e Squad C (Nível 4 — ERP / TI Corporativa).
- **FR-003**: O sistema DEVE fornecer mecanismo para obter o diagnóstico consolidado de uma squad específica, incluindo o nível assinalado (AL0 a AL4) para cada uma das 40 afirmações, o Grau de Adoção por dimensão SMAF ($AD_{SMAF}$), o Grau de Adoção por estágio StH-AppSec ($AD_{StH}$) e o Grau de Adoção Global ($AD_{global}$).
- **FR-004**: O módulo de cálculo matemático DEVE computar o Grau de Adoção de qualquer agrupamento $k$ ($AD_k$) pela fórmula canônica $AD_k = \frac{\sum_{i \in k} peso(AL_i)}{n_k} \times 100\%$, utilizando os pesos oficiais: AL0 = 0,00; AL1 = 0,10; AL2 = 0,30; AL3 = 0,60; AL4 = 1,00.
- **FR-005**: O módulo de cálculo matemático DEVE computar o Grau de Adoção Global ($AD_{global}$) de cada squad como a média aritmética simples dos Graus de Adoção das 6 dimensões do SMAF: $AD_{global} = \frac{1}{6} \sum_{k \in SMAF} AD_k$.
- **FR-006**: O sistema DEVE disponibilizar uma interface web responsiva contendo um seletor interativo de squad que atualize dinamicamente todos os cartões métricos, gráficos e tabelas diagnósticas.
- **FR-007**: A interface DEVE exibir cards métricos de destaque no topo da página apresentando: Grau de Adoção Global ($AD_{global}$), classificação do Modelo Purdue, estágio StH-AppSec predominante e o quantitativo de práticas em cada nível de institucionalização (AL0 a AL4).
- **FR-008**: O sistema DEVE renderizar um gráfico Radar interativo mapeando o Grau de Adoção nas 6 dimensões do SMAF com escala radial fixada de 0% a 100%, permitindo visualização clara do perfil da squad selecionada.
- **FR-009**: O sistema DEVE renderizar um gráfico de Barras ilustrando a distribuição e contagem das práticas adotadas por estágio StH-AppSec (Estágios A ao E), discriminadas pelos níveis de adoção AL0 a AL4, conforme a representação visual do relatório analítico de referência.
- **FR-010**: A interface DEVE disponibilizar uma tabela detalhada com as 40 afirmações atômicas avaliadas para a squad selecionada, indicando o nível de adoção assinalado, o peso numérico correspondente e filtros rápidos por dimensão SMAF e estágio StH-AppSec.
- **FR-011**: O sistema DEVE disponibilizar uma visualização de panorama comparativo organizacional consolidando as 3 squads industriais e a média corporativa geral para todas as dimensões e estágios.

### Key Entities *(include if feature involves data)*

- **Squad (Equipe de Engenharia / Unidade de Avaliação)**: Entidade que representa o time avaliado. Principais atributos: identificador único, nome descritivo (ex.: "Squad A"), nível no Modelo Purdue / ISA-95 (Nível 2 OT, Nível 3 MES, Nível 4 ERP), descrição do escopo operacional e data do diagnóstico.
- **Afirmação Atômica (Item de Diagnóstico)**: Entidade que representa uma prática técnica atômica de segurança contínua focada em DX. Principais atributos: código oficial unívoco (ex.: AO.01, COD.01, ARQ.01, VER.01, OPE.01), declaração simplificada da prática, estágio StH-AppSec (Estágio A ao E), dimensão SMAF (1 a 6), referência normativa ao OWASP SAMM v2.0 e referências de atividades diretas/correlatas ao OWASP DSOMM v5.0.2.
- **Avaliação e Resposta de Adoção**: Entidade que vincula uma squad a uma afirmação atômica e registra o grau de adoção observado. Principais atributos: identificador da squad, código da afirmação, nível de institucionalização assinalado (AL0, AL1, AL2, AL3 ou AL4) e peso de adoção correspondente (0,00; 0,10; 0,30; 0,60; 1,00).
- **Diagnóstico Consolidado**: Entidade calculada que agrega os resultados diagnósticos de uma squad ou da organização. Principais atributos: identificador da squad, percentual de Grau de Adoção para cada uma das 6 dimensões SMAF, percentual de Grau de Adoção para cada um dos 5 estágios StH-AppSec, Grau de Adoção Global ($AD_{global}$) e contagem agregada de práticas por nível AL.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O painel diagnóstico carrega integralmente e renderiza todos os cards de métricas e gráficos analíticos em menos de 2 segundos após a seleção de qualquer squad ou do panorama global.
- **SC-002**: Os cálculos matemáticos executados pelo sistema apresentam 100% de concordância com os valores de referência da dissertação e das planilhas canônicas, sem divergência nas casas decimais: Squad A = 20,3%; Squad B = 47,0%; Squad C = 88,7%; Média Geral = 52,0%.
- **SC-003**: 100% das 40 afirmações atômicas e suas respectivas correlações com OWASP SAMM v2.0 e OWASP DSOMM v5.0.2 são consultáveis na interface de forma estruturada.
- **SC-004**: O dashboard analítico mantém integridade visual, legibilidade e navegabilidade sem quebra de elementos em telas desktop (>= 1280px), telas de tablets (768px a 1024px) e dispositivos móveis (>= 375px).
- **SC-005**: Usuários avaliadores conseguem interpretar o diagnóstico de uma squad e identificar a dimensão de menor maturidade em menos de 1 minuto de interação com o dashboard.

## Assumptions

- A base de dados inicial do sistema será populada com a carga de sementes extraída diretamente dos arquivos canônicos `docs/zeppelin_appsec_40_afirmacoes.xlsx` e `docs/simulacao_zeppelin_appsec_3_squads.xlsx`.
- O modelo de avaliação considera uma avaliação diagnóstica consolidada por squad, alinhada ao protocolo misto do estudo de validação industrial descrito na dissertação IFES 2026.
- A paleta de cores e a disposição dos elementos gráficos adotam as diretrizes corporativas exemplificadas em `docs/zeppelin_analytics_report_v1.xlsx` (paleta azul marinho `#1B365D`, azul aço `#2F5496`, azul royal `#4472C4`, verde de conformidade `#E2EFDA` / `#A8D08D`).
- O acesso ao painel de diagnóstico é realizado através de navegadores web modernos com suporte a JavaScript habilitado para renderização de gráficos em canvas.
- A categorização industrial utiliza a taxonomia oficial do Modelo Purdue (ISA-95) para diferenciar ambientes operacionais com características distintas de tolerância a risco e latência.
