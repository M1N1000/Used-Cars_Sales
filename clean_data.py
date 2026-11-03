import numpy as np
import pandas as pd

df = pd.read_csv("data/used_car_sales.csv")

# 1. Czytelne nazwy kolumn (snake_case)
df.columns = (
    df.columns.str.strip().str.lower()
    .str.replace("-$", "_usd")
    .str.replace("-%", "_pct")
    .str.replace("-", "_")
    .str.replace(" ", "_")
)

# 2. Typy: daty i status
df["purchased_date"] = pd.to_datetime(df["purchased_date"])
df["sold_date"] = pd.to_datetime(df["sold_date"])
df["is_sold"] = df["car_sale_status"] == "Sold"

# 3. Niesprzedane auta: daty i kwoty zastępcze -> puste wartości
df[["sold_price_usd", "margin_pct", "sales_commission_usd"]] = df[
    ["sold_price_usd", "margin_pct", "sales_commission_usd"]
].astype("Int64")
df.loc[~df["is_sold"], "sold_date"] = pd.NaT
df.loc[~df["is_sold"], ["sold_price_usd", "margin_pct", "sales_commission_usd"]] = pd.NA

# 4. Flaga błędnych dat (sprzedaż przed zakupem) i czas sprzedaży
df["date_error"] = df["is_sold"] & (df["sold_date"] < df["purchased_date"])
df["days_to_sell"] = (df["sold_date"] - df["purchased_date"]).dt.days.astype("float")
df.loc[df["date_error"], "days_to_sell"] = np.nan

# 5. Wiek zapasu niesprzedanych aut względem ostatniej daty w danych
snapshot_date = df["sold_date"].max()
df["inventory_age_days"] = (snapshot_date - df["purchased_date"]).dt.days.astype("float")
df.loc[df["is_sold"], "inventory_age_days"] = np.nan

# 6. Kontrola spójności marży (tylko sprzedane)
sold = df[df["is_sold"]]
calc = (sold["sold_price_usd"] - sold["purchased_price_usd"]) / sold["purchased_price_usd"] * 100
print("Największa różnica marży (pp):", (calc - sold["margin_pct"]).abs().max())

# 7. Podsumowanie i zapis
print("Sprzedane:", df["is_sold"].sum(), "| Błędne daty:", df["date_error"].sum())
print("Snapshot:", snapshot_date.date())
print(df[["days_to_sell", "inventory_age_days"]].describe().T)

df.to_csv("data/used_car_sales_clean.csv", index=False)