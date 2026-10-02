<!--
=== Sync Impact Report ===
- Version change: Initial template -> 1.0.0
- List of modified principles:
  * [PRINCIPLE_1_NAME] -> I. Modelo Evolutivo StH-AppSec e Rastreabilidade Normativa Tripla
  * [PRINCIPLE_2_NAME] -> II. Modelagem Matemática e Escala de Institucionalização (AL0 a AL4)
  * [PRINCIPLE_3_NAME] -> III. Identidade Visual Analítica e Representação Gráfica Padronizada
  * [PRINCIPLE_4_NAME] -> IV. Arquitetura Técnica Enxuta e Contrato de Stack Unificado
  * [PRINCIPLE_5_NAME] -> V. Integridade Canônica de Dados e Carga de Sementes (Seeds Obrigatórios)
- Added sections:
  * Restrições Técnicas e de Arquitetura (Section 2)
  * Fluxo de Governança de Dados e Validação de Conformidade (Section 3)
- Removed sections: None
- Follow-up TODOs: None (All placeholders resolved)
==========================
-->

# Zeppelin-AppSec Constitution

## Core Principles

### I. Modelo Evolutivo StH-AppSec e Rastreabilidade Normativa Tripla
O projeto Zeppelin-AppSec baseia-se integralmente no modelo evolutivo StH-AppSec (Stairway to Heaven for AppSec), estruturado em cinco estágios progressivos e contínuos de maturidade:
1. **Estágio A — AppSec Reativa / Tradicional (Reactive AppSec)**: Segurança tratada como auditoria pontual e reativa no final do ciclo de vida, sem integração ao backlog ágil (3 afirmações atômicas).
2. **Estágio B — AppSec Ágil (Agile AppSec)**: Integração orgânica no time ágil com Security Champions, Breakout Action Groups (BAGs), Security Stories e revisões de código na squad (10 afirmações atômicas).
3. **Estágio C — Integração Contínua Segura (Continuous Security Integration - CSI)**: Automação técnica no servidor de CI, executando verificações automáticas de SAST, SCA, Threat Modeling as Code e Quality Gates automáticos no build (8 afirmações atômicas).
4. **Estágio D — Implantação Contínua Segura (Continuous Security Deployment - CSD)**: Automação na esteira de CD, contemplando análise de Infraestrutura como Código (IaC), cofres de segredos centralizados (Vaults) e testes de segurança dinâmicos (DAST) em staging (9 afirmações atômicas).
5. **Estágio E — Operação Contínua Segura (Continuous Security Operations - CSO)**: Observabilidade em produção, centralização de logs em SIEM, WAF, escaneamentos agendados periódicos e resiliência operacional (10 afirmações atômicas).

O instrumento de avaliação DEVE conter exatamente 40 afirmações atômicas e unívocas, focadas em Experiência do Desenvolvedor (Developer Experience - DX), eliminando o "Dilema do Respondente" decorrente de perguntas compostas. O catálogo DEVE manter rastreabilidade normativa bidirecional completa com:
- As 6 dimensões do framework SMAF: Governança (6 afirmações), Arquitetura e Design (8 afirmações), Desenvol. e Revisão (5 afirmações), Construção e Impl. (6 afirmações), Testes e Verificação (7 afirmações), Operações e Obs. (8 afirmações).
- 100% das práticas do OWASP SAMM v2.0 (15 práticas distribuídas pelas funções de Governança, Design, Implementação, Verificação e Operações).
- Os 250 IDs de atividades (diretos e correlatos/absorvidos) do OWASP DSOMM v5.0.2.

### II. Modelagem Matemática e Escala de Institucionalização (AL0 a AL4)
A quantificação da maturidade em segurança DEVE adotar com rigor absoluto a Escala Oficial de Institucionalização do Zeppelin (Júnior et al., 2022), composta por cinco níveis ordenados com atribuição de pesos numéricos bem definidos:
- **AL0 — Não Adotada (0%; peso = 0,00)**: Prática nunca implementada ou inexistente na organização.
- **AL1 — Abandonada (10%; peso = 0,10)**: Prática testada no passado, mas descontinuada por complexidade ou excesso de falsos positivos (reconhece explicitamente a capacidade e o aprendizado adquirido).
- **AL2 — Projeto / Produto (30%; peso = 0,30)**: Execução pontual ou ad-hoc em um projeto ou produto específico por iniciativa individual.
- **AL3 — Processo Definido (60%; peso = 0,60)**: Prática padronizada e documentada corporativamente, porém de adoção facultativa pelos times.
- **AL4 — Institucionalizada (100%; peso = 1,00)**: Prática formalmente definida, automatizada quando aplicável e executada sistematicamente em todas as soluções.

