from GoogleNews import GoogleNews
import pandas as pd

# Función para buscar eventos de derrame de petróleo
def buscar_eventos_derrame(palabras_clave, fecha_inicio, fecha_fin):
    gNews = GoogleNews(lang='es', region='MX')  # Idioma español, región México
    gNews.set_time_range(fecha_inicio, fecha_fin)  # Establecer el rango de fechas
    
    # Realizar la búsqueda
    gNews.search(palabras_clave)
    
    # Obtener los resultados
    result = gNews.result()
    
    return result

# Lista de palabras clave
palabras_clave_lista = [
    "derrame de petróleo sur del golfo de méxico",
    "derrame de crudo golfo de méxico",
    "accidente petrolero golfo de méxico",
    "fuga de petróleo golfo de méxico",
    "contaminación por petróleo golfo de méxico",
    "vertido de petróleo golfo de méxico",
    "derrame de aceite golfo de méxico",
    "desastre ecológico petróleo golfo de méxico",
    "derrame de hidrocarburos golfo de méxico",
    "accidente de plataforma petrolera golfo de méxico",
    "emergencia petrolera golfo de méxico"
]

# Parámetros de búsqueda
fecha_inicio = '01/01/2018'
fecha_fin = '12/31/2023'

# Inicializar un DataFrame vacío para acumular los resultados
resultados_totales = pd.DataFrame()

# Iterar a través de las palabras clave y buscar resultados
for palabras_clave in palabras_clave_lista:
    resultados = buscar_eventos_derrame(palabras_clave, fecha_inicio, fecha_fin)
    df = pd.DataFrame(resultados)
    resultados_totales = pd.concat([resultados_totales, df], ignore_index=True)

# Eliminar duplicados si los hubiera
resultados_totales.drop_duplicates(inplace=True)

# Guardar los resultados en un archivo CSV
resultados_totales.to_csv('resultados_derrame_news.csv', index=False)

# Mostrar los resultados
print(resultados_totales.head())