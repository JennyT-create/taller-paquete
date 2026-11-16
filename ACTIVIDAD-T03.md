# Código para la actividad práctica de T03

Copia el código desde aquí, no desde el PDF: al copiar desde un PDF se pierde la sangría, y en Python la sangría
importa. Los pasos completos están en la hoja de la actividad práctica.

## Tarea 2.2: la prueba

En `tests/test_preprocessing.py`, reemplaza la línea del import por esta:

```python
from hotel_booking.preprocessing import add_arrival_month, clean_column_names
```

Y agrega esta prueba al final del archivo:

```python
def test_add_arrival_month() -> None:
    df = pd.DataFrame(
        {"date_of_reservation": ["1/15/2018", "2018-2-29"], "lead_time": [20, 0]}
    )

    result = add_arrival_month(df)

    assert list(result["arrival_month"]) == [2, 3]
```

## Tarea 2.3: el punto de partida de la función

Agrega esto al final de `src/hotel_booking/preprocessing.py` y complétalo con la lógica de la última celda de
cálculo de `notebooks/preprocesamiento.py`:

```python
def add_arrival_month(df):
    df = df.copy()
    # Aquí va la lógica del notebook: corregir la fecha 2018-2-29,
    # convertirla a fecha, sumar el lead_time y sacar el mes.
    return df
```
