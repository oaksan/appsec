# Quickstart: Painel Diagnóstico e Analítico Zeppelin-AppSec

**Feature**: `001-diagnostic-dashboard`
**Status**: Ready for Validation
**Date**: 2026-09-23

---

## 1. Pré-Requisitos

- **Python**: Versão 3.10 ou superior (ambiente atual: Python 3.13).
- **Ambiente Virtual**: Recomendado `venv`.
- **Arquivos Canônicos**: Presença obrigatória dos arquivos de seed em `docs/`:
  - `docs/zeppelin_appsec_40_afirmacoes.xlsx`
  - `docs/simulacao_zeppelin_appsec_3_squads.xlsx`
  - `docs/zeppelin_analytics_report_v1.xlsx`

---

## 2. Instalação e Preparação do Ambiente

No diretório raiz do projeto:

```bash
# 1. Criar e ativar o ambiente virtual (opcional, porém recomendado)
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar as dependências do projeto
pip install fastapi uvicorn sqlmodel pandas openpyxl jinja2 pytest httpx
# ou via requirements.txt:
pip install -r requirements.txt
```

---

## 3. Execução da Aplicação

Inicie o servidor de desenvolvimento FastAPI com Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> **Nota**: No primeiro startup da aplicação, a rotina `lifespan` invocará `init_db()` e `seed_database()`. O banco `zeppelin.db` será criado automaticamente e populado com as 40 afirmações atômicas e com os dados das 3 squads.

---

## 4. Cenários de Validação Rápida

### Cenário 1: Execução dos Testes Automatizados de Rigor Matemático

Execute a suíte de testes unitários para validar a precisão das fórmulas e a integridade da carga:

```bash
pytest -v
```

**Resultado Esperado**:
- Todos os testes passam (`PASSED`).
- `test_math.py`: validação de $AD_k$ e $AD_{global}$ para Squad A ($20{,}3\%$), Squad B ($47{,}0\%$), Squad C ($88{,}7\%$) e Média Geral ($52{,}0\%$).
- `test_seed.py`: validação da presença de 40 afirmações e 3 squads no banco SQLite.
- `test_api.py`: validação dos contratos HTTP das rotas `/api/*`.

### Cenário 2: Validação dos Endpoints da API REST

```bash
# 1. Verificar contagem de afirmações atômicas (deve retornar 40 itens)
curl -s http://localhost:8000/api/statements | jq length

# 2. Verificar lista de squads industriais (deve retornar 3 squads)
curl -s http://localhost:8000/api/squads | jq '.[].name'

# 3. Conferir Grau de Adoção Global da Squad A (Nível 2 OT) -> 20.3%
curl -s http://localhost:8000/api/diagnostics/squad-a | jq '{squad: .squad.name, ad_global: .global_adoption_degree_formatted}'

# 4. Conferir Grau de Adoção Global da Squad B (Nível 3 MES) -> 47.0%
curl -s http://localhost:8000/api/diagnostics/squad-b | jq '{squad: .squad.name, ad_global: .global_adoption_degree_formatted}'

# 5. Conferir Grau de Adoção Global da Squad C (Nível 4 ERP) -> 88.7%
curl -s http://localhost:8000/api/diagnostics/squad-c | jq '{squad: .squad.name, ad_global: .global_adoption_degree_formatted}'

# 6. Conferir Benchmark Organizacional -> Média Geral 52.0%
curl -s http://localhost:8000/api/benchmark | jq .global_summary
```

### Cenário 3: Validação da Interface Web e Gráficos

1. Abra o navegador em `http://localhost:8000/`.
2. Verifique se o cabeçalho apresenta a identidade visual Zeppelin (Azul Noturno `#1B365D`).
3. Alterne entre as opções do seletor de squad:
   - Ao selecionar **Squad A**, o card principal exibe `20,3%`, o Gráfico Radar plota a área concentrada no centro, e o Gráfico de Barras ilustra concentração em AL0 a AL2.
   - Ao selecionar **Squad B**, o card atualiza para `47,0%`, com expansão das dimensões de Governança e Desenvolvimento.
   - Ao selecionar **Squad C**, o card atualiza para `88,7%`, com o gráfico Radar preenchendo a quase totalidade do polígono e predominância de AL4 no gráfico de barras.
4. Teste os filtros da tabela de 40 afirmações por dimensão SMAF (ex.: filtrar por "Governança" exibe 6 itens; por "Arquitetura e Design" exibe 8 itens).

