from math import log


class Client:
    """Class that create client object and make decision about credit accessibility"""
    def __init__(self, client_data: dict):
        self._client_data = client_data

        if self._client_data['gender'] == 'M':
            self._client_data['retirement_age'] = 65
        elif self._client_data['gender'] == 'F':
            self._client_data['retirement_age'] = 60
        else:
            self._client_data['retirement_age'] = 'Error_unknown_retirement_age'

        self._available_amount = AvailableAmount.get_available_amount(client_data)

        self.decision = dict(is_credit_available=False,
                             year_payment=0)

    def get_block_reasons(self) -> list:
        """Is there any reason to reject of credit"""
        self.block_reasons = list()
        if self._client_data['age'] + self._client_data['payment_term'] >= \
                self._client_data['retirement_age']:
            self.block_reasons.append(True)
        if self._client_data['requested_amount'] / self._client_data['payment_term'] > \
                self._client_data['recent_year_income'] / 3:
            self.block_reasons.append(True)
        if self._client_data['credit_score'] == -2:
            self.block_reasons.append(True)
        if self._client_data['income_source'] == 'unemployed':
            self.block_reasons.append(True)

        return self.block_reasons


    def make_credit_decision(self) -> dict:
        """Method that check all requirements to client and return credit decision"""
        if self._available_amount and \
                self._available_amount >= self._client_data['requested_amount'] and \
                not self.get_block_reasons():
            year_payment = YearPayment(self._client_data).calculate_year_payment()
            if year_payment and year_payment < self._client_data['recent_year_income'] / 2:
                self.decision['is_credit_available'] = True
                self.decision['year_payment'] = year_payment

        return self.decision


class AvailableAmount:
    AMOUNT_TABLE = {
        'credit_score': {-2: 0,
                         -1: 1,
                         0: 5,
                         1: 10,
                         2: 10},
        'income_source': {'passive': 1,
                          'employee': 5,
                          'businessman': 10,
                          'unemployed': 0}
    }

    @classmethod
    def get_available_amount(cls, client_data: dict, amount_table=AMOUNT_TABLE) -> int:
        """Checking maximum available amount to client"""
        amount = dict()
        amount['credit_score'] = amount_table['credit_score'][client_data['credit_score']]
        amount['income_source'] = amount_table['income_source'][client_data['income_source']]
        return (min(amount.values()))


class ClientDataValidatorException(Exception):
    pass


class ClientDataValidator(ClientDataValidatorException):

    @classmethod
    def validate(cls, client_data: dict) -> dict:
        """Trying to convert client data to the required format"""
        try:
            client_data['age'] = int(client_data['age'])
            client_data['gender'] = str(client_data['gender']).upper()
            client_data['income_source'] = str(client_data['income_source']).lower()
            client_data['recent_year_income'] = int(client_data['recent_year_income'])
            client_data['credit_score'] = int(client_data['credit_score'])
            client_data['requested_amount'] = float(client_data['requested_amount'])
            client_data['payment_term'] = int(client_data['payment_term'])
            client_data['credit_purpose'] = str(client_data['credit_purpose']).lower()
        except ValueError:
            raise ClientDataValidatorException("""
                Failed in ClientDataValidator.validate.
                ValueError, failed during client data validation.
                Some data impossible to convert.
                The transmitted data must match with loan_calculator/client_config_schema.json""")
        else:  # TODO refactor to cycle or function
            if not 0 <= (foo := client_data['age']) <= 150:
                raise ClientDataValidatorException(f'Client age is "{foo}", but should be in range 0 <= age <= 150')
            if (foo := client_data['gender']) not in ['F', 'M']:
                raise ClientDataValidatorException(f'Client gender value is "{foo}", but should be F or M')
            if (foo := client_data['income_source']) not in ['passive', 'employee',	'businessman', 'unemployed']:
                raise ClientDataValidatorException(f"""Client income_source value is "{foo}",
                    but should be passive or employee or businessman or unemployed""")
            if not 0 <= (foo := client_data['recent_year_income']) <= 1000:
                raise ClientDataValidatorException(f"""Client recent_year_income is "{foo}",
                    but should be in range 0 <= age <= 1000""")
            if not -2 <= (foo := client_data['credit_score']) <= 2:
                raise ClientDataValidatorException(f'Client age is "{foo}", but should be in range 0 <= age <= 150')
            if not 0.1 <= (foo := client_data['requested_amount']) <= 10:
                raise ClientDataValidatorException(f"""Client requested_amount is "{foo}",
                    but should be in range 0.1 <= age <= 10""")
            if not 1 <= (foo := client_data['payment_term']) <= 20:
                raise ClientDataValidatorException(f"""Client payment_term is "{foo}",
                    but should be in range 1 <= age <= 20""")
            if (foo := client_data['credit_purpose']) not in ['mortgage', 'business', 'car',	'consumer']:
                raise ClientDataValidatorException(f"""Client credit_purpose value is "{foo}", but should be
                    mortgage or business or car or consumer""")
            return client_data


class Modifier:
    MODIFIERS_TABLE = {
        'credit_purpose': {'mortgage': -0.02,
                           'business': -0.005,
                           'car': 0,
                           'consumer': 0.015},
        'credit_score': {-1: 0.015,
                         0: 0,
                         1: -0.0025,
                         2: -0.0075},
        'income_source': {'passive': 0.005,
                          'employee': -0.0025,
                          'businessman': 0.0025,
                          'unemployed': 0}
    }

    @classmethod
    def get_total_modifier(cls, client_data: dict, modifiers_table=MODIFIERS_TABLE) -> dict:
        """Get all credit score modifiers which are depending from client data"""
        modifiers = dict()
        try:
            requested_amount_modifier = -log(client_data['requested_amount'], 10) / 100
        except ValueError:
            print("It's impossible to get log(<=0, 10). Loan requested amount can't be <= 0")
            requested_amount_modifier = None
        modifiers['requested_amount'] = requested_amount_modifier
        modifiers['credit_purpose'] = modifiers_table['credit_purpose'][client_data['credit_purpose']]
        modifiers['credit_score'] = modifiers_table['credit_score'][client_data['credit_score']]
        modifiers['income_source'] = modifiers_table['income_source'][client_data['income_source']]
        return modifiers


class YearPayment:
    def __init__(self, client_data: dict):
        self.__basic_rate = 0.10
        self.__client_data = client_data
        self.__rate_modifiers = Modifier.get_total_modifier(client_data)
        
    def calculate_year_payment(self) -> float or None:
        """Calculate year payment for client"""
        try:
            # (<requested_amount> * (1 + <payment_term> * (<basic_rate> + <modifiers>))) / <payment_term>
            year_payment = (
                    (
                            self.__client_data['requested_amount'] *
                            (
                                    1 +
                                    self.__client_data['payment_term'] *
                                    (
                                            self.__basic_rate + sum(self.__rate_modifiers.values())
                                    )
                            )
                    )
                    /
                    self.__client_data['payment_term']
            )
            return year_payment
        except TypeError:
            return None
