import requests

url = 'https://api.open-meteo.com/v1/forecast?latitude=43.53573&longitude=-5.66152&hourly=temperature_2m,rain,wind_speed_10m&timezone=Europe%2FLondon'

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    print(data)

else:
    print(f'Error {response.status_code}. No se ha obtenido respuesta')