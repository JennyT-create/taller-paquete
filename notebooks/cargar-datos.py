# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # Cargar los datos
# MAGIC
# MAGIC Córrelo **una sola vez**: conéctalo a *Serverless* y pulsa *Run all*. Deja el dataset del libro en tu
# MAGIC catálogo, en `/Volumes/mlops_dev/hotel_booking/datos/booking.csv`, y te muestra cómo es.
# MAGIC
# MAGIC Los datos no van a Git: viven en el catálogo de Databricks. Este notebook los baja de su fuente pública, el
# MAGIC repositorio del libro en GitHub. Si lo corres otra vez, no duplica nada: vuelve a bajar el archivo y lo
# MAGIC reemplaza.

# COMMAND ----------

import urllib.request

import pandas as pd

# Los mismos nombres que usa project_config.yml para el entorno dev
CATALOGO = "mlops_dev"
ESQUEMA = "hotel_booking"
VOLUMEN = "datos"
RUTA = f"/Volumes/{CATALOGO}/{ESQUEMA}/{VOLUMEN}/booking.csv"

FUENTE = (
    "https://raw.githubusercontent.com/mvechtomova/oreilly-mlops-with-databricks/"
    "main/mlops/data/booking.csv"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Preparar el lugar en el catálogo
# MAGIC
# MAGIC El catálogo de Databricks tiene tres niveles: **catálogo** → **esquema** → lo que guardes adentro. Un
# MAGIC **volumen** es como una carpeta dentro del esquema, hecha para guardar archivos tal cual, como este CSV.
# MAGIC `IF NOT EXISTS` evita que falle si ya existe.

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOGO}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{ESQUEMA}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOGO}.{ESQUEMA}.{VOLUMEN}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Bajar el archivo y guardarlo en el volumen

# COMMAND ----------

with urllib.request.urlopen(FUENTE, timeout=60) as respuesta:
    contenido = respuesta.read()

with open(RUTA, "wb") as archivo:
    archivo.write(contenido)

print(f"Guardado en {RUTA}: {len(contenido):,} bytes")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Mirar los datos

# COMMAND ----------

df = pd.read_csv(RUTA)
print(f"{len(df):,} reservas y {len(df.columns)} columnas")
display(df.head(10))

# COMMAND ----------

# MAGIC %md
# MAGIC Cada fila es **una reserva** de un hotel. Lo que queremos predecir es `average price`: el precio
# MAGIC promedio por noche.
# MAGIC
# MAGIC | Columna | Qué es |
# MAGIC |---|---|
# MAGIC | `Booking_ID` | Identificador de la reserva. No sirve para predecir |
# MAGIC | `number of adults`, `number of children` | Cuántos adultos y niños |
# MAGIC | `number of weekend nights`, `number of week nights` | Noches de fin de semana y entre semana |
# MAGIC | `type of meal` | Plan de comidas: `Meal Plan 1`, `2`, `3` o `Not Selected` |
# MAGIC | `car parking space` | Si pidió estacionamiento (1) o no (0) |
# MAGIC | `room type` | Tipo de habitación, de `Room_Type 1` a `7` |
# MAGIC | `lead time` | Días entre la reserva y la llegada |
# MAGIC | `market segment type` | Por dónde llegó: `Online`, `Offline`, `Corporate`, `Complementary`, `Aviation` |
# MAGIC | `repeated` | Si el huésped ya había venido antes (1) o no (0) |
# MAGIC | `P-C`, `P-not-C` | Reservas anteriores del huésped canceladas y no canceladas |
# MAGIC | `average price` | **Lo que queremos predecir:** precio promedio por noche |
# MAGIC | `special requests` | Cuántos pedidos especiales hizo |
# MAGIC | `date of reservation` | Fecha en que se hizo la reserva, como mes/día/año |
# MAGIC | `booking status` | Si se canceló o no. El dataset original es para predecir esto; el libro usa el precio |
# MAGIC
# MAGIC Dos cosas que verás en el código:
# MAGIC
# MAGIC - Los nombres tienen espacios y guiones. `clean_column_names`, en el paquete, los cambia por `_`
# MAGIC   (`lead time` → `lead_time`).
# MAGIC - En `date of reservation` hay 37 filas con `2018-2-29`: una fecha que no existe (2018 no fue bisiesto) y
# MAGIC   que además viene en otro formato. Por eso el código la corrige antes de convertir la columna a fecha.

# COMMAND ----------

display(df[df["date of reservation"] == "2018-2-29"].head())

# COMMAND ----------

# MAGIC %md
# MAGIC Fuente: dataset *Hotel Booking Cancellation Prediction*, publicado en Kaggle por Youssef Aboelwafa
# MAGIC (`kaggle.com/datasets/youssefaboelwafa/hotel-booking-cancellation-prediction`), tal como lo usa el libro
# MAGIC *MLOps with Databricks*.