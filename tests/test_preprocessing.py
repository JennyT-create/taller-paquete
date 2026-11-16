import pandas as pd

from hotel_booking.preprocessing import clean_column_names


def test_clean_column_names() -> None:
    df = pd.DataFrame(columns=["lead time", "room-type", "Booking_ID"])

    result = clean_column_names(df)

    assert list(result.columns) == ["lead_time", "room_type", "Booking_ID"]
