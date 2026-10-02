# Contract: Squad Creation API (POST /api/squads)

## Overview
Permite o cadastro de uma nova Squad industrial no sistema Zeppelin-AppSec. Ao cadastrar a squad, o sistema inicializa automaticamente 40 respostas de avaliação vinculadas às 40 afirmações atômicas com nível AL0 (peso 0.0), disponibilizando a squad imediatamente para auditoria e inclusão nos benchmarks.

- **Método**: `POST`
- **Caminho**: `/api/squads`
- **Content-Type**: `application/json`

---

## Requisição

### Request Body (`SquadCreate`)

```json
{
  "name": "Squad Logística",
  "purdue_level": "Nível 3 - Sistemas de Execução de Manufatura (MES)",
  "purdue_short": "N3 MES",
  "description": "Responsável por rastreabilidade e roteamento de materiais na planta"
}
```

### Campos da Requisição

| Campo | Tipo | Obrigatório | Descrição / Restrições |
|---|---|---|---|
| `name` | `string` | Sim | Nome de exibição da Squad (2 a 100 caracteres). Não pode ser vazio. |
| `purdue_level` | `string` | Sim | Descrição do nível Purdue ISA-95 (3 a 100 caracteres). |
| `purdue_short` | `string` | Sim | Rótulo abreviado para badges e tabelas (2 a 50 caracteres). Ex: `N2 OT`, `N3 MES`. |
| `description` | `string` | Não | Contextualização do escopo da Squad (máx. 500 caracteres, padrão: `""`). |

---

## Resposta

### Sucesso (`201 Created`)

```json
{
  "id": 4,
  "code": "squad-logistica",
  "name": "Squad Logística",
  "purdue_level": "Nível 3 - Sistemas de Execução de Manufatura (MES)",
  "purdue_short": "N3 MES",
  "description": "Responsável por rastreabilidade e roteamento de materiais na planta",
  "created_at": "2026-09-23T23:55:00Z"
}
```

### Efeitos Colaterais no Banco de Dados
1. Inserção de 1 registro na tabela `squad` com código único em slug (`squad-logistica`).
2. Inserção em lote de 40 registros na tabela `assessment_answer` vinculando `squad_id = 4` a cada uma das 40 afirmações com `adoption_level = 0` e `adoption_weight = 0.0`.
3. Notificação e disponibilidade imediata na rota `GET /api/squads`, `GET /api/diagnostics/squad-logistica` e `GET /api/benchmark`.

---

## Erros e Validações

### `422 Unprocessable Entity` (Validação de Entrada)
Disparado se campos obrigatórios estiverem ausentes, forem nulos ou violarem tamanhos mínimos/máximos.

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "String should have at least 2 characters",
      "type": "string_too_short"
    }
  ]
}
```

### `409 Conflict` (Squad ou Código Duplicado)
Disparado se já existir uma squad cadastrada com o mesmo `code` gerado ou mesmo nome.

```json
{
  "detail": "Já existe uma squad cadastrada com o código 'squad-logistica'."
}
```

