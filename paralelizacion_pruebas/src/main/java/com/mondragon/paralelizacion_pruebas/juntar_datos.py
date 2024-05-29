import pandas as pd
import glob

# Obtener la lista de nombres de archivos CSV de cada tipo en el directorio actual
file_list_type1 = glob.glob("C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/con_paralelizar_00*.csv")

# Leer y combinar archivos CSV del primer tipo
dfs_type1 = [pd.read_csv(file) for file in file_list_type1]
combined_df_type1 = pd.concat(dfs_type1, ignore_index=True)


combined_df_type1["tiempo_en_milisegundos"] = combined_df_type1["tiempo_en_milisegundos"].astype(int)

# Calcular el promedio de los tiempos para cada tipo
average_times_type1 = combined_df_type1.groupby(["nodos_threadpool", "cantidad_de_datos"])["tiempo_en_milisegundos"].mean().reset_index()

# Combinar los resultados en un solo DataFrame
# Guardar los resultados en archivos CSV separados
average_times_type1.to_csv("promedio_tiempos_tipo01.csv", index=False)
