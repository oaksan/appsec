from sqlmodel import Session, select
from models import Squad, Statement, AssessmentAnswer

def test_seed_database_counts(session: Session):
    statements = session.exec(select(Statement)).all()
    squads = session.exec(select(Squad)).all()
    answers = session.exec(select(AssessmentAnswer)).all()

    assert len(statements) == 40
    assert len(squads) == 3
    assert len(answers) == 120  # 40 afirmacoes * 3 squads


def test_seed_database_squad_purdue_levels(session: Session):
    squad_a = session.exec(select(Squad).where(Squad.code == "squad-a")).first()
    squad_b = session.exec(select(Squad).where(Squad.code == "squad-b")).first()
    squad_c = session.exec(select(Squad).where(Squad.code == "squad-c")).first()

    assert squad_a is not None
    assert squad_b is not None
    assert squad_c is not None

    assert "Nível 2" in squad_a.purdue_level
    assert "Nível 3" in squad_b.purdue_level
    assert "Nível 4" in squad_c.purdue_level


def test_seed_database_statements_dimensions(session: Session):
    statements = session.exec(select(Statement)).all()
    dimensions = {s.smaf_dimension for s in statements}

    expected_dimensions = {
        "Governança",
        "Arquitetura e Design",
        "Desenvol. e Revisão",
        "Construção e Impl.",
        "Testes e Verificação",
        "Operações e Obs.",
    }
    assert dimensions == expected_dimensions

