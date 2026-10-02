# API Contract: Diagnostics Endpoint

**Endpoint**: `GET /api/diagnostics/{squad_id_or_code}`  
**Description**: Retorna o diagnóstico consolidado de uma squad específica, contendo o Grau de Adoção Global ($AD_{global}$), as pontuações nas 6 dimensões SMAF, as pontuações nos 5 estágios StH-AppSec, a distribuição de institucionalização por nível (AL0 a AL4) e o detalhamento item a item das 40 afirmações.

## Path Parameters

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `squad_id_or_code` | string/integer | ID numérico (ex.: `1`) ou código da squad (ex.: `squad-a`). |

## Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

### Payload Schema

```json
{
  "squad": {
    "id": 1,
    "code": "squad-a",
    "name": "Squad A",
    "purdue_level": "Nível 2 — OT / Controle de Processos",
    "purdue_short": "N2 OT",
    "description": "Responsável por softwares de supervisão de campo (SCADA, IHMs) e controle em tempo real."
  },
  "global_adoption_degree": 20.3,
  "global_adoption_degree_formatted": "20.3%",
  "predominant_stage": "Estágio A (Reactive)",
  "al_distribution": {
    "AL0": 18,
    "AL1": 2,
    "AL2": 8,
    "AL3": 10,
    "AL4": 2
  },
  "dimension_scores": [
    {
      "dimension": "Governança",
      "total_items": 6,
      "weight_sum": 2.2,
      "adoption_degree": 36.7,
      "adoption_degree_formatted": "36.7%"
    },
    {
      "dimension": "Arquitetura e Design",
      "total_items": 8,
      "weight_sum": 0.8,
      "adoption_degree": 10.0,
      "adoption_degree_formatted": "10.0%"
    },
    {
      "dimension": "Desenvol. e Revisão",
      "total_items": 5,
      "weight_sum": 1.2,
      "adoption_degree": 24.0,
      "adoption_degree_formatted": "24.0%"
    },
    {
      "dimension": "Construção e Impl.",
      "total_items": 6,
      "weight_sum": 0.8,
      "adoption_degree": 13.3,
      "adoption_degree_formatted": "13.3%"
    },
    {
      "dimension": "Testes e Verificação",
      "total_items": 7,
      "weight_sum": 1.0,
      "adoption_degree": 14.3,
      "adoption_degree_formatted": "14.3%"
    },
    {
      "dimension": "Operações e Obs.",
      "total_items": 8,
      "weight_sum": 1.9,
      "adoption_degree": 23.8,
      "adoption_degree_formatted": "23.8%"
    }
  ],
  "stage_scores": [
    {
      "stage": "Estágio A (Reactive)",
      "stage_code": "A",
      "total_items": 3,
      "weight_sum": 1.8,
      "adoption_degree": 60.0,
      "adoption_degree_formatted": "60.0%",
      "al_counts": { "AL0": 0, "AL1": 0, "AL2": 0, "AL3": 3, "AL4": 0 }
    },
    {
      "stage": "Estágio B (Agile)",
      "stage_code": "B",
      "total_items": 10,
      "weight_sum": 2.6,
      "adoption_degree": 26.0,
      "adoption_degree_formatted": "26.0%",
      "al_counts": { "AL0": 3, "AL1": 0, "AL2": 3, "AL3": 4, "AL4": 0 }
    },
    {
      "stage": "Estágio C (CSI)",
      "stage_code": "C",
      "total_items": 8,
      "weight_sum": 0.8,
      "adoption_degree": 10.0,
      "adoption_degree_formatted": "10.0%",
      "al_counts": { "AL0": 5, "AL1": 1, "AL2": 1, "AL3": 1, "AL4": 0 }
    },
    {
      "stage": "Estágio D (CSD)",
      "stage_code": "D",
      "total_items": 9,
      "weight_sum": 0.4,
      "adoption_degree": 4.4,
      "adoption_degree_formatted": "4.4%",
      "al_counts": { "AL0": 7, "AL1": 1, "AL2": 1, "AL3": 0, "AL4": 0 }
    },
    {
      "stage": "Estágio E (CSO)",
      "stage_code": "E",
      "total_items": 10,
      "weight_sum": 2.3,
      "adoption_degree": 23.0,
      "adoption_degree_formatted": "23.0%",
      "al_counts": { "AL0": 3, "AL1": 0, "AL2": 3, "AL3": 2, "AL4": 2 }
    }
  ],
  "statements": [
    {
      "statement_code": "AO.01",
      "description": "Regras técnicas e objetivos de segurança documentados e divulgados para todas as squads.",
      "smaf_dimension": "Governança",
      "sth_stage": "Estágio A (Reactive)",
      "adoption_level_code": "AL3",
      "adoption_level_num": 3,
      "adoption_level_name": "Processo Definido",
      "adoption_weight": 0.6,
      "adoption_degree_pct": "60%",
      "samm_ref": "Strategy & Metrics (SM-1A, SM-2A), Policy & Compliance (PC-1A, PC-2A)",
      "dsomm_ref": "Culture and Organization -> Design (ID: 071) [Correlatos: IDs 008, 062, 133]"
    }
  ]
}
```

