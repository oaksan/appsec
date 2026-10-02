# API Contract: Statements Endpoint

**Endpoint**: `GET /api/statements`  
**Description**: Retorna o catálogo completo das 40 afirmações atômicas de segurança contínua com filtros opcionais por dimensão SMAF e estágio evolutivo StH-AppSec.

## Query Parameters

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `dimension` | string | Não | Filtra por dimensão SMAF (ex.: `Governança`, `Arquitetura e Design`). |
| `stage` | string | Não | Filtra pelo código do estágio StH (`A`, `B`, `C`, `D` ou `E`). |

## Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

### Payload Schema

```json
[
  {
    "id": 1,
    "code": "AO.01",
    "description": "Regras técnicas e objetivos de segurança documentados e divulgados para todas as squads.",
    "sth_stage": "Estágio A (Reactive)",
    "sth_stage_code": "A",
    "smaf_dimension": "Governança",
    "samm_ref": "Strategy & Metrics (SM-1A, SM-2A), Policy & Compliance (PC-1A, PC-2A)",
    "dsomm_ref": "Culture and Organization -> Design (ID: 071) [Correlatos: IDs 008, 062, 133]"
  },
  {
    "id": 2,
    "code": "AO.02",
    "description": "Mapeamos a criticidade e o perfil de risco de cada aplicação (sensibilidade dos dados e exposição) para calibrar os requisitos de segurança.",
    "sth_stage": "Estágio A (Reactive)",
    "sth_stage_code": "A",
    "smaf_dimension": "Governança",
    "samm_ref": "Threat Assessment (TA-1A, TA-2A)",
    "dsomm_ref": "N/A (Atividade nativa do OWASP SAMM) [Correlatos: IDs 095, 159]"
  }
]
```

