# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # Preprocesamiento: la versión "antes"
# MAGIC
# MAGIC Así se ve un notebook típico de experimentación: todo junto, valores
# MAGIC escritos a mano y nada que se pueda probar por separado. En T03 llevamos
# MAGIC este código al paquete `hotel_booking`, paso a paso.
# MAGIC
# MAGIC Antes de correrlo, corre una vez el notebook `cargar-datos`: deja los datos en tu catálogo.

# COMMAND ----------

from datetime import datetime

import pandas as pd

# COMMAND ----------

# Valores escritos a mano: si cambian, hay que buscarlos en el código
CATALOG = "mlops_dev"
SCHEMA = "hotel_booking"
TARGET = "average_price"

# COMMAND ----------

df = pd.read_csv(f"/Volumes/{CATALOG}/{SCHEMA}/datos/booking.csv")

# Nombres de columna sin espacios ni guiones (ya está en el paquete: clean_column_names)
df.columns = df.columns.str.replace(r"[ -]", "_", regex=True)

# COMMAND ----------

# Mes de llegada (la tarea 2 de la actividad práctica lo lleva al paquete)
df["date_of_reservation"] = df["date_of_reservation"].apply(
    lambda x: "3/1/2018" if x == "2018-2-29" else x
)
df["date_of_reservation"] = df["date_of_reservation"].apply(
    lambda x: datetime.strptime(x, "%m/%d/%Y")
)
df["arrival_date"] = df["date_of_reservation"] + pd.to_timedelta(
    df["lead_time"], unit="d"
)
df["arrival_month"] = df["arrival_date"].dt.month

# COMMAND ----------

df.head()