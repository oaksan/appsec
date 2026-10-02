# Quickstart: Gestão de Squads, Edição de Auditoria e Benchmark StH-AppSec

**Feature**: `002-squad-audit-management`
**Status**: Ready for Validation
**Date**: 2026-09-23

---

## 1. Pré-Requisitos

- **Python**: Versão 3.10 ou superior (ambiente atual: Python 3.13).
- **Ambiente Virtual**: `.venv` configurado na raiz do projeto.
- **Banco de Dados**: SQLite `zeppelin.db` ativo.

---

## 2. Inicialização do Servidor

Certifique-se de que a aplicação está em execução:

```bash
# Ativação do ambiente e execução local
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 3. Cenários de Validação Rápida

### Cenário 1: Adicionar Nova Squad

#### Via Linha de Comando (cURL):
```bash
curl -X POST http://localhost:8000/api/squads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Squad Logística",
    "purdue_level": "Nível 3 - Sistemas de Execução de Manufatura (MES)",
    "purdue_short": "N3 MES",
    "description": "Responsável por automação logística e controle de esteiras"
  }'
```

**Resultado Esperado**:
- Status HTTP `201 Created`.
- Retorno JSON com `id`, `code: "squad-logistica"`.
- O banco SQLite registra 40 entradas de avaliação para a nova squad, todas com `adoption_level = 0`.

#### Via Interface Gráfica:
1. Abra `http://localhost:8000/`.
2. Clique no botão **"+ Nova Squad"** alinhado ao seletor de squads.
3. Preencha o modal com Nome, Nível Purdue e Descrição, e clique em "Salvar".
4. Verifique se o seletor de Squad agora exibe a nova squad e a seleciona imediatamente com Grau de Adoção de `0,0%`.

---

### Cenário 2: Editar e Persistir Auditoria de uma Squad

#### Via Interface Gráfica:
1. Com a squad desejada selecionada (ex: `Squad A` ou a nova squad), clique no botão **"Editar Auditoria"** na seção do catálogo de afirmações.
2. Observe que as badges estáticas de nível (AL0 a AL4) tornam-se `<select>` interativos.
3. Modifique os níveis de algumas afirmações (ex: de AL0 para AL3 ou AL4).
4. Clique em **"Salvar Alterações"**.
5. Observe:
   - A confirmação visual de sucesso (toast / badge verde).
   - A atualização imediata dos cards superiores (Grau de Adoção Global, Estágio Predominante).
   - O redesenho em tempo real dos gráficos Radar SMAF e Barras StH.
   - Recarregue a página (`F5`) e confirme que as alterações persistiram no banco `zeppelin.db`.

#### Via Linha de Comando (cURL):
```bash
curl -X PUT http://localhost:8000/api/diagnostics/squad-a \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"statement_code": "AO.01", "adoption_level": 4},
      {"statement_code": "ARQ.01", "adoption_level": 4}
    ]
  }'
```

**Resultado Esperado**:
- Status HTTP `200 OK`.
- Diagnóstico retornado com novos scores recalculados para `squad-a`.

---

### Cenário 3: Validação das Duas Matrizes de Benchmarking (SMAF e StH-AppSec)

1. Na interface web, role até a seção **"Benchmarking Organizacional"**.
2. Verifique a existência de **duas tabelas distintas**:
   - **Tabela 1 - Dimensões SMAF**: Exibe as 6 dimensões com colunas para cada squad cadastrada e a Média Geral.
   - **Tabela 2 - Estágios StH-AppSec (Tabela 4.2)**: Exibe os 5 estágios (Reactive a CSO) com colunas para cada squad e a Média Geral.
3. Verifique a linha de rodapé da Tabela 2:
   - Rotulada como **`GRAU DE ADOÇÃO GLOBAL (AD%)`** e formatada identicamente à Tabela 1.
   - Exibe o grau global de cada equipe (Squad A: 20,3%, Squad B: 47,0%, Squad C: 88,7%) e a média geral organizacional (52,0%).
4. Verifique os valores de referência da dissertação para as squads canônicas na Tabela 4.2:
   - **Reactive (Estágio A)**: Squad A (60,0%), Squad B (60,0%), Squad C (86,7%), Média (68,9%).
   - **Agile (Estágio B)**: Squad A (26,0%), Squad B (54,0%), Squad C (92,0%), Média (57,3%).
   - **CSI (Estágio C)**: Squad A (10,0%), Squad B (50,0%), Squad C (85,0%), Média (48,3%).
   - **CSD (Estágio D)**: Squad A (4,4%), Squad B (31,1%), Squad C (86,7%), Média (40,7%).
   - **CSO (Estágio E)**: Squad A (23,0%), Squad B (44,0%), Squad C (88,0%), Média (51,7%).

---

### Cenário 4: Filtros Combinados de Dimensão SMAF e Estágio StH no Catálogo Zeppelin-AppSec

1. Na seção **"Catálogo e Auditoria Zeppelin-AppSec"**, observe a existência de dois conjuntos de filtros:
   - Linha 1: Filtro com rótulo **`Dimensão SMAF:`** (Todas, Governança, Arquitetura e Design, Desenvol. e Revisão, Construção e Impl., Testes e Verificação, Operações e Obs.).
   - Linha 2: Filtro por **Estágio StH** com nomenclatura evolutiva: `Todos (40)`, `Reactive (3)`, `Agile (10)`, `CSI - Continuous Security Integration (8)`, `CSD - Continuous Security Deployment (9)` e `CSO - Continuous Security Operation (10)`.
2. Clique no filtro **"Reactive (3)"**:
   - A tabela deve exibir exatamente as 3 afirmações correspondentes ao Estágio A (Reactive).
3. Selecione concomitantemente uma dimensão SMAF (ex: "Governança"):
   - A tabela deve cruzar os filtros e exibir somente as afirmações de Governança no Estágio Reactive.
4. Digite um termo no campo de busca (ex: "pipeline" ou "treinamento") para validar a filtragem unificada.

---

### Cenário 5: Exclusão de Squad com Limpeza em Cascata

#### Via Interface Gráfica:
1. Selecione a squad a ser removida no seletor de squads (ex.: `Squad Logística`).
2. Clique no botão **"Excluir Squad"** presente no cabeçalho da squad.
3. No diálogo de confirmação, leia a mensagem de alerta sobre remoção definitiva e clique em **"Confirmar Exclusão"**.
4. Observe que:
   - A squad é excluída e removida da lista do `<select>`.
   - Outra squad é selecionada automaticamente (ex.: `Squad A`).
   - O painel diagnóstico, cartões e gráficos são recarregados para a squad ativa.
   - Na seção de benchmarking, as matrizes (SMAF e StH) são atualizadas sem a coluna da squad excluída.

#### Via Linha de Comando (cURL):
```bash
curl -X DELETE http://localhost:8000/api/squads/squad-logistica
```

**Resultado Esperado**:
- Status HTTP `200 OK`.
- Retorno JSON: `{"message": "Squad 'Squad Logística' e suas 40 respostas associadas foram excluídas com sucesso.", "deleted_code": "squad-logistica"}`.

---

### Cenário 6: Execução da Suíte de Testes Automatizados

```bash
pytest tests/ -v
```

**Critérios de Aceite**:
- Todos os testes de unidade, integração e regressão devem passar sem falhas (`100% pass`).
- Validação de criação de squad com 40 respostas geradas automaticamente.
- Validação de exclusão de squad com remoção em cascata e recálculo dinâmico.
- Validação de atualização de respostas com limites AL0–AL4.
- Validação de cálculo das matrizes dinâmicas de benchmark por dimensão e por estágio.

