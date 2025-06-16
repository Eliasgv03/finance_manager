from django.shortcuts import render
import httpx  # Usamos httpx para llamadas asíncronas
from asgiref.sync import sync_to_async # Para envolver llamadas síncronas de BD
from users.models import UserProfile
from django.conf import settings

# Modificamos la función para que pre-cargue la relación 'default_currency'
# Esto evita una llamada síncrona a la BD desde un contexto asíncrono.
@sync_to_async
def get_user_profile_with_currency(user):
    return UserProfile.objects.select_related('default_currency').get(user=user)

async def get_conversion_context(request):
    """
    Función auxiliar asíncrona para obtener datos de conversión de moneda
    y preparar el contexto.
    """
    try:
        # Usamos la nueva función asíncrona que precarga la moneda
        user_profile = await get_user_profile_with_currency(user=request.user)
        
        value = float(request.GET.get('value', 1))
                # Ahora, esta línea es segura porque 'default_currency' ya está cargada
        from_currency_code = request.GET.get('from_currency', user_profile.default_currency.code)
        to_currency_code = request.GET.get('to_currency', None)

        api_key = settings.EXCHANGE_API_KEY
        api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency_code}"

        # Usamos un cliente asíncrono para la llamada a la API
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()

        if "conversion_rates" not in data:
            raise ValueError("Invalid API response format.")

        conversion_rates = data["conversion_rates"]
        currencies = sorted(conversion_rates.keys())

        # El resto de la lógica es funcional y no necesita cambios
        conversion_data = [
            {
                'currency': currency,
                'rate': rate,
                'converted_value': round(value * rate, 2)
            }
            for currency, rate in conversion_rates.items()
        ]

        single_conversion = None
        if to_currency_code:
            single_conversion = next(
                (item for item in conversion_data if item['currency'] == to_currency_code),
                None
            )

        return {
            'user_profile': user_profile,
            'value': value,
            'from_currency': from_currency_code,
            'to_currency': to_currency_code,
            'conversion_data': conversion_data,
            'single_conversion': single_conversion,
            'currencies': currencies,
            'error': None
        }

    except httpx.RequestError as e:
        # Intenta obtener user_profile aunque falle la API
        try:
            user_profile = await get_user_profile_with_currency(user=request.user)
            from_currency_code = user_profile.default_currency.code
        except Exception:
            user_profile = None
            from_currency_code = ''
        return {
            'error': f'Error connecting to the API: {e}',
            'user_profile': user_profile,
            'from_currency': from_currency_code,
            'to_currency': '',
            'currencies': [],
        }
    except ValueError as e:
        # Intenta obtener user_profile aunque falle la API
        try:
            user_profile = await get_user_profile_with_currency(user=request.user)
            from_currency_code = user_profile.default_currency.code
        except Exception:
            user_profile = None
            from_currency_code = ''
        return {
            'error': f"Invalid API response: {e}",
            'user_profile': user_profile,
            'from_currency': from_currency_code,
            'to_currency': '',
            'currencies': [],
        }
    except UserProfile.DoesNotExist:
        # Contexto mínimo para evitar errores en la plantilla
        return {
            'error': "User profile not found.",
            'user_profile': None,
            'from_currency': '',
            'to_currency': '',
            'currencies': [],
        }

async def convert_view(request):
    """
    Renderiza la página completa del conversor de moneda.
    """
    context = await get_conversion_context(request)
    return render(request, 'currencies/convert_currency.html', context)

async def conversion_results_partial(request):
    """
    Renderiza solo la plantilla parcial de resultados para HTMX.
    """
    context = await get_conversion_context(request)
    return render(request, 'currencies/partials/_conversion_results.html', context)
