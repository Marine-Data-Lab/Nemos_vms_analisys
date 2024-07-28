import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinterweb import HtmlFrame
import sqlite3
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Embarcaciones")

        # Conectar a la base de datos
        self.conn = sqlite3.connect('flota_nemo.db')

        # Crear la interfaz de usuario
        self.create_widgets()

        # Configurar valores predeterminados
        self.configurar_valores_predeterminados()

    def create_widgets(self):
        # Nombre de la embarcación
        self.lbl_name = ttk.Label(self.root, text="Nombre de la Embarcación:")
        self.lbl_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_name = ttk.Combobox(self.root)
        self.combo_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Botón para ejecutar la consulta
        self.btn_query = ttk.Button(self.root, text="Ejecutar Consulta", command=self.execute_query)
        self.btn_query.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        # Frame para el mapa
        self.map_frame = HtmlFrame(self.root, messages_enabled=False)
        self.map_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    def configurar_valores_predeterminados(self):
        cursor = self.conn.cursor()

        # Obtener nombres de las embarcaciones
        cursor.execute("SELECT DISTINCT Nombre_Embarcacion FROM datos_flota")
        nombres_embarcaciones = [row[0] for row in cursor.fetchall()]
        self.combo_name['values'] = nombres_embarcaciones
        if nombres_embarcaciones:
            self.combo_name.set(nombres_embarcaciones[0])

        # Inicializar el mapa sin puntos
        self.visualizar_mapa(pd.DataFrame())

    def execute_query(self):
        name = self.combo_name.get()

        # Validar entrada
        if not name:
            messagebox.showerror("Error", "El campo de nombre de embarcación es obligatorio.")
            return

        query = """
        SELECT *
        FROM datos_flota
        WHERE Nombre_Embarcacion = ?
        """
        params = (name,)

        try:
            df = pd.read_sql_query(query, self.conn, params=params)
            if df.empty:
                messagebox.showinfo("Sin Resultados", "No se encontraron datos para la embarcación especificada.")
            else:
                self.visualizar_mapa(df)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualizar_mapa(self, df):
        if df.empty:
            m = folium.Map(location=[20, -90], zoom_start=5)
        else:
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitud, df.Latitud))
            m = folium.Map(location=[gdf.Latitud.mean(), gdf.Longitud.mean()], zoom_start=10)
            marker_cluster = MarkerCluster().add_to(m)

            for idx, row in gdf.iterrows():
                folium.Marker(location=[row['Latitud'], row['Longitud']],
                              popup=f"{row['Fecha_Hora']} - {row['Nombre_Embarcacion']}").add_to(marker_cluster)

        mapa_path = os.path.abspath('mapa.html')
        m.save(mapa_path)
        self.map_frame.load_url(f'file://{mapa_path}')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = App(root)
    root.mainloop()
