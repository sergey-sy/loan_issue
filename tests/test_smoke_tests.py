import pytest

from main import return_credit_decision
from loan_calculator.loan_calculator import ClientDataValidatorException


def test_approve_loan_smoke():
    input_data = {
        'age': '58',
        'gender': 'M',
        'income_source': 'businessman',
        'recent_year_income': '2',
        'credit_score': '0',
        'requested_amount': '1',
        'payment_term': '2',
        'credit_purpose': 'car'
    }
    expected_responce = dict(is_credit_available=True, year_payment=0.6025)
    assert return_credit_decision(input_data) == expected_responce


def test_reject_loan_smoke():
    input_data = {
        'age': '58',
        'gender': 'M',
        'income_source': 'businessman',
        'recent_year_income': '2',
        'credit_score': '0',
        'requested_amount': '5',
        'payment_term': '2',
        'credit_purpose': 'car'
    }
    expected_responce = dict(is_credit_available=False, year_payment=0)
    assert return_credit_decision(input_data) == expected_responce


def test_invalid_input_data_smoke():
    input_data = {
        'age': 'INVALID_DATA',
        'gender': 'M',
        'income_source': 'businessman',
        'recent_year_income': 2,
        'credit_score': 0,
        'requested_amount': 5,
        'payment_term': 2,
        'credit_purpose': 'car'
    }
    with pytest.raises(ClientDataValidatorException):
        return_credit_decision(input_data)
