import pandas as pd
from sqlalchemy import create_engine,text
import logging

# -------------------- CONFIG --------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
DB_URL = "postgresql+psycopg2://user:walmart@localhost:5432/universidad"
engine = create_engine(DB_URL)

# -------------------- EJERCICIO 1 --------------------
def ejercicio1():
    logging.info("Ejecutando Ejercicio 1...")
    query = text("""
    WITH ranked AS (
        SELECT 
            i.curso_id,
            i.calificacion,
            i.num_cuenta,
            i.asignatura_id,
            AVG(i.calificacion) OVER (PARTITION BY i.asignatura_id) AS promedio
        FROM inscripcion i
    )
    SELECT 
        e.nombre AS nombre_alumno,
        a.nombre AS nombre_materia,
        r.calificacion,
        ROUND(r.promedio,2) AS calificacion_promedio,
        CASE WHEN r.calificacion > r.promedio THEN 1 ELSE 0 END AS bandera1
    FROM ranked r
    JOIN estudiante e ON r.num_cuenta = e.numero_cuenta
    JOIN asignatura a ON r.asignatura_id = a.asignatura_id
    WHERE r.calificacion > r.promedio
    ORDER BY a.nombre, r.calificacion DESC;
    """)
    df = pd.read_sql(query, engine)

    df.to_csv("csv_salida/alumnos_mayor_promedio.csv", index=False, encoding="utf-8")
    logging.info("CSV alumnos_mayor_promedio.csv generado.")

# -------------------- EJERCICIO 2 --------------------
def ejercicio2():
    logging.info("Ejecutando Ejercicio 2...")
    query2 = text("""
    WITH conteo AS (
    SELECT 
        e.numero_cuenta,
        e.nombre AS nombre_alumno,
        COUNT(DISTINCT i.asignatura_id) AS total_materias_cursadas,
        (SELECT COUNT(*) FROM asignatura) AS total_materias
    FROM estudiante e
    LEFT JOIN inscripcion i ON e.numero_cuenta = i.num_cuenta
    GROUP BY e.numero_cuenta, e.nombre
    )
    SELECT
        nombre_alumno,
        total_materias_cursadas,
        total_materias,
        ROUND((total_materias_cursadas::decimal / total_materias) * 100, 2) AS porcentaje_avance,
        CASE 
            WHEN (total_materias_cursadas::decimal / total_materias) * 100 = 100 THEN 5
            WHEN (total_materias_cursadas::decimal / total_materias) * 100 >= 80 THEN 4
            WHEN (total_materias_cursadas::decimal / total_materias) * 100 >= 65 THEN 3
            WHEN (total_materias_cursadas::decimal / total_materias) * 100 >= 40 THEN 2
            ELSE 1
        END AS bandera_clasificacion
    FROM conteo
    ORDER BY porcentaje_avance DESC
    """)
    df2 = pd.read_sql(query2, engine)

    # Top 10 (mayor avance)
    top10 = df2.nlargest(10, "porcentaje_avance")[["nombre_alumno"]]

    # Bottom 10 (menor avance)
    bottom10 = df2.nsmallest(10, "porcentaje_avance")[["nombre_alumno"]]

    top10.to_csv("csv_salida/top10_avance_creditos.csv", index=False, encoding="utf-8")
    bottom10.to_csv("csv_salida/bottom10_avance_creditos.csv", index=False, encoding="utf-8")
    logging.info("CSVs top10_avance_creditos.csv y bottom10_avance_creditos.csv generados.")

# -------------------- MAIN --------------------
if __name__ == "__main__":
    try:
        #ejercicio1()
        ejercicio2()
        logging.info("✅ Ejercicios completados correctamente.")
    except Exception as e:
        logging.error(f"Error en los ejercicios: {e}")
