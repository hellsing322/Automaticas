#Se debe definir cual es el valor de Desviacion Tipica por variable 
# jemplo de Datos de Temperatura Máxima (Tmax) por Minuto

# Minuto	Tmax (°C)
# 1	25
# 2	26
# 3	28
# 4	29
# 5	30
# 6	35
# 7	36
# 8	31
# 9	29
# 10	28
# Aplicaremos la validación de coherencia temporal para períodos de 5 minutos, calculando la media y la desviación típica para cada periodo:

# Tabla: Validación de Coherencia Temporal para Periodos de 5 Minutos

# Período	Minutos (del 1 al 10)	Tmax (°C)	Media (°C)	Desviación Típica (σ)	Cumple Desviación < 2.5
# 1	1 al 5	25, 26, 28, 29, 30	27.6	2.49	Sí
# 2	2 al 6	26, 28, 29, 30, 35	29.6	3.27	No
# 3	3 al 7	28, 29, 30, 35, 36	31.6	3.75	No
# 4	4 al 8	29, 30, 35, 36, 31	32.2	2.81	Sí
# 5	5 al 9	30, 35, 36, 31, 29	32.2	3.67	No
# 6	6 al 10	35, 36, 31, 29, 28	31.8	3.67	No
# En este ejemplo, se calcularon las medias y desviaciones típicas para cada período de 5 minutos. Se observa que algunos períodos cumplen con la condición de que la desviación típica sea menor que 2.5 (Sí), mientras que otros no (No).

# Para datos por minuto, el nivel 4 de validación de coherencia temporal puede ser útil para identificar variaciones inusuales o anomalías en intervalos de tiempo más cortos. Sin embargo, los resultados pueden variar dependiendo de los datos específicos que se estén analizando. Si la desviación típica supera el valor mínimo aceptable (2.5), algunos datos podrían considerarse sospechosos o requerir una revisión adicional.
# Para calcular la desviación típica (o desviación estándar) de un conjunto de datos, sigue los siguientes pasos:

# Calcula la media (promedio) de los datos. Para ello, suma todos los valores y divide el resultado entre la cantidad de datos.

# Resta la media a cada valor individual del conjunto de datos.

# Calcula el cuadrado de cada diferencia (para eliminar los signos negativos).

# Calcula el promedio de los cuadrados obtenidos en el paso anterior.

# Finalmente, obtén la raíz cuadrada del valor obtenido en el paso 4.

# La fórmula matemática para la desviación típica es la siguiente:

# Desviación Típica (σ) = √(Σ(xi - μ)² / n)

# Donde:

# σ es la desviación típica.
# Σ representa la suma de los valores que se obtienen a partir de los siguientes cálculos.
# xi son los valores individuales del conjunto de datos.
# μ es la media (promedio) de los datos.
# n es la cantidad total de datos en el conjunto.
# Veamos un ejemplo de cómo calcular la desviación típica para un conjunto de datos:

# Ejemplo: Calcula la desviación típica para los siguientes valores: 10, 15, 20, 25, 30.

# Calculamos la media: (10 + 15 + 20 + 25 + 30) / 5 = 20.

# Restamos la media a cada valor individual:
# (10 - 20) = -10
# (15 - 20) = -5
# (20 - 20) = 0
# (25 - 20) = 5
# (30 - 20) = 10

# Calculamos el cuadrado de cada diferencia:
# (-10)² = 100
# (-5)² = 25
# (0)² = 0
# (5)² = 25
# (10)² = 100

# Calculamos el promedio de los cuadrados: (100 + 25 + 0 + 25 + 100) / 5 = 50.

# Finalmente, obtenemos la raíz cuadrada de 50: √50 ≈ 7.07.

# La desviación típica para este conjunto de datos es aproximadamente 7.07. Esto nos indica que los valores tienden a variar alrededor de la media en aproximadamente 7.07 unidades.