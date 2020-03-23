from loan_calculator.loan_calculator import Client, ClientDataValidator


INPUT_DATA = {
    'age': '18',
    'gender': 'F',
    'income_source': 'businessman',
    'recent_year_income': '2',
    'credit_score': '2',
    'requested_amount': '1',
    'payment_term': '2',
    'credit_purpose': 'car'
}


def return_credit_decision(raw_client_data=INPUT_DATA):
    """
    Take client data and return credit decision.
    Use this function such as API for loan calculator.
    Input data should be such as INPUT_DATA. Inside the loan_calculator
    input data converted to format like loan_calculator/client_config_schema.json.
    Function return # dict(is_credit_available=True or False, year_payment=float in millions)
    """

    client_data = ClientDataValidator.validate(raw_client_data)
    client = Client(client_data)
    return client.make_credit_decision()


if __name__ == '__main__':
    credit_decision = return_credit_decision()
    if credit_decision['is_credit_available']:
        print(f"Pre-certified for a loan of up to MLN {credit_decision['year_payment']}.")
    else:
        print("Loan has not approved")
