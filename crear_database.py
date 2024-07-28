import sqlite3

def crear_conexion(db_file):
    """ Crear una conexión a la base de datos SQLite especificada por db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Conexión exitosa. SQLite DB version:", sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def crear_tabla(conn):
    """ Crear una tabla en la base de datos SQLite """
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_flota (
                ID_Unico TEXT,
                Nombre_Embarcacion TEXT,
                Ref_Posicion TEXT,
                Ref_Auxiliar TEXT,
                Longitud REAL,
                Latitud REAL,
                Fecha_Hora DATETIME,
                Fecha_Log DATETIME,
                Hora_Log DATETIME,
                Tipo_Marca TEXT,
                Subtipo_Marca TEXT,
                Guardar_Marca TEXT,
                Rumbo INTEGER,
                Rumbo_Promedio INTEGER,
                Velocidad REAL,
                Velocidad_Promedio REAL,
                Ref_Secundaria TEXT,
                Dispositivo TEXT,
                Retraso_Local INTEGER,
                Tipo_Dispositivo TEXT,
                Retraso_Promedio INTEGER,
                Retraso_Reporte INTEGER,
                ID_Zona INTEGER,
                Dia INTEGER,
                Mes INTEGER,
                Anio INTEGER,
                ID_Viaje INTEGER,
                Etapa_Viaje TEXT,
                Inicio_Viaje DATETIME,
                Fin_Viaje DATETIME,
                ID_Unico_Alterno TEXT,
                Detalle_Dispositivo TEXT,
                Inicio_Viaje_Detalle DATETIME,
                Fin_Viaje_Detalle DATETIME
            )
        ''')
        conn.commit()
        print("Tabla creada exitosamente")
    except sqlite3.Error as e:
        print(e)

def main():
    database = "flota_nemo.db"

    # Crear una conexión a la base de datos
    conn = crear_conexion(database)

    if conn is not None:
        # Crear la tabla
        crear_tabla(conn)
        # Cerrar la conexión a la base de datos
        conn.close()
    else:
        print("Error! No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()
