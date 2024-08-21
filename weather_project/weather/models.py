from django.db import models

class WeatherData(models.Model):
    tiempo_actual = models.DateTimeField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    temperatura = models.FloatField()
    precipitaciones = models.FloatField()
    velocidad_viento = models.FloatField()

    def __str__(self):
        return f"{self.tiempo_actual} - {self.latitud}, {self.longitud}"

