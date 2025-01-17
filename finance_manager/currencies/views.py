from django.shortcuts import render
import requests
from users.models import UserProfile
from django.conf import settings

def convert_view(request):
    
    user_profile = UserProfile.objects.get(user=request.user)
   
    value = float(request.GET.get('value', 1))  
    from_currency_code = request.GET.get('from_currency', user_profile.default_currency.code )  
    to_currency_code = request.GET.get('to_currency', None) 

    
    api_key = settings.EXCHANGE_API_KEY
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency_code}"

    try:
       
        response = requests.get(api_url)
        response.raise_for_status()  
        data = response.json()

       
        if "conversion_rates" not in data:
            raise ValueError("Invalid API response format.")

        conversion_rates = data["conversion_rates"]
        currencies = sorted(conversion_rates.keys())  
       
        conversion_data = [
            {
                'currency': currency,
                'rate': rate,
                'converted_value': round(value * rate, 2)
            }
            for currency, rate in conversion_rates.items()
        ]

       
        single_conversion = next(
            (item for item in conversion_data if item['currency'] == to_currency_code),
            None
        )

        context = {
            'user_profile': user_profile,
            'value': value,
            'from_currency': from_currency_code,
            'to_currency': to_currency_code,
            'conversion_data': conversion_data, 
            'single_conversion': single_conversion,  
            'currencies': currencies, 
        }

        return render(request, 'currencies/convert_currency.html', context)

    except requests.exceptions.RequestException as e:
        
        return render(request, 'currencies/convert_currency.html', {
            'error': f"Error connecting to the API: {str(e)}",
        })
    except ValueError as e:
       
        return render(request, 'currencies/convert_currency.html', {
            'error': f"Invalid API response: {str(e)}",
        })
