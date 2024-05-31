import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
con_paralelizar_df = pd.read_csv("C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/paralelizar_promedio.csv")

# Verificar los tipos de datos
print(con_paralelizar_df.dtypes)

# Convertir columnas a tipos numéricos si es necesario
con_paralelizar_df['cantidad_de_datos'] = pd.to_numeric(con_paralelizar_df['cantidad_de_datos'], errors='coerce')
con_paralelizar_df['nodos_threadpool'] = pd.to_numeric(con_paralelizar_df['nodos_threadpool'], errors='coerce')
con_paralelizar_df['tiempo_en_milisegundos'] = pd.to_numeric(con_paralelizar_df['tiempo_en_milisegundos'], errors='coerce')

# Verificar si hay NaNs después de la conversión
print(con_paralelizar_df.isna().sum())

# Ordenar los datos por cantidad de datos
con_paralelizar_df = con_paralelizar_df.sort_values(by="cantidad_de_datos")

# Gráfico de Líneas con Subplots
plt.figure(figsize=(16, 12))
unique_nodos = con_paralelizar_df["nodos_threadpool"].unique()
for i, nodo in enumerate(unique_nodos):
    plt.subplot(len(unique_nodos), 1, i + 1)
    subset = con_paralelizar_df[con_paralelizar_df["nodos_threadpool"] == nodo]
    sns.lineplot(
        data=subset,
        x="cantidad_de_datos",
        y="tiempo_en_milisegundos",
        linewidth=2.5
    )
    plt.title(f"Tiempos de Ejecución Con Paralelización - {nodo} Nodos", fontsize=16)
    plt.xlabel("Cantidad de Datos", fontsize=12)
    plt.ylabel("Tiempo en Milisegundos", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()


# Gráfico de Cajas (Boxplot)
plt.figure(figsize=(13, 7))
sns.boxplot(
    data=con_paralelizar_df,
    x="nodos_threadpool",
    y="tiempo_en_milisegundos",
    palette="coolwarm"
)
plt.title("Distribución de Tiempos de Ejecución", fontsize=20)
plt.xlabel("Nodos Threadpool", fontsize=16)
plt.ylabel("Tiempo en Milisegundos", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.show()

# Calcular datos óptimos
optimal_data = con_paralelizar_df.groupby('nodos_threadpool').apply(
    lambda df: df[df['tiempo_en_milisegundos'] == df['tiempo_en_milisegundos'].min()]
).reset_index(drop=True)

print(optimal_data)
