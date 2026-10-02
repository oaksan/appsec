# API Contract: Benchmark Endpoint

**Endpoint**: `GET /api/benchmark`  
**Description**: Retorna o comparativo consolidado de maturidade entre as três squads industriais avaliadas (Níveis 2, 3 e 4 do Modelo Purdue) e a Média Geral da Organização para todas as dimensões SMAF e estágios StH-AppSec.

## Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

### Payload Schema

```json
{
  "dimensions": [
    {
      "dimension": "Governança",
      "squad_a_pct": 36.7,
      "squad_b_pct": 55.0,
      "squad_c_pct": 93.3,
      "average_pct": 61.7
    },
    {
      "dimension": "Arquitetura e Design",
      "squad_a_pct": 10.0,
      "squad_b_pct": 37.5,
      "squad_c_pct": 80.0,
      "average_pct": 42.5
    },
    {
      "dimension": "Desenvol. e Revisão",
      "squad_a_pct": 24.0,
      "squad_b_pct": 54.0,
      "squad_c_pct": 92.0,
      "average_pct": 56.7
    },
    {
      "dimension": "Construção e Impl.",
      "squad_a_pct": 13.3,
      "squad_b_pct": 51.7,
      "squad_c_pct": 100.0,
      "average_pct": 55.0
    },
    {
      "dimension": "Testes e Verificação",
      "squad_a_pct": 14.3,
      "squad_b_pct": 40.0,
      "squad_c_pct": 77.1,
      "average_pct": 43.8
    },
    {
      "dimension": "Operações e Obs.",
      "squad_a_pct": 23.8,
      "squad_b_pct": 43.8,
      "squad_c_pct": 90.0,
      "average_pct": 52.5
    }
  ],
  "stages": [
    {
      "stage": "Estágio A (Reactive)",
      "squad_a_pct": 60.0,
      "squad_b_pct": 60.0,
      "squad_c_pct": 86.7
    },
    {
      "stage": "Estágio B (Agile)",
      "squad_a_pct": 26.0,
      "squad_b_pct": 54.0,
      "squad_c_pct": 92.0
    },
    {
      "stage": "Estágio C (CSI)",
      "squad_a_pct": 10.0,
      "squad_b_pct": 50.0,
      "squad_c_pct": 85.0
    },
    {
      "stage": "Estágio D (CSD)",
      "squad_a_pct": 4.4,
      "squad_b_pct": 31.1,
      "squad_c_pct": 86.7
    },
    {
      "stage": "Estágio E (CSO)",
      "squad_a_pct": 23.0,
      "squad_b_pct": 44.0,
      "squad_c_pct": 88.0
    }
  ],
  "global_summary": {
    "squad_a_pct": 20.3,
    "squad_b_pct": 47.0,
    "squad_c_pct": 88.7,
    "organization_average_pct": 52.0
  }
}
```

