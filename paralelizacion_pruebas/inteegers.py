import pandas as pd

# Ruta del archivo CSV original
input_csv = "C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/promedio_tiempos_tipo1.csv"
# Ruta del archivo CSV modificado
output_csv = "C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/promedio_tiempos_tipo1_integers.csv"

# Leer el archivo CSV
df = pd.read_csv(input_csv)

# Convertir las columnas a enteros
df['cantidad_de_datos'] = df['cantidad_de_datos'].astype(int)
df['tiempo_en_milisegundos'] = df['tiempo_en_milisegundos'].astype(int)
df['nodos_threadpool'] = df['nodos_threadpool'].astype(int)

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv(output_csv, index=False)

print("Las columnas han sido convertidas a enteros y el archivo modificado se ha guardado en:", output_csv)
