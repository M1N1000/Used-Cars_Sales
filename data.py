import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/used_car_sales.csv")
print(df.shape)
df.info()

# duplikaty
print("Duplikaty wierszy:", df.duplicated().sum())
print("Unikalne ID:", df["ID"].nunique(), "z", len(df))

# statystyki liczbowe
print(df.describe().T)

# kolumny kategorialne
for col in ["Car Sale Status", "Gearbox", "Energy", "Car Type", "Manufacturer Name"]:
    print("\n", col)
    print(df[col].value_counts())

# daty
df["Purchased Date"] = pd.to_datetime(df["Purchased Date"], errors="coerce")
df["Sold Date"] = pd.to_datetime(df["Sold Date"], errors="coerce")
print("\nNieparsowalne daty:", df["Purchased Date"].isna().sum(), df["Sold Date"].isna().sum())
print("Sprzedaż przed zakupem:", (df["Sold Date"] < df["Purchased Date"]).sum())

df = df.drop(columns="margin_check", errors="ignore")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# pełne statystyki liczbowe, bez ucinania
print(df.describe().T)

sold = df[df["Car Sale Status"] == "Sold"]
unsold = df[df["Car Sale Status"] == "Un Sold"]

# jak wyglądają daty sprzedaży dla niesprzedanych
print("\nSold Date dla niesprzedanych:")
print(unsold["Sold Date"].value_counts().head())
print(unsold[["Sold Price-$", "Margin-%", "Sales Commission-$", "Sales Rating"]].describe().T)

# sprzedane auta z datą sprzedaży przed zakupem
bad = sold[sold["Sold Date"] < sold["Purchased Date"]]
print("\nSprzedane przed zakupem:", len(bad))
print(bad[["ID", "Purchased Date", "Sold Date"]].head())

# zakres dat i marża wśród sprzedanych
print("\nZakres Purchased Date:", df["Purchased Date"].min(), df["Purchased Date"].max())
print("Zakres Sold Date (sprzedane):", sold["Sold Date"].min(), sold["Sold Date"].max())
print("\nMarża (sprzedane):")
print(sold["Margin-%"].describe())
print("Sprzedane ze stratą:", (sold["Margin-%"] < 0).sum())