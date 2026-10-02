# Contract: Squad Deletion API (DELETE /api/squads/{squad_id_or_code})

## Overview
Remove uma squad do sistema e executa limpeza transacional em cascata de todos os seus 40 registros de avaliação (`assessment_answer`) no banco de dados local SQLite `zeppelin.db`.

- **Método**: `DELETE`
- **Caminho**: `/api/squads/{squad_id_or_code}`
- **Content-Type**: `application/json`

---

## Parâmetros de Rota (Path Parameters)

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|:---:|---|
| `squad_id_or_code` | `string` ou `integer` | Sim | Identificador numérico (`id`) ou slug textual (`code`, ex.: `squad-logistica`) da equipe |

---

## Regras de Negócio e Validação

1. **Localização Flexível**: O endpoint aceita tanto o ID numérico quanto o código da squad.
2. **Proteção de Integridade**: Se restar apenas uma squad cadastrada no sistema, a requisição é rejeitada com `HTTP 400 Bad Request`, impedindo que o painel fique em estado inconsistente sem nenhuma squad disponível.
3. **Exclusão em Cascata Atômica**:
   - `DELETE FROM assessment_answer WHERE squad_id = :id;`
   - `DELETE FROM squad WHERE id = :id;`
   - Processado em uma única transação atômica (`session.commit()`).
4. **Impacto no Benchmarking**: Após a exclusão, consultas subsequentes a `GET /api/benchmark` deixam imediatamente de exibir a coluna da squad excluída e recomputam a média organizacional com base no novo total de equipes ($N - 1$).

---

## Respostas

### 1. Sucesso (`200 OK`)

```json
{
  "message": "Squad 'Squad Logística' e suas 40 respostas associadas foram excluídas com sucesso.",
  "deleted_code": "squad-logistica",
  "deleted_id": 4
}
```

### 2. Squad Não Encontrada (`404 Not Found`)

```json
{
  "detail": "Squad com identificador 'squad-inexistente' não encontrada."
}
```

### 3. Rejeição por Squad Única (`400 Bad Request`)

```json
{
  "detail": "Não é permitido excluir a única squad restante no sistema."
}
```

