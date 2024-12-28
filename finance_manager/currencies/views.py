from django.shortcuts import render
import requests
from users.models import UserProfile
from django.conf import settings

def convert_view(request):
    
    user_profile = UserProfile.objects.get(user=request.user)
    # Obtener valores de los parámetros GET
    value = float(request.GET.get('value', 1))  # Valor predeterminado: 1
    from_currency_code = request.GET.get('from_currency', user_profile.default_currency.code )  # Moneda predeterminada: USD
    to_currency_code = request.GET.get('to_currency', None)  # Moneda de destino (opcional)

    # Obtener el perfil del usuario (si aplica)
    
    
  

    # API key y URL base
    api_key = settings.EXCHANGE_API_KEY
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency_code}"

    try:
        # Solicitar tasas de cambio a la API
        response = requests.get(api_url)
        response.raise_for_status()  # Verificar respuesta exitosa
        data = response.json()

        # Validar formato de la respuesta
        if "conversion_rates" not in data:
            raise ValueError("Invalid API response format.")

        conversion_rates = data["conversion_rates"]
        currencies = sorted(conversion_rates.keys())  # Monedas disponibles ordenadas

        # Crear estructura de datos para la plantilla
        conversion_data = [
            {
                'currency': currency,
                'rate': rate,
                'converted_value': round(value * rate, 2)
            }
            for currency, rate in conversion_rates.items()
        ]

        # Filtrar conversión específica si se especifica una moneda de destino
        single_conversion = next(
            (item for item in conversion_data if item['currency'] == to_currency_code),
            None
        )

        # Contexto para la plantilla
        context = {
            'user_profile': user_profile,
            'value': value,
            'from_currency': from_currency_code,
            'to_currency': to_currency_code,
            'conversion_data': conversion_data,  # Lista de conversiones accesible
            'single_conversion': single_conversion,  # Conversión específica si aplica
            'currencies': currencies,  # Monedas ordenadas
        }

        return render(request, 'currencies/convert_currency.html', context)

    except requests.exceptions.RequestException as e:
        # Error de conexión con la API
        return render(request, 'currencies/convert_currency.html', {
            'error': f"Error connecting to the API: {str(e)}",
        })
    except ValueError as e:
        # Error de formato o datos inválidos
        return render(request, 'currencies/convert_currency.html', {
            'error': f"Invalid API response: {str(e)}",
        })
