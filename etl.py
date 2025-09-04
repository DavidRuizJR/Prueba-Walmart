import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configuración de conexión (cambia si usas otras credenciales)
DB_URL = "postgresql+psycopg2://user:walmart@localhost:5432/universidad"
engine = create_engine(DB_URL)

# Definición de tablas
DDL = """
CREATE TABLE IF NOT EXISTS asignatura (
    asignatura_id INT PRIMARY KEY,
    nombre TEXT NOT NULL,
    semestre INT NOT NULL
);

CREATE TABLE IF NOT EXISTS estudiante (
    numero_cuenta INT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inscripcion (
    curso_id INT PRIMARY KEY,
    calificacion DECIMAL(4,2),
    num_cuenta INT NOT NULL,
    asignatura_id INT NOT NULL,
    FOREIGN KEY (num_cuenta) REFERENCES estudiante (numero_cuenta),
    FOREIGN KEY (asignatura_id) REFERENCES asignatura (asignatura_id)
);
"""

def crear_tablas():
    with engine.connect() as conn:
        conn.execute(text(DDL))
        conn.commit()
    logging.info("Tablas creadas/verificadas.")

def validar_dataframe(df, pk_col, nombre_tabla, columnas_esperadas):
    # Validar columnas esperadas
    if set(df.columns) != set(columnas_esperadas.keys()):
        raise ValueError(
            f"{nombre_tabla}: columnas no coinciden.\n"
            f"Esperadas: {list(columnas_esperadas.keys())}\n"
            f"Recibidas: {list(df.columns)}"
        )

    # Renombrar columnas
    df = df.rename(columns=columnas_esperadas)

    # Reordenar columnas
    df = df[list(columnas_esperadas.values())]

    # Validar PK
    if df[pk_col].isnull().any():
        raise ValueError(f"{nombre_tabla}: hay valores nulos en la PK {pk_col}")
    if df[pk_col].duplicated().any():
        raise ValueError(f"{nombre_tabla}: hay duplicados en la PK {pk_col}")

    logging.info(f"{nombre_tabla}: validación y renombrado OK.")
    return df

def cargar_datos():
    # Leer CSVs
    df_asignatura = pd.read_csv(r"csv/asignaturas.csv")
    df_estudiante = pd.read_csv(r"csv/estudiantes.csv")
    df_inscripcion = pd.read_csv(r"csv/inscripcion.csv")

    # Validar y normalizar columnas
    df_asignatura = validar_dataframe(
        df_asignatura,
        pk_col="asignatura_id",
        nombre_tabla="asignatura",
        columnas_esperadas={
            "asignatura_id": "asignatura_id",
            "nombre": "nombre",
            "Semestre": "semestre"
        }
    )

    df_estudiante = validar_dataframe(
        df_estudiante,
        pk_col="numero_cuenta",
        nombre_tabla="estudiante",
        columnas_esperadas={
            "numero_cuenta": "numero_cuenta",
            "nombre": "nombre"
        }
    )

    df_inscripcion = validar_dataframe(
        df_inscripcion,
        pk_col="curso_id",
        nombre_tabla="inscripcion",
        columnas_esperadas={
            "curso_id": "curso_id",
            "calificacion": "calificacion",
            "num_cuenta": "num_cuenta",
            "asignatura_id": "asignatura_id"
        }
    )

    # Insertar
    df_asignatura.to_sql("asignatura", engine, if_exists="append", index=False)
    df_estudiante.to_sql("estudiante", engine, if_exists="append", index=False)
    df_inscripcion.to_sql("inscripcion", engine, if_exists="append", index=False)

    logging.info("Datos cargados exitosamente.")

if __name__ == "__main__":
    try:
        crear_tablas()
        cargar_datos()
    except Exception as e:
        logging.error(f"Error en la carga: {e}")
