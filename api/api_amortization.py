from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict
from src.interest_rates import InterestRates
from src.amortization import Amortization

app = FastAPI()
interest_rates = InterestRates()
amortization = Amortization()

app.mount("/static", StaticFiles(directory="static"), name="static")

class AmortizationRequest(BaseModel):
    desembolso_date:str
    loan_amount:float
    interest_rate:float
    type_rate:str
    period:str
    loan_term_years:float
    insurance: float = 0.0
    abono_capital_all: Dict[str, float]

@app.post('/amortization/')
async def calculate_amortization_table(request: AmortizationRequest):
    """
    Calcula la tabla de amortización con los parámetros proporcionados.

    Args:

        desembolso_date: Fecha en formato AAAAMM\n
        loan_amount: Monto total del préstamo\n
        interest_rate: Tasa de interés (porcentaje)\n
        type_rate: Tipo de tasa (Nominal/Efectiva)\n
        period: Periodo de la tasa (Anual/Mensual)\n
        loan_term_years: Plazo en años\n
        insurance: Valor del seguro (opcional)\n
        abono_capital_all: Diccionario de abonos {AAAAMM: valor}\n

    Returns:

        Dict con la tabla de amortización
    """
    
    try:
        if len(request.desembolso_date) != 6 or not (request.desembolso_date.isdigit()):
            raise ValueError("Formato de fecha inválido. Deber ser AAAAMM")
        
        amortization_table  = amortization.calculation_amortization(
        desembolso_date     = request.desembolso_date,
        loan_amount         = request.loan_amount,
        interest_rate       = request.interest_rate,
        type_rate           = request.type_rate,
        period              = request.period,
        loan_term_years     = request.loan_term_years,
        insurance           = request.insurance,
        abono_capital_all   = request.abono_capital_all,
            )

        return {"amortization_table":amortization_table.to_dict(orient='records')}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'error interno: {str(e)}')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # with open("templates/amortization_test.html","r", encoding="utf-8") as file:
        with open("templates/amortization.html","r", encoding="utf-8") as file:
            content = file.read()
            return HTMLResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al leer el archivo HTML: {str(e)}')