import requests
import datetime
import sqlite3
from flask import Flask, request, jsonify

def get_weather_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,wind_speed_10m&timezone=Europe%2FLondon"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extraer los datos necesarios
        temperature = data['hourly']['temperature_2m'][0]
        precipitation = data['hourly']['rain'][0]
        windspeed = data['hourly']['wind_speed_10m'][0]
        
        return {
            "tiempo_actual": current_time,
            "temperatura": temperature,
            "precipitaciones": precipitation,
            "velocidadViento": windspeed
        }
    else:
        print(f'Error {response.status_code}. No se ha obtenido respuesta')
        return None

# Paso 2: guardar datos consultados en bbdd
def create_db():
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
    cursor.execute('''INSERT INTO weather (tiempo_actual, latitud, longitud, temperatura, precipitaciones, velocidadViento)
                      VALUES (?, ?, ?, ?, ?, ?)''', (datos_meteo['tiempo_actual'], lat, lon, datos_meteo['temperatura'], datos_meteo['precipitaciones'], datos_meteo['velocidadViento']))
    conn.commit()
    conn.close()

# Crear un endpoint para recuperar los datos
app = Flask(__name__)

@app.route('/get_weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    datetime_param = request.args.get('tiempo_actual', type=str)
    order = request.args.get('order', type=str)
    
    conn = sqlite3.connect('datos_meteo.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM weather WHERE latitud=? AND longitud=?"
    params = [lat, lon]
    
    if datetime_param:
        query += " AND tiempo_actual=?"
        params.append(datetime_param)
    
    if order == 'asc':
        query += " ORDER BY tiempo_actual ASC"
    elif order == 'desc':
        query += " ORDER BY tiempo_actual DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    datos_meteo = []
    for row in rows:
        datos_meteo.append({
            "id": row[0],
            "tiempo_actual": row[1],
            "latitud": row[2],
            "longitud": row[3],
            "temperatura": row[4],
            "precipitaciones": row[5],
            "velocidadViento": row[6]
        })
    
    return jsonify(datos_meteo)

if __name__ == '__main__':
    create_db()  # Crear la base de datos y la tabla si no existe
    app.run(debug=True)

    # Ejecución del script para obtener y guardar datos
lat = 43.53573
lon = -5.66152

datos_meteo = get_weather_data(lat, lon)
if datos_meteo:
    insert_datos_meteo(lat, lon, datos_meteo)