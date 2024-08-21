from django.http import JsonResponse
from .models import WeatherData

def get_weather(request):
    # Obtiene los parámetros de la solicitud GET
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    datetime_param = request.GET.get('datetime')  # Se usa 'datetime' en lugar de 'tiempo_actual' para evitar problemas
    order = request.GET.get('order')  # Obtiene el parámetro 'order' si existe

    # Filtrar los datos por latitud y longitud
    queryset = WeatherData.objects.filter(latitud=lat, longitud=lon)
    
    # Si se proporciona el parámetro 'datetime', se filtra también por tiempo_actual
    if datetime_param:
        queryset = queryset.filter(tiempo_actual=datetime_param)
    
    # Ordenar los resultados si se solicita
    if order == 'asc':
        queryset = queryset.order_by('tiempo_actual')
    elif order == 'desc':
        queryset = queryset.order_by('-tiempo_actual')

    # Convertir el queryset a una lista de diccionarios para devolverlo como JSON
    datos_meteo = list(queryset.values())
    
    return JsonResponse(datos_meteo, safe=False)
