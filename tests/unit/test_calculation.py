import uuid

import pytest

from app.models import (
    AbstractCalculation,
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


@pytest.fixture
def user_id():
    return uuid.uuid4()


@pytest.mark.parametrize(
    ("calculation_type", "expected_class", "inputs", "expected_result"),
    [
        ("addition", Addition, [10, 5, 3], 18),
        ("subtraction", Subtraction, [20, 5, 3], 12),
        ("multiplication", Multiplication, [2, 3, 4], 24),
        ("division", Division, [100, 5, 2], 10),
    ],
)
def test_calculation_factory(
    user_id,
    calculation_type,
    expected_class,
    inputs,
    expected_result,
):
    calculation = Calculation.create(calculation_type, user_id, inputs)

    assert isinstance(calculation, expected_class)
    assert calculation.user_id == user_id
    assert calculation.inputs == inputs
    assert calculation.get_result() == expected_result


def test_calculation_factory_accepts_uppercase_type(user_id):
    calculation = Calculation.create("ADDITION", user_id, [4, 6])

    assert isinstance(calculation, Addition)
    assert calculation.get_result() == 10


def test_calculation_factory_rejects_unsupported_type(user_id):
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create("square", user_id, [4, 5])


@pytest.mark.parametrize(
    "calculation_class",
    [Addition, Subtraction, Multiplication, Division],
)
def test_calculation_rejects_non_list_inputs(calculation_class, user_id):
    calculation = calculation_class(user_id=user_id, inputs=(10, 5))

    with pytest.raises(ValueError, match="Inputs must be a list"):
        calculation.get_result()


@pytest.mark.parametrize(
    "calculation_class",
    [Addition, Subtraction, Multiplication, Division],
)
@pytest.mark.parametrize("inputs", [[], [10]])
def test_calculation_requires_at_least_two_inputs(
    calculation_class,
    user_id,
    inputs,
):
    calculation = calculation_class(user_id=user_id, inputs=inputs)

    with pytest.raises(
        ValueError,
        match="at least two numbers",
    ):
        calculation.get_result()


def test_addition_calculation(user_id):
    calculation = Addition(user_id=user_id, inputs=[1, 2, 3, 4])
    assert calculation.get_result() == 10


def test_subtraction_calculation(user_id):
    calculation = Subtraction(user_id=user_id, inputs=[20, 5, 3, 2])
    assert calculation.get_result() == 10


def test_multiplication_calculation(user_id):
    calculation = Multiplication(user_id=user_id, inputs=[2, 3, 4])
    assert calculation.get_result() == 24


def test_division_calculation(user_id):
    calculation = Division(user_id=user_id, inputs=[120, 3, 4])
    assert calculation.get_result() == 10


def test_division_by_zero_raises_error(user_id):
    calculation = Division(user_id=user_id, inputs=[10, 2, 0])

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation.get_result()


def test_abstract_calculation_get_result_raises_error():
    calculation = AbstractCalculation()

    with pytest.raises(
        NotImplementedError,
        match="Subclasses must implement get_result",
    ):
        calculation.get_result()


def test_calculation_string_representation():
    calculation = Calculation(type="calculation", inputs=[2, 3])

    assert repr(calculation) == "<Calculation(type=calculation, inputs=[2, 3])>"
