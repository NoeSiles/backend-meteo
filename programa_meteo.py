#Paso 1: obtener datos metereológicos

import requests
import datetime

url = 'https://api.open-meteo.com/v1/forecast?latitude=43.53573&longitude=-5.66152&hourly=temperature_2m,rain,wind_speed_10m&timezone=Europe%2FLondon'

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    tiempo_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperatura = data['hourly']['temperature_2m'][0]
    precipitaciones = data['hourly']['rain'][0]
    velocidadViento = data['hourly']['wind_speed_10m'][0]

    print(f'Fecha y hora actuales: {tiempo_actual} \nTemperatura: {temperatura} \nPrecipitaciones: {precipitaciones} \nVelocidad del viento: {velocidadViento}')
           

else:
    print(f'Error {response.status_code}. No se ha obtenido respuesta')

#Paso 2: guardar datos consultados en bbdd

import sqlite3

def crear_bbdd():
    conn = sqlite3.connect('datos_meteo.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY,
                        tiempo_actual TEXT,
                        latitud REAL,
                        longitud REAL,
                        temperatura REAL,
                        precipitaciones REAL,
                        velocidadViento REAL
                    )''')
    conn.commit()
    conn.close()

    def insert_datos_meteo(lat, lon, datos_meteo):
        conn = sqlite3.connect('datos_meteo.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO weather (tiempo_actual, latitud, longitud, temperatura, precipitaciones, velocidad_viento)
                      VALUES (?, ?, ?, ?, ?, ?)''', (datos_meteo['tiempo_actual'], lat, lon, datos_meteo['temperatura'], datos_meteo['precipitaciones'], datos_meteo['velocidadViento']))
        conn.commit()
        conn.close()

#Paso 3: Crear un endpoint para recuperar los datos
