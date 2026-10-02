import pytest
from models import (
    ADOPTION_LEVEL_WEIGHTS,
    get_adoption_weight,
    calculate_group_adoption_degree,
    calculate_global_adoption_degree,
)

def test_adoption_level_weights():
    assert get_adoption_weight(0) == 0.0
    assert get_adoption_weight(1) == 0.1
    assert get_adoption_weight(2) == 0.3
    assert get_adoption_weight(3) == 0.6
    assert get_adoption_weight(4) == 1.0

    with pytest.raises(ValueError):
        get_adoption_weight(5)

    with pytest.raises(ValueError):
        get_adoption_weight(-1)


def test_calculate_group_adoption_degree_edge_cases():
    assert calculate_group_adoption_degree([]) == 0.0
    assert calculate_group_adoption_degree([1.0]) == 100.0
    assert calculate_group_adoption_degree([0.0]) == 0.0
    assert calculate_group_adoption_degree([0.6, 0.6]) == 60.0


def test_canonical_squad_a_dimension_math():
    # Squad A (N2 OT) pesos por dimensão SMAF
    gov_weights = [0.6, 0.6, 0.3, 0.3, 0.1, 0.3]  # sum=2.2, n=6
    arq_weights = [0.3, 0.3, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0]  # sum=0.8, n=8
    des_weights = [0.3, 0.3, 0.3, 0.3, 0.0]  # sum=1.2, n=5
    con_weights = [0.1, 0.1, 0.3, 0.3, 0.0, 0.0]  # sum=0.8, n=6
    tes_weights = [0.6, 0.1, 0.3, 0.0, 0.0, 0.0, 0.0]  # sum=1.0, n=7
    ope_weights = [0.1, 0.0, 0.1, 0.0, 0.0, 1.0, 0.1, 0.6]  # sum=1.9, n=8

    ad_gov = calculate_group_adoption_degree(gov_weights)
    ad_arq = calculate_group_adoption_degree(arq_weights)
    ad_des = calculate_group_adoption_degree(des_weights)
    ad_con = calculate_group_adoption_degree(con_weights)
    ad_tes = calculate_group_adoption_degree(tes_weights)
    ad_ope = calculate_group_adoption_degree(ope_weights)

    assert round(ad_gov, 1) == 36.7
    assert round(ad_arq, 1) == 10.0
    assert round(ad_des, 1) == 24.0
    assert round(ad_con, 1) == 13.3
    assert round(ad_tes, 1) == 14.3
    assert round(ad_ope, 1) == 23.8

    ad_global_squad_a = calculate_global_adoption_degree([
        ad_gov, ad_arq, ad_des, ad_con, ad_tes, ad_ope
    ])
    assert round(ad_global_squad_a, 1) == 20.3


def test_canonical_squad_b_and_c_global_math():
    # Dimensões Squad B (N3 MES)
    squad_b_dim_ads = [55.0, 37.5, 54.0, 51.66666666666667, 40.0, 43.75]
    ad_global_squad_b = calculate_global_adoption_degree(squad_b_dim_ads)
    assert round(ad_global_squad_b, 1) == 47.0

    # Dimensões Squad C (N4 ERP)
    squad_c_dim_ads = [93.33333333333333, 80.0, 92.0, 100.0, 77.14285714285714, 90.0]
    ad_global_squad_c = calculate_global_adoption_degree(squad_c_dim_ads)
    assert round(ad_global_squad_c, 1) == 88.7

    # Média Organizacional Global
    org_average = (ad_global_squad_b + ad_global_squad_c + 20.333333333333332) / 3
    assert round(org_average, 1) == 52.0


def test_canonical_sth_stages_math():
    # Estágio A: 3 itens, Squad A weights = [0.6, 0.6, 0.6] -> 1.8 / 3 -> 60.0%
    assert round(calculate_group_adoption_degree([0.6, 0.6, 0.6]), 1) == 60.0
    # Estágio B: 10 itens, Squad A weights -> sum=2.6 / 10 -> 26.0%
    assert round(calculate_group_adoption_degree([0.3, 0.3, 0.3, 0.3, 0.1, 0.6, 0.1, 0.3, 0.3, 0.0]), 1) == 26.0
    # Estágio C: 8 itens, Squad A weights -> sum=0.8 / 8 -> 10.0%
    assert round(calculate_group_adoption_degree([0.3, 0.3, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0]), 1) == 10.0
    # Estágio D: 9 itens, Squad A weights -> sum=0.4 / 9 -> 4.4%
    assert round(calculate_group_adoption_degree([0.1, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]), 1) == 4.4
    # Estágio E: 10 itens, Squad A weights -> sum=2.3 / 10 -> 23.0%
    assert round(calculate_group_adoption_degree([0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.6, 1.0, 0.0, 0.6]), 1) == 23.0

