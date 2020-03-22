from jsonschema import validate


input_data = {
    'age': 58,
    'gender': 'M',
    'income_source': 'businessman',
    'recent_year_income': 2,
    'credit_score': 0,
    'requested_amount': 1,
    'payment_term': 2,
    'credit_purpose': 'car'
}


def test_validate_client_schema(client_data=input_data):
    '''
    Validate json-schema for incoming client data
    '''
    schema = {
        'type': 'object',
        'properties': {
            'age': {"type" : "number"},
            'gender': {"type" : "string"},
            'income_source': {"type" : "string"},
            'recent_year_income': {"type" : "number"},
            'credit_score': {"type" : "number"},
            'requested_amount': {"type" : "number"},
            'payment_term': {"type" : "number"}
        }
    }

    responce = client_data #TODO realise getting data
    validate(responce, schema)
    # if haven't validate raise exception
    assert True