O cálculo do Grau de Adoção (AD) DEVE ser estritamente determinístico, conforme formalizado na dissertação IFES 2026:
1. **Grau de Adoção de um agrupamento $k$ ($AD_k$)**: O Grau de Adoção de uma dimensão SMAF ou de um estágio evolutivo StH-AppSec é a média aritmética simples dos pesos das afirmações que compõem o agrupamento:
   $$AD_k = \frac{\sum_{i \in k} peso(AL_i)}{n_k} \times 100\%$$
   onde $n_k$ é o número total de afirmações do agrupamento $k$ e $peso(AL_i) \in \{0,00; 0,10; 0,30; 0,60; 1,00\}$.
2. **Grau de Adoção Global da Squad ($AD_{global}$)**: O Grau de Adoção global da squad é a média aritmética simples dos Graus de Adoção das seis dimensões do SMAF:
   $$AD_{global} = \frac{1}{6} \sum_{k \in SMAF} AD_k$$
3. Toda camada de agregação ou serviço DEVE validar que os resultados dos cálculos confiram com os benchmarks da simulação empírica industrial: Squad A (N2 OT) = 20,3%; Squad B (N3 MES) = 47,0%; Squad C (N4 ERP) = 88,7%; Média Geral = 52,0%.

### III. Identidade Visual Analítica e Representação Gráfica Padronizada
A interface do usuário e os relatórios diagnósticos DEVEM adotar a identidade visual e as representações gráficas exemplificadas em `docs/zeppelin_analytics_report_v1.xlsx` e `docs/simulacao_zeppelin_appsec_3_squads.xlsx`:
- **Paleta Cromática Corporativa**:
  - Azul Noturno Executivo (Navy): `#1B365D` (cabeçalhos de tabelas, cartões de destaque, títulos de nível 1).
  - Azul Aço Corporativo (Steel Blue): `#2F5496` (subtítulos, bordas estruturadas, eixos e séries primárias).
  - Azul Royal (Accent Blue): `#4472C4` (linhas dinâmicas, preenchimento de radar, botões principais de ação).
  - Azul Gelo Suave (Ice Blue): `#DCE6F1` e `#F9FBFD` (linhas alternadas de dados, fundos de cartões métricos).
  - Cinza Neutro de Estrutura: `#D6DCE4` e `#D9D9D9` (divisórias, bordas de formulários, grids de apoio).
  - Verde Sucesso / Institucionalizado: `#E2EFDA` e `#A8D08D` (totais consolidados, indicadores de prática AL4).
- **Representações Gráficas Obrigatórias (via Chart.js)**:
  1. **Gráfico Radar SMAF**: Mapeamento do Grau de Adoção ($AD$) nas seis dimensões do SMAF em escala radial de 0% a 100%, permitindo visualização de perfil de maturidade e sobreposição comparativa entre squads e benchmark organizacional.
  2. **Gráfico de Barras StH-AppSec**: Representação das práticas adotadas por estágio StH-AppSec (Estágios A ao E) e distribuição por níveis de adoção (AL0 a AL4), fornecendo visibilidade direta da progressão na trilha evolutiva.

### IV. Arquitetura Técnica Enxuta e Contrato de Stack Unificado
A solução de software DEVE aderir a uma arquitetura desacoplada, leve e de fácil execução local:
- **Backend**: Python 3.10+ com FastAPI para fornecimento de APIs RESTful estruturadas, assíncronas e documentadas automaticamente via OpenAPI/Swagger. A camada de persistência e validação de contratos DEVE utilizar SQLModel (unificando SQLAlchemy ORM e Pydantic v2).
- **Banco de Dados**: SQLite transacional armazenado localmente no arquivo `zeppelin.db`, garantindo portabilidade, persistência relacional e ausência de dependência de servidores de banco externos para desenvolvimento e execução.
- **Frontend**: HTML5 semântico estilizado com Tailwind CSS fornecido via CDN, priorizando responsividade, leveza, ausência de compiladores complexos de frontend e compatibilidade entre navegadores modernos.
- **Visualização de Dados**: Chart.js fornecido via CDN para renderização em `<canvas>` interativo dos gráficos de Radar SMAF e Barras StH.

