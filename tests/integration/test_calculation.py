"""
Integration tests for Calculation model database operations.

Tests calculation creation, persistence, retrieval, relationships,
and database error handling using PostgreSQL.
"""

import pytest
from uuid import uuid4
from sqlalchemy.exc import IntegrityError

from app.models.calculation import Calculation


@pytest.mark.parametrize(
    "calculation_type, inputs, expected",
    [
        ("addition", [10, 5], 15),
        ("subtraction", [10, 5], 5),
        ("multiplication", [10, 5], 50),
        ("division", [10, 5], 2),
    ],
)
def test_calculation_factory_and_result(
    calculation_type, inputs, expected, test_user
):
    """Test factory creation and result calculation for all four types."""

    calculation = Calculation.create(
        calculation_type=calculation_type,
        user_id=test_user.id,
        inputs=inputs
    )

    assert calculation is not None
    assert calculation.get_result() == expected
    assert calculation.user_id == test_user.id


def test_create_and_persist_calculation(db_session, test_user):
    """Test saving a calculation record to PostgreSQL."""

    calculation = Calculation.create(
        calculation_type="addition",
        user_id=test_user.id,
        inputs=[20, 30]
    )

    calculation.result = calculation.get_result()

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    assert calculation.id is not None
    assert calculation.user_id == test_user.id
    assert calculation.type == "addition"
    assert calculation.inputs == [20, 30]
    assert calculation.result == 50


def test_retrieve_calculation_from_database(db_session, test_user):
    """Test retrieving a persisted calculation by its ID."""

    calculation = Calculation.create(
        calculation_type="multiplication",
        user_id=test_user.id,
        inputs=[4, 5]
    )

    calculation.result = calculation.get_result()

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    saved_id = calculation.id

    retrieved = db_session.query(Calculation).filter_by(
        id=saved_id
    ).first()

    assert retrieved is not None
    assert retrieved.id == saved_id
    assert retrieved.type == "multiplication"
    assert retrieved.inputs == [4, 5]
    assert retrieved.result == 20


def test_calculation_user_relationship(db_session, test_user):
    """Test the relationship between a calculation and its user."""

    calculation = Calculation.create(
        calculation_type="addition",
        user_id=test_user.id,
        inputs=[3, 7]
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    assert calculation.user is not None
    assert calculation.user.id == test_user.id


def test_unsupported_calculation_type(test_user):
    """Test that unsupported calculation types raise ValueError."""

    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type="power",
            user_id=test_user.id,
            inputs=[2, 3]
        )


def test_calculation_with_nonexistent_user(db_session):
    """Test that PostgreSQL rejects a calculation with an invalid user ID."""

    calculation = Calculation.create(
        calculation_type="addition",
        user_id=uuid4(),
        inputs=[10, 20]
    )

    db_session.add(calculation)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_division_by_zero_error(test_user):
    """Test that division by zero raises ValueError."""

    calculation = Calculation.create(
        calculation_type="division",
        user_id=test_user.id,
        inputs=[10, 0]
    )

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation.get_result()
