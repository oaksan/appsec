from fastapi.testclient import TestClient

def test_get_dashboard_html(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "Zeppelin-AppSec" in response.text
    assert "radarChart" in response.text
    assert "barChart" in response.text

    # Verifica ausência do botão duplicado e presença do botão único de Nova Squad
    assert 'id="btn-open-squad-modal"' not in response.text
    assert 'id="btn-open-squad-modal-btn"' in response.text

    # Verifica novos rótulos de filtros e tabelas
    assert "Dimensão SMAF:" in response.text
    assert "Catálogo e Auditoria Zeppelin-AppSec" in response.text
    assert "Reactive (3)" in response.text
    assert "Agile (10)" in response.text
    assert "CSI - Continuous Security Integration (8)" in response.text
    assert "CSD - Continuous Security Deployment (9)" in response.text
    assert "CSO - Continuous Security Operation (10)" in response.text
    assert "GRAU DE ADOÇÃO GLOBAL (AD%)" in response.text

    # Verifica botão e modal de exclusão de squad
    assert 'id="btn-delete-squad"' in response.text
    assert 'id="delete-squad-modal"' in response.text


def test_get_squads(client: TestClient):
    response = client.get("/api/squads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    codes = [sq["code"] for sq in data]
    assert "squad-a" in codes
    assert "squad-b" in codes
    assert "squad-c" in codes


def test_get_diagnostics_squad_a(client: TestClient):
    response = client.get("/api/diagnostics/squad-a")
    assert response.status_code == 200
    data = response.json()

    assert data["squad"]["code"] == "squad-a"
    assert data["global_adoption_degree"] == 20.3
    assert data["global_adoption_degree_formatted"] == "20.3%"
    assert len(data["dimension_scores"]) == 6
    assert len(data["stage_scores"]) == 5
    assert len(data["statements"]) == 40

    # Valida dimensões específicas da Squad A
    dim_dict = {d["dimension"]: d["adoption_degree"] for d in data["dimension_scores"]}
    assert dim_dict["Governança"] == 36.7
    assert dim_dict["Arquitetura e Design"] == 10.0
    assert dim_dict["Desenvol. e Revisão"] == 24.0
    assert dim_dict["Construção e Impl."] == 13.3
    assert dim_dict["Testes e Verificação"] == 14.3
    assert dim_dict["Operações e Obs."] == 23.8


def test_get_diagnostics_squad_b(client: TestClient):
    response = client.get("/api/diagnostics/squad-b")
    assert response.status_code == 200
    data = response.json()
    assert data["global_adoption_degree"] == 47.0
    assert data["global_adoption_degree_formatted"] == "47.0%"


def test_get_diagnostics_squad_c(client: TestClient):
    response = client.get("/api/diagnostics/squad-c")
    assert response.status_code == 200
    data = response.json()
    assert data["global_adoption_degree"] == 88.7
    assert data["global_adoption_degree_formatted"] == "88.7%"


def test_get_diagnostics_not_found(client: TestClient):
    response = client.get("/api/diagnostics/squad-inexistente")
    assert response.status_code == 404


def test_get_statements_catalog(client: TestClient):
    response = client.get("/api/statements")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 40


def test_get_statements_filter_dimension(client: TestClient):
    response = client.get("/api/statements?dimension=Governança")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    for item in data:
        assert item["smaf_dimension"] == "Governança"


def test_get_statements_filter_stage(client: TestClient):
    response = client.get("/api/statements?stage=A")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for item in data:
        assert item["sth_stage_code"] == "A"


def test_get_benchmark(client: TestClient):
    response = client.get("/api/benchmark")
    assert response.status_code == 200
    data = response.json()

    assert "dimensions" in data
    assert len(data["dimensions"]) == 6
    assert "stages" in data
    assert len(data["stages"]) == 5
    assert "global_summary" in data

    summary = data["global_summary"]
    assert summary["squad_a_pct"] == 20.3
    assert summary["squad_b_pct"] == 47.0
    assert summary["squad_c_pct"] == 88.7
    assert summary["organization_average_pct"] == 52.0


def test_update_audit_success(client: TestClient):
    payload = {
        "answers": [
            {"statement_code": "AO.01", "adoption_level": 4},
            {"statement_code": "AO.02", "adoption_level": 4},
        ]
    }
    response = client.put("/api/diagnostics/squad-a", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["squad"]["code"] == "squad-a"
    # Previously 20.3, with AO.01 (0.6->1.0, +0.4) and AO.02 (0.0->1.0, +1.0)
    # The score must be higher than 20.3
    assert data["global_adoption_degree"] > 20.3

    # Check persistence by issuing a GET
    get_res = client.get("/api/diagnostics/squad-a")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["global_adoption_degree"] == data["global_adoption_degree"]
    answers_map = {ans["statement_code"]: ans["adoption_level_num"] for ans in get_data["statements"]}
    assert answers_map["AO.01"] == 4
    assert answers_map["AO.02"] == 4


def test_update_audit_invalid_level(client: TestClient):
    payload = {
        "answers": [
            {"statement_code": "AO.01", "adoption_level": 5}
        ]
    }
    response = client.put("/api/diagnostics/squad-a", json=payload)
    assert response.status_code == 422


def test_update_audit_statement_not_found(client: TestClient):
    payload = {
        "answers": [
            {"statement_code": "INVALID.99", "adoption_level": 2}
        ]
    }
    response = client.put("/api/diagnostics/squad-a", json=payload)
    assert response.status_code == 422 or response.status_code == 404


def test_update_audit_squad_not_found(client: TestClient):
    payload = {
        "answers": [
            {"statement_code": "AO.01", "adoption_level": 2}
        ]
    }
    response = client.put("/api/diagnostics/squad-nao-existe", json=payload)
    assert response.status_code == 404


def test_create_squad_success(client: TestClient):
    payload = {
        "name": "Squad Logística",
        "purdue_level": "Nível 3 - Sistemas de Execução de Manufatura (MES)",
        "purdue_short": "N3 MES",
        "description": "Responsável por roteamento e esteiras industriais",
    }
    response = client.post("/api/squads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "squad-logistica"
    assert data["name"] == "Squad Logística"
    assert data["purdue_short"] == "N3 MES"

    # Confirm in squads list
    squads_res = client.get("/api/squads")
    assert squads_res.status_code == 200
    codes = [sq["code"] for sq in squads_res.json()]
    assert "squad-logistica" in codes

    # Confirm diagnostic initialization with 40 AL0 statements
    diag_res = client.get("/api/diagnostics/squad-logistica")
    assert diag_res.status_code == 200
    diag_data = diag_res.json()
    assert diag_data["global_adoption_degree"] == 0.0
    assert len(diag_data["statements"]) == 40
    for stmt in diag_data["statements"]:
        assert stmt["adoption_level_num"] == 0
        assert stmt["adoption_weight"] == 0.0


def test_create_squad_duplicate_rejected(client: TestClient):
    payload = {
        "name": "Squad A",
        "purdue_level": "Nível 2 OT",
        "purdue_short": "N2 OT",
    }
    response = client.post("/api/squads", json=payload)
    assert response.status_code == 409


def test_create_squad_validation_error(client: TestClient):
    payload = {
        "name": "S",  # Too short (min 2)
        "purdue_level": "N",
        "purdue_short": "",
    }
    response = client.post("/api/squads", json=payload)
    assert response.status_code == 422


def test_benchmark_stages_table_values(client: TestClient):
    response = client.get("/api/benchmark")
    assert response.status_code == 200
    data = response.json()

    assert "squads" in data
    assert len(data["squads"]) >= 3
    assert "stages" in data
    assert len(data["stages"]) == 5

    stages_dict = {stg["stage_code"]: stg for stg in data["stages"]}
    # Check exact values calculated from simulation dataset:
    # Estágio A: Squad A=60.0, Squad B=60.0, Squad C=86.7, Média=68.9
    stg_a = stages_dict["A"]
    assert stg_a["squad_a_pct"] == 60.0
    assert stg_a["squad_b_pct"] == 60.0
    assert stg_a["squad_c_pct"] == 86.7
    assert stg_a["average_pct"] == 68.9

    # Estágio B: Squad A=26.0, Squad B=54.0, Squad C=92.0, Média=57.3
    stg_b = stages_dict["B"]
    assert stg_b["squad_a_pct"] == 26.0
    assert stg_b["squad_b_pct"] == 54.0
    assert stg_b["squad_c_pct"] == 92.0
    assert stg_b["average_pct"] == 57.3

    # Estágio C: Squad A=10.0, Squad B=50.0, Squad C=85.0, Média=48.3
    stg_c = stages_dict["C"]
    assert stg_c["squad_a_pct"] == 10.0
    assert stg_c["squad_b_pct"] == 50.0
    assert stg_c["squad_c_pct"] == 85.0
    assert stg_c["average_pct"] == 48.3

    # Estágio D: Squad A=4.4, Squad B=31.1, Squad C=86.7, Média=40.7
    stg_d = stages_dict["D"]
    assert stg_d["squad_a_pct"] == 4.4
    assert stg_d["squad_b_pct"] == 31.1
    assert stg_d["squad_c_pct"] == 86.7
    assert stg_d["average_pct"] == 40.7

    # Estágio E: Squad A=23.0, Squad B=44.0, Squad C=88.0, Média=51.7
    stg_e = stages_dict["E"]
    assert stg_e["squad_a_pct"] == 23.0
    assert stg_e["squad_b_pct"] == 44.0
    assert stg_e["squad_c_pct"] == 88.0
    assert stg_e["average_pct"] == 51.7


def test_delete_squad_success_and_cascade(client: TestClient):
    # 1. Cria uma squad temporária
    payload = {
        "name": "Squad Temporaria Deletavel",
        "purdue_level": "Nível 2 - Controle de Processo (OT)",
        "purdue_short": "N2 TEMP",
        "description": "Squad criada exclusivamente para teste de exclusão.",
    }
    create_resp = client.post("/api/squads", json=payload)
    assert create_resp.status_code == 201
    squad_data = create_resp.json()
    code = squad_data["code"]
    squad_id = squad_data["id"]

    # 2. Confirma que o diagnóstico existe com 40 respostas
    diag_resp = client.get(f"/api/diagnostics/{code}")
    assert diag_resp.status_code == 200
    assert len(diag_resp.json()["statements"]) == 40

    # 3. Executa exclusão da squad
    del_resp = client.delete(f"/api/squads/{code}")
    assert del_resp.status_code == 200
    del_data = del_resp.json()
    assert del_data["deleted_code"] == code
    assert del_data["deleted_id"] == squad_id

    # 4. Confirma que a squad não é mais encontrada (404)
    after_resp = client.get(f"/api/diagnostics/{code}")
    assert after_resp.status_code == 404

    # 5. Confirma que não consta mais na listagem geral de squads
    squads_resp = client.get("/api/squads")
    assert squads_resp.status_code == 200
    codes = [sq["code"] for sq in squads_resp.json()]
    assert code not in codes


def test_delete_squad_not_found(client: TestClient):
    response = client.delete("/api/squads/squad-inexistente-xyz")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]


def test_delete_last_squad_forbidden(client: TestClient):
    # Squads padrão: squad-a, squad-b, squad-c (total 3)
    # Deleta 2 squads
    r1 = client.delete("/api/squads/squad-a")
    assert r1.status_code == 200
    r2 = client.delete("/api/squads/squad-b")
    assert r2.status_code == 200

    # Tenta deletar a 3ª e última squad remanescente
    r3 = client.delete("/api/squads/squad-c")
    assert r3.status_code == 400
    assert "Não é permitido excluir a única squad" in r3.json()["detail"]



