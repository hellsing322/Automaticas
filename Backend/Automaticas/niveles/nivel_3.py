# Solo se debe analizar que los valores maximos promedios y minimos no tengan discrepacias 
# Tabla 1: Ejemplo con Datos de Temperatura

# Día	Tmax (°C)	Tmin (°C)	Tmed (°C)	Cumple Tmax > Tmin	Cumple Tmax > Tmed > Tmin	Rango Diario (Tmax - Tmin)	Datos Coherentes
# 1	30	20	25	Sí	Sí	10	Sí
# 2	28	18	23	Sí	Sí	10	Sí
# 3	29	21	25	Sí	Sí	8	Sí
# 4	32	22	27	Sí	Sí	10	Sí
# 5	27	19	23	Sí	Sí	8	Sí
# 6	31	23	27	Sí	Sí	8	Sí
# 7	33	24	28	Sí	Sí	9	Sí
# En este ejemplo, todos los datos de temperatura cumplen con las comprobaciones de coherencia interna, ya que se mantienen las relaciones lógicas entre Tmax, Tmin y Tmed, y los rangos diarios son razonables.

# Tabla 2: Ejemplo con Datos de Precipitación

# Día	Precipitación (mm)	Cumple Precipitación > 0	Cumple Acumulado Día Actual > Acumulado Día Anterior	Datos Coherentes
# 1	5	Sí	Sí	Sí
# 2	10	Sí	Sí	Sí
# 3	2	Sí	Sí	Sí
# 4	15	Sí	Sí	Sí
# 5	0	No	Sí	No
# 6	8	Sí	Sí	Sí
# 7	12	Sí	Sí	Sí
# En este ejemplo, los datos de precipitación para el día 5 no cumplen con la comprobación de que la precipitación debe ser mayor que 0, lo que indica un error o dato faltante. A pesar de ese dato incorrecto, los demás valores cumplen con las comprobaciones de coherencia interna.