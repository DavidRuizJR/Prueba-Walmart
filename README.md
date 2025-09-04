# Proyecto Data Engineer - Prueba Técnica

Este repositorio contiene la prueba técnica para el puesto de Data Engineer.  
Incluye la carga de datos desde CSVs a PostgreSQL, consultas SQL para análisis y generación de reportes en CSV.

---

## Contenido del repositorio

- `etl.py` → Script para crear tablas y cargar los CSVs en la base de datos.
- `ejercicios.py` → Script que realiza los ejercicios solicitados:
  1. Calificaciones más altas y comparación con promedio.
  2. Porcentaje de avance de créditos y generación de top/bottom 10.
- `asignatura.csv`, `estudiante.csv`, `inscripcion.csv` → Archivos de entrada.
- `requirements.txt` → Dependencias de Python.
- `.gitignore` → Ignora archivos temporales y entorno virtual.
- `Dockerfile` o `docker-compose.yml` → Opcional, para levantar PostgreSQL fácilmente.

---

## Requisitos

- Python 3.9+  
- PostgreSQL 12+  
- Librerías Python: `pandas`, `sqlalchemy`, `psycopg2-binary`  

Instalar dependencias:

```bash
pip install -r requirements.txt
