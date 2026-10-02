# Contract: Audit Update API (PUT /api/diagnostics/{squad_id_or_code})

## Overview
Permite a atualização dos níveis de maturidade (AL0 a AL4) assinalados para uma Squad específica. Os novos valores são persistidos no banco de dados SQLite (`assessment_answer`) e o endpoint retorna imediatamente o diagnóstico recalculado da squad, incluindo os graus de adoção por dimensão SMAF ($AD_k$), por estágio StH-AppSec, média global ($AD_{global}$) e estágio predominante.

- **Método**: `PUT`
- **Caminho**: `/api/diagnostics/{squad_id_or_code}`
- **Content-Type**: `application/json`

---

## Parâmetros de Rota

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `squad_id_or_code` | `string` | Identificador numérico da squad (ex: `1`) ou seu código slug canônico (ex: `squad-a`). |

---

## Requisição

### Request Body (`AuditUpdateRequest`)

```json
{
  "answers": [
    {
      "statement_code": "AO.01",
      "adoption_level": 3
    },
    {
      "statement_code": "ARQ.01",
      "adoption_level": 4
    }
  ]
}
```

### Regras do Request Body

1. `answers`: Lista com 1 a 40 objetos `AnswerUpdateItem`.
2. `statement_code`: String que deve corresponder exatamente a um dos códigos de afirmações do catálogo (ex: `AO.01`, `AO.02`, ..., `GOV.08`).
3. `adoption_level`: Inteiro restrito a `[0, 1, 2, 3, 4]`.
4. Os pesos matemáticos correspondentes são definidos deterministicamente pelo backend:
   - AL0 $\rightarrow$ 0.0
   - AL1 $\rightarrow$ 0.1
   - AL2 $\rightarrow$ 0.3
   - AL3 $\rightarrow$ 0.6
   - AL4 $\rightarrow$ 1.0

---

## Resposta

### Sucesso (`200 OK`)
Retorna a entidade consolidada `SquadDiagnosticSummary` com todos os dados recalculados com precisão matemática.

```json
{
  "squad": {
    "id": 1,
    "code": "squad-a",
    "name": "Squad A",
    "purdue_level": "Nível 2 - Controle e Supervisão (SCADA/HMI)",
    "purdue_short": "N2 OT",
    "description": "Responsável por automação e controle operacional"
  },
  "global_score": 25.5,
  "predominant_stage": "Estágio B - Automação Integrada",
  "predominant_stage_code": "B",
  "radar_smaF": {
    "labels": [
      "Arquitetura e Design Seguro (ARQ)",
      "Automação e Operações DevSecOps (AO)",
      "Cultura, Governança e Métricas (GOV)",
      "Defesa e Resiliência Operacional (DEF)",
      "Gestão de Vulnerabilidades (GV)",
      "Segurança de Software na Entrega (SSE)"
    ],
    "scores": [33.3, 45.0, 15.0, 20.0, 20.0, 20.0]
  },
  "stages_adoption": [
    {
      "stage_code": "A",
      "stage_name": "Fundação e Conscientização",
      "adoption_pct": 60.0,
      "total_statements": 5
    },
    {
      "stage_code": "B",
      "stage_name": "Automação Integrada",
      "adoption_pct": 35.0,
      "total_statements": 10
    },
    {
      "stage_code": "C",
      "stage_name": "Segurança como Código",
      "adoption_pct": 18.0,
      "total_statements": 10
    },
    {
      "stage_code": "D",
      "stage_name": "Resiliência Avançada",
      "adoption_pct": 10.0,
      "total_statements": 8
    },
    {
      "stage_code": "E",
      "stage_name": "Excelência e Adaptação Contínua",
      "adoption_pct": 5.0,
      "total_statements": 7
    }
  ],
  "answers": [
    {
      "statement_code": "AO.01",
      "dimension_code": "AO",
      "stage_code": "B",
      "stage_name": "Automação Integrada",
      "statement_text": "Pipelines de CI/CD possuem validações estáticas de segurança ativadas.",
      "adoption_level": 3,
      "adoption_level_label": "AL3 - Adoção Generalizada",
      "adoption_weight": 0.6,
      "samm_coverage": "V&V / Static Analysis",
      "dsomm_coverage": "Static Application Security Testing (SAST)"
    }
  ]
}
```

---

## Erros e Validações

### `404 Not Found` (Squad Inexistente)
```json
{
  "detail": "Squad 'squad-inexistente' não encontrada."
}
```

### `422 Unprocessable Entity` (Nível Inválido ou Afirmação Inexistente)
Disparado se `adoption_level` for fora de 0-4 ou se `statement_code` for inválido.

```json
{
  "detail": "Código de afirmação 'XYZ.99' não reconhecido no catálogo."
}
```
ou Pydantic validation:
```json
{
  "detail": [
    {
      "loc": ["body", "answers", 0, "adoption_level"],
      "msg": "Input should be less than or equal to 4",
      "type": "less_than_equal"
    }
  ]
}
```

