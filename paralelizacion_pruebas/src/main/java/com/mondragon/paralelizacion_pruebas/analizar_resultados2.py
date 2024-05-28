import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

con_paralelizar_df = pd.read_csv("C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/promedio_tiempos_tipo1.csv")

con_paralelizar_df = con_paralelizar_df.sort_values(by="cantidad_de_datos")

plt.figure(figsize=(14, 7))

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