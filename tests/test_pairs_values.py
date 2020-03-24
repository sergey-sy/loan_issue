import pytest

from main import return_credit_decision
from tests.tools.pairwise_client_data import get_pairwise_object


@pytest.fixture(params=get_pairwise_object())
def fixture_with_params(request):
    return request.param


def test_pairs(fixture_with_params):
    """
    Check that function return_credit_decision works with all pairs combination
    """
    input_keys = [
        'age',
        'gender',
        'income_source',
        'recent_year_income',
        'credit_score',
        'requested_amount',
        'payment_term',
        'credit_purpose'
    ]

    input_values = fixture_with_params
    c = dict(zip(input_keys, input_values))

    credit_decision = return_credit_decision(c)
    assert credit_decision['is_credit_available'] in [False, True]
