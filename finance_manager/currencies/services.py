

import requests
from .models import Currency


def get_exchange_rate(from_currency_code, to_currency_code):
    
    api_url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/{from_currency_code}"
    
    
    response = requests.get(api_url)
    data = response.json()

    if response.status_code == 200:
        
        exchange_rate = data['conversion_rates'].get(to_currency_code)
        if exchange_rate:
            return exchange_rate
        else:
            raise ValueError(f"No se encontró la tasa de cambio para {to_currency_code}.")
    else:
        raise ValueError(f"Error al obtener la tasa de cambio: {data.get('error', 'Desconocido')}")

def convert_currency(from_currency_code, to_currency_code, amount):
    
    rate = get_exchange_rate(from_currency_code, to_currency_code)
    
   
    converted_amount = amount * rate
    
    return converted_amount