### V. Integridade Canônica de Dados e Carga de Sementes (Seeds Obrigatórios)
O banco de dados relacional `zeppelin.db` DEVE contar com carga inicial obrigatória, automatizada e idempotente a partir dos arquivos canônicos do projeto:
- **Catálogo de Afirmações Atômicas**: Ingestão completa das 40 afirmações atômicas de `docs/zeppelin_appsec_40_afirmacoes.xlsx`, persistindo código unívoco (ex.: AO.01, AO.02, VER.01, GOV.01), declaração simplificada voltada a DX, estágio StH correspondente, dimensão SMAF, referências do OWASP SAMM v2.0 e identificadores diretos e correlatos do OWASP DSOMM v5.0.2.
- **Simulação Empírica Industrial**: Carga dos diagnósticos das três squads operacionais de `docs/simulacao_zeppelin_appsec_3_squads.xlsx`, respeitando a classificação do Modelo Purdue (ISA-95):
  - **Squad A (Nível 2 — OT / Controle de Processos)**: SCADA, IHMs, restrições rígidas de latência, sistemas legados ($AD_{global} = 20,3\%$).
  - **Squad B (Nível 3 — MES / Gestão de Operações de Manufatura)**: Rastreabilidade, controle de lotes, historiadores de dados, ponte OT-TI ($AD_{global} = 47,0\%$).
  - **Squad C (Nível 4 — ERP / TI Corporativa)**: Sistemas corporativos em nuvem, microsserviços, CI/CD ($AD_{global} = 88,7\%$).

## Restrições Técnicas e de Arquitetura

### Contratos de API e Validação
- Todas as rotas de backend DEVEM validar entradas e saídas utilizando esquemas SQLModel/Pydantic, impedindo a persistência ou retorno de dados fora da especificação da escala AL0–AL4.
- As respostas de cálculo de Grau de Adoção DEVEM retornar tanto o valor percentual formatado quanto o valor decimal bruto para auditoria.

### Persistência e Integridade de Dados
- O esquema de banco de dados SQLite DEVE implementar chaves primárias, chaves estrangeiras e índices adequados para afirmações, squads, avaliações e respostas individuais.
- O script de carga de sementes DEVE ser idempotente: execuções sucessivas não devem duplicar registros nem corromper dados existentes.

### Usabilidade e Experiência do Desenvolvedor (DX)
- A interface de diagnóstico DEVE garantir tempo de preenchimento inferior a 30 minutos por squad, em conformidade com o Requisito de Design R1 e Critério C1 da pesquisa DSR.
- Cada afirmação DEVE ser apresentada com texto conciso, livre de conjunções que criem avaliações duplas ou ambíguas.

### Adequação ao Modelo Purdue
- A classificação de squads no sistema DEVE exigir o enquadramento no nível de arquitetura de automação industrial (ISA-95), garantindo a capacidade discriminatória de maturidade (Requisito R3 e Critério C2).

## Fluxo de Governança de Dados e Validação de Conformidade

### Procedimento de Diagnóstico e Auditoria
1. Cada squad é avaliada por meio de uma única submissão completa cobrindo todas as 40 afirmações atômicas.
2. Cada resposta DEVE selecionar exclusivamente um nível da escala oficial: AL0 (0%), AL1 (10%), AL2 (30%), AL3 (60%) ou AL4 (100%).
3. Nenhuma afirmação pode ficar sem resposta; submissões parciais DEVEM ser rejeitadas pela camada de validação da API.

### Qualidade e Gates de Verificação
- O repositório DEVE incluir testes unitários e de integração automatizados (`pytest`) cobrindo:
  - Consistência do parser e integridade da carga dos dados de sementes (`docs/*.xlsx`).
  - Precisão exata das fórmulas matemáticas de cálculo de $AD_k$ e $AD_{global}$.
  - Respostas e validações dos endpoints da API FastAPI.
- Qualquer discrepância entre os valores calculados pelo sistema e os dados consolidados da simulação empírica industrial (Tabelas 4.1 e 4.2 da dissertação) DEVE ser considerada uma falha impeditiva de build.

## Governance

A Constituição do Zeppelin-AppSec é a autoridade máxima regulatória, metodológica e arquitetural do projeto.
- **Hierarquia Normativa**: As diretrizes, princípios e restrições aqui formalizados sobrepõem-se a quaisquer decisões informais, planos de implementação (`plan.md`), especificações de requisitos (`spec.md`) ou tarefas operacionais (`tasks.md`).
- **Procedimento de Emenda**: Qualquer alteração, adição ou revogação de princípios exige a elaboração de uma proposta de emenda formal, contendo justificativa técnica fundamentada, avaliação de impacto nos cálculos diagnósticos e plano de migração de dados.
- **Versionamento Semântico da Governança**:
  - **MAJOR**: Alterações que quebrem a retrocompatibilidade matemática, remoção de princípios fundamentais ou reestruturação da escala de institucionalização.
  - **MINOR**: Inclusão de novas dimensões, princípios complementares ou expansão material das diretrizes.
  - **PATCH**: Correções ortográficas, esclarecimentos terminológicos e refinamentos textuais sem alteração semântica ou normativa.
- **Verificação Contínua**: Toda revisão de código (Pull Request / Merge Request) DEVE verificar explicitamente a conformidade das mudanças com os princípios estabelecidos nesta Constituição.

**Version**: 1.0.0 | **Ratified**: 2026-09-23 | **Last Amended**: 2026-09-23
