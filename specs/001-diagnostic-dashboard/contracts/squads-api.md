# API Contract: Squads Endpoint

**Endpoint**: `GET /api/squads`  
**Description**: Retorna a lista das squads operacionais cadastradas, classificadas segundo os níveis do Modelo Purdue (ISA-95).

## Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

### Payload Schema

```json
[
  {
    "id": 1,
    "code": "squad-a",
    "name": "Squad A",
    "purdue_level": "Nível 2 — OT / Controle de Processos",
    "purdue_short": "N2 OT",
    "description": "Responsável por softwares de supervisão de campo (SCADA, IHMs) e controle em tempo real."
  },
  {
    "id": 2,
    "code": "squad-b",
    "name": "Squad B",
    "purdue_level": "Nível 3 — MES / Gestão de Operações de Manufatura",
    "purdue_short": "N3 MES",
    "description": "Sistemas de rastreabilidade de produção, controle de lotes e historiadores de dados, atuando na ponte entre OT e TI corporativa."
  },
  {
    "id": 3,
    "code": "squad-c",
    "name": "Squad C",
    "purdue_level": "Nível 4 — ERP / TI Corporativa",
    "purdue_short": "N4 ERP",
    "description": "Gestão de sistemas de logística, portais corporativos e soluções em nuvem operando sob microsserviços e integração contínua."
  }
]
```

