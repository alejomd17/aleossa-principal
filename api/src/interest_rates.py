class InterestRates():
    dict_period = {'Mensual':1,
                'Semestral':6,
                'Anual':12}

    def nominal_efectiva(self, initial_rate:float,current_period:str) -> float:
        # Si es Nominal Siempre la vuelvo anual
        interes_rates = initial_rate / self.dict_period[current_period]
        current_period = 'Mensual'
        return interes_rates, current_period

    def calculate_interest_rate(self, initial_rate:float, rate_type:str,current_period:str, wished_period:str) -> float:
        if rate_type == 'Nominal':
            initial_rate, current_period = self.nominal_efectiva(initial_rate, current_period)

        new_interest_rate = (((1+(initial_rate/100))**(self.dict_period[wished_period]/self.dict_period[current_period]))-1) * 100

        return round(new_interest_rate,4)