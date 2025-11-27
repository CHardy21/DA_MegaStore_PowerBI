import pandas as pd

def generar_calendar(df_ordenes):
    fechas = pd.date_range(
        start=df_ordenes["OrderDate"].min(),
        end=df_ordenes["OrderDate"].max(),
        freq="D"
    )
    calendar = pd.DataFrame({"Date": fechas})
    calendar["Year"] = calendar["Date"].dt.year
    calendar["Month"] = calendar["Date"].dt.month
    calendar["MonthName"] = calendar["Date"].dt.strftime("%B")
    calendar["Quarter"] = "Q" + calendar["Date"].dt.quarter.astype(str)
    calendar["WeekOfYear"] = calendar["Date"].dt.isocalendar().week
    calendar["Day"] = calendar["Date"].dt.day
    calendar["DayName"] = calendar["Date"].dt.strftime("%A")
    return calendar
