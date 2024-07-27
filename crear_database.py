import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('flota_nemo.db')
cursor = conn.cursor()

# Crear la tabla con las columnas adecuadas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS datos_flota (
        ID_Unico TEXT,
        Nombre_Embarcacion TEXT,
        Fecha_Hora DATETIME,
        Longitud REAL,
        Latitud REAL,
        Velocidad REAL,
        Rumbo REAL,
        PRIMARY KEY (ID_Unico, Fecha_Hora)
    )
''')

# Si planeas hacer muchas consultas por Fecha_Hora o ID_Unico, considera añadir índices
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fecha_hora ON datos_flota (Fecha_Hora)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_id_unico ON datos_flota (ID_Unico)')

# Guardar los cambios y cerrar la conexión a la base de datos
conn.commit()
conn.close()

print("Base de datos creada y tabla configurada con índices optimizados para consultas.")
