import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#sin_paralelizar_df = pd.read_csv("C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/promedio_tiempos_tipo2.csv")
con_paralelizar_df = pd.read_csv("C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/promedio_tiempos_tipo1.csv")

#sin_paralelizar_df = sin_paralelizar_df.sort_values(by="cantidad_de_datos")
con_paralelizar_df = con_paralelizar_df.sort_values(by="cantidad_de_datos")

plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
sns.lineplot(
    data=sin_paralelizar_df,
    x="cantidad_de_datos",
    y="tiempo_en_milisegundos",
    label="Sin Paralelizar",
)
plt.title("Tiempos de ejecución sin paralelizar")
plt.title("Tiempos de Ejecución Sin Paralelizar")
plt.xlabel("Cantidad de Datos")
plt.ylabel("Tiempo en Milisegundos")

# Gráfico para tiempos con paralelización
plt.subplot(1, 2, 2)
sns.lineplot(
    data=con_paralelizar_df,
    x="cantidad_de_datos",
    y="tiempo_en_milisegundos",
    hue="nodos_threadpool",
    palette="viridis",
)
plt.title("Tiempos de Ejecución Con Paralelización")
plt.xlabel("Cantidad de Datos")
plt.ylabel("Tiempo en Milisegundos")

# Mostrar gráficos
plt.tight_layout()
plt.show()

# Comparación de ambos métodos
plt.figure(figsize=(14, 7))
sns.lineplot(
    data=sin_paralelizar_df,
    x="cantidad_de_datos",
    y="tiempo_en_milisegundos",
    label="Sin Paralelizar",
)
sns.lineplot(
    data=con_paralelizar_df,
    x="cantidad_de_datos",
    y="tiempo_en_milisegundos",
    hue="nodos_threadpool",
    palette="viridis",
)
plt.title("Comparación de Tiempos de Ejecución")
plt.xlabel("Cantidad de Datos")
plt.ylabel("Tiempo en Milisegundos")
plt.legend()
plt.show()