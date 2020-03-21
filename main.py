INPUT_DATA = {
    'age': '30',
    'gender': 'M',
    'income_source': 'employee',
    'recent_year_income': '2000_000',
    'credit_score': '0',
    'requested_amount': '500_000',
    'payment_term': '10',
    'credit_purpose': 'car'
}


def get_client_data():
    # get data from keyboard
    return INPUT_DATA


def return_credit_decision(input_data):
    credit_decision = dict(is_credit_available=True, credit_amount=1_000)
    return credit_decision


if __name__ == '__main__':
    # input_data = get_client_data()
    input_data = INPUT_DATA
    credit_decision = return_credit_decision(input_data)
    if credit_decision['is_credit_available']:
        print(f"Pre-certified for a loan of up to ${credit_decision['credit_amount']}.")
    else:
        print("Loan has not approved")
