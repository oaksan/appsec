# Contract: Benchmark API (GET /api/benchmark)

## Overview
Retorna a matriz de benchmarking organizacional consolidada para todas as squads cadastradas. Inclui duas tabelas completas de maturidade:
1. **Matriz de Adoção por Dimensão SMAF**: Adoção percentual ($AD_k$) nas 6 dimensões SMAF.
2. **Matriz de Adoção por Estágio StH-AppSec**: Adoção percentual ($AD_{estágio}$) nos 5 estágios (Estágios A ao E), correspondente à Tabela 4.2 da dissertação `docs/SDL.pdf`.

O endpoint é dinâmico, suportando de 1 a N squads, e preserva retrocompatibilidade com campos fixos para clientes legados.

- **Método**: `GET`
- **Caminho**: `/api/benchmark`
- **Content-Type**: `application/json`

---

## Requisição

Não requer parâmetros obrigatórios.

---

## Resposta

### Sucesso (`200 OK`)

```json
{
  "squads": [
    {
      "id": 1,
      "code": "squad-a",
      "name": "Squad A",
      "purdue_short": "N2 OT"
    },
    {
      "id": 2,
      "code": "squad-b",
      "name": "Squad B",
      "purdue_short": "N3 MES"
    },
    {
      "id": 3,
      "code": "squad-c",
      "name": "Squad C",
      "purdue_short": "N4 IT/Cloud"
    },
    {
      "id": 4,
      "code": "squad-logistica",
      "name": "Squad Logística",
      "purdue_short": "N3 MES"
    }
  ],
  "dimensions": [
    {
      "dimension": "Arquitetura e Design Seguro (ARQ)",
      "scores": {
        "squad-a": 36.7,
        "squad-b": 55.0,
        "squad-c": 91.7,
        "squad-logistica": 0.0
      },
      "squad_a_pct": 36.7,
      "squad_b_pct": 55.0,
      "squad_c_pct": 91.7,
      "average_pct": 45.9
    }
  ],
  "stages": [
    {
      "stage": "Estágio A - Fundação e Conscientização",
      "stage_code": "A",
      "scores": {
        "squad-a": 60.0,
        "squad-b": 60.0,
        "squad-c": 100.0,
        "squad-logistica": 0.0
      },
      "squad_a_pct": 60.0,
      "squad_b_pct": 60.0,
      "squad_c_pct": 100.0,
      "average_pct": 55.0
    },
    {
      "stage": "Estágio B - Automação Integrada",
      "stage_code": "B",
      "scores": {
        "squad-a": 35.0,
        "squad-b": 62.0,
        "squad-c": 95.0,
        "squad-logistica": 0.0
      },
      "squad_a_pct": 35.0,
      "squad_b_pct": 62.0,
      "squad_c_pct": 95.0,
      "average_pct": 48.0
    },
    {
      "stage": "Estágio C - Segurança como Código",
      "stage_code": "C",
      "scores": {
        "squad-a": 18.0,
        "squad-b": 45.0,
        "squad-c": 90.0,
        "squad-logistica": 0.0
      },
      "squad_a_pct": 18.0,
      "squad_b_pct": 45.0,
      "squad_c_pct": 90.0,
      "average_pct": 38.3
    },
    {
      "stage": "Estágio D - Resiliência Avançada",
      "stage_code": "D",
      "scores": {
        "squad-a": 10.0,
        "squad-b": 38.8,
        "squad-c": 82.5,
        "squad-logistica": 0.0
      },
      "squad_a_pct": 10.0,
      "squad_b_pct": 38.8,
      "squad_c_pct": 82.5,
      "average_pct": 32.8
    },
    {
      "stage": "Estágio E - Excelência e Adaptação Contínua",
      "stage_code": "E",
      "scores": {
        "squad-a": 5.7,
        "squad-b": 32.9,
        "squad-c": 75.7,
        "squad-logistica": 0.0
      },
      "squad_a_pct": 5.7,
      "squad_b_pct": 32.9,
      "squad_c_pct": 75.7,
      "average_pct": 28.6
    }
  ],
  "global_summary": {
    "squad-a": 20.3,
    "squad-b": 47.0,
    "squad-c": 88.7,
    "squad-logistica": 0.0,
    "organization_average_pct": 39.0
  }
}
```

---

## Formatação e Regras de Apresentação

1. **Colunas Dinâmicas**: Cada item em `squads` determina uma coluna na tabela do frontend.
2. **Compatibilidade**: Os campos `squad_a_pct`, `squad_b_pct`, `squad_c_pct` continuam presentes na resposta para squads A, B e C, garantindo que qualquer consumidor que dependa dessas propriedades não seja quebrado.
3. **Média Geral (`average_pct`)**: Corresponde à média aritmética dos percentuais das $N$ squads presentes no cálculo:
   $$\text{Média do Agrupamento} = \frac{1}{N} \sum_{s \in \text{Squads}} AD_{s, k}$$

