from src.interest_rates import InterestRates
import pandas as pd
from datetime import datetime
interest_rates = InterestRates()

class Amortization:
    def calculation_amortization(self, 
                                 desembolso_date:str = datetime.now().strftime("%Y%m"),
                                 loan_amount:int = 100000000,
                                 interest_rate:float=12,
                                 type_rate:str="Efectiva",
                                 period:str="Anual",
                                 loan_term_years:float=20,
                                 insurance:float = 80000,
                                 abono_capital_all:dict={},
                                 )-> pd.DataFrame:
        
        monthly_interest_rate = interest_rates.calculate_interest_rate(interest_rate,type_rate,period,'Mensual') /100

        number_of_payments = loan_term_years * 12

        monthly_payment = (loan_amount * monthly_interest_rate *
                           (1 + monthly_interest_rate) ** number_of_payments) /\
                            ((1 + monthly_interest_rate)**number_of_payments -1)
        
        saldo = loan_amount
        anno_mes = desembolso_date

        amortization_table = [{
                    "num":0,
                    "anno_mes":anno_mes,
                    "interest":0,
                    "capital":0,
                    "insurance":0,
                    "payment":0,
                    "abono_capital":0,
                    "balance":saldo
                }]
        
        df_amortization_table_without_abono_capital = pd.DataFrame(
                                                self.amortization_abonos_capital(
                                                amortization_table.copy(),
                                                anno_mes,
                                                number_of_payments, 
                                                saldo,
                                                insurance,
                                                monthly_interest_rate, 
                                                monthly_payment,
                                                {}
                                                ))
        
        df_amortization_table = pd.DataFrame(
                                        self.amortization_abonos_capital(
                                        amortization_table.copy(),
                                        anno_mes,
                                        number_of_payments, 
                                        saldo,
                                        insurance,
                                        monthly_interest_rate, 
                                        monthly_payment,
                                        abono_capital_all))

        number_months_to_pay_total = df_amortization_table['num'].max()
        amount_paid_at_end = df_amortization_table['payment'].sum() + df_amortization_table['abono_capital'].sum() 
        amount_paid_without_abonos_capital = df_amortization_table_without_abono_capital['payment'].sum()

        print(f'Anual interest rate: {round(interest_rate,2)}%')
        print(f'Monthly interest rate: {round(monthly_interest_rate*100,4)}%')
        print(f'Amount paid without abonos capital: {amount_paid_without_abonos_capital:,.0f}')
        print(f'Number of months of the loan: {number_of_payments}')
        if len(abono_capital_all) > 0:
            print(f'Amount paid at end: {amount_paid_at_end:,.0f}')
            print(f'Money saved: {amount_paid_without_abonos_capital - amount_paid_at_end:,.0f}')
            print(f'Number of months you paid: {number_months_to_pay_total}')
            print(f'Number of months saved: {number_of_payments - number_months_to_pay_total}')
             
        return df_amortization_table
            
    def anno_mes_str(self, anno_mes):
        if int(anno_mes[4:]) == 12:
                anno = str(int(anno_mes[:4])+1)
                mes = '01'
        else:
            anno = anno_mes[:4]
            mes = str(int(anno_mes[4:])+1).zfill(2)
        
        anno_mes = anno + mes

        return anno_mes

    def amortization_abonos_capital(self, 
                                    amortization_table,
                                    anno_mes,
                                    number_of_payments,
                                    saldo,
                                    insurance,
                                    monthly_interest_rate, 
                                    monthly_payment,
                                    abono_capital_all
                                    ):
        
        month = 1
        while saldo > 0:
            # for month in range(1, number_of_payments + 1):
            anno_mes = self.anno_mes_str(anno_mes)
            interest = saldo * monthly_interest_rate
            abono = monthly_payment - interest
            abono_capital = min(abono_capital_all.get(anno_mes, 0),saldo)
            saldo = max(saldo - abono - abono_capital,0)

        # print(f"Month: {month}, Anno_mes: {anno_mes}, Interest: {interest}, Abono: {abono}, Abono Capital: {abono_capital}, Saldo: {saldo}")  # Depuración
            amortization_table.append(
                {
                    "num": month,
                    "anno_mes": anno_mes,
                    "interest": round(interest, 2),
                    "capital": round(abono, 2),
                    "insurance": round(insurance, 2),
                    "payment": round(monthly_payment + insurance, 2),
                    "abono_capital": abono_capital,
                    "balance": round(saldo, 2)
                }
            )

            month += 1

        return amortization_table

