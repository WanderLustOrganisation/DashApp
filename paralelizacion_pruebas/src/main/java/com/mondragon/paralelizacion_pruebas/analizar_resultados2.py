import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el archivo CSV
con_paralelizar_df = pd.read_csv("C:/Users/julga/Documents/MU/23-24/wanderlust/Web/paralelizacion_pruebas/paralelizar_promedio.csv")

# Ordenar los datos por cantidad de datos
con_paralelizar_df = con_paralelizar_df.sort_values(by="cantidad_de_datos")

# Configurar el tamaño de la figura
plt.figure(figsize=(13, 7))

# Gráfico para tiempos con paralelización
sns.lineplot(
    data=con_paralelizar_df,
    x="cantidad_de_datos",
    y="tiempo_en_milisegundos",
    hue="nodos_threadpool",
    palette="coolwarm",
    linewidth=2.5
)

# Personalizar el gráfico
plt.title("Tiempos de Ejecución Con Paralelización", fontsize=20)
plt.xlabel("Cantidad de Datos", fontsize=16)
plt.ylabel("Tiempo en Milisegundos", fontsize=16)
plt.legend(title="Nodos Threadpool", title_fontsize='13', fontsize='11')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Mostrar el gráfico
plt.tight_layout()
plt.show()