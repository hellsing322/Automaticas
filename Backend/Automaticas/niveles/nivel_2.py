
#Definir cual es el limite de diferencia que peude haber por variable
# Supongamos que tenemos los siguientes datos:

# Fecha y Hora	Temperatura (°C)
# 2023-07-25 12:00	25.5
# 2023-07-25 12:01	26.0
# 2023-07-25 12:02	25.8
# 2023-07-25 12:03	25.3
# 2023-07-25 12:04	25.2
# ...	...
# 2023-07-25 12:29	26.5
# 2023-07-25 12:30	26.7
# 2023-07-25 12:31	27.5
# 2023-07-25 12:32	28.2
# 2023-07-25 12:33	25.8
# ...	...
# En este ejemplo, estamos analizando la coherencia temporal de la temperatura cada 30 minutos. Comenzaremos comparando la temperatura a las 12:00 con la temperatura a las 12:30, luego a las 12:30 con la temperatura a las 13:00 y así sucesivamente.

# Aplicamos el NIVEL 2 de validación de la coherencia temporal del dato de la siguiente manera:

# Comparamos la temperatura a las 12:00 (25.5 °C) con la temperatura a las 12:30 (26.7 °C):

# Diferencia = 26.7 - 25.5 = 1.2 °C (Menor que 3 °C, la diferencia es aceptable).
# Comparamos la temperatura a las 12:30 (26.7 °C) con la temperatura a las 13:00 (27.5 °C):

# Diferencia = 27.5 - 26.7 = 0.8 °C (Menor que 3 °C, la diferencia es aceptable).
# Comparamos la temperatura a las 13:00 (27.5 °C) con la temperatura a las 13:30 (28.2 °C):

# Diferencia = 28.2 - 27.5 = 0.7 °C (Menor que 3 °C, la diferencia es aceptable).
# Y así sucesivamente para cada par de mediciones consecutivas.

# En este ejemplo, todas las diferencias entre las mediciones consecutivas de temperatura son menores que 3 grados Celsius, por lo que no se generaría ninguna alerta para estos datos.

# Es importante señalar que este es solo un ejemplo ilustrativo. En la aplicación real, debes considerar un conjunto más extenso de datos y ajustar el valor preestablecido según las condiciones específicas y los requisitos de precisión de tus mediciones meteorológicas. Además, este proceso se debe repetir para cada variable que desees analizar en tus datos meteorológicos.