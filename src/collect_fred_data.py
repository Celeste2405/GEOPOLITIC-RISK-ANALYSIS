
import pandas as pd
from pathlib import Path

START = "2000-01-01"
END = "2025-12-31"

SERIES = {
    "FEDFUNDS": "fed_effective_rate",
    "ECBDFR": "ecb_deposit_rate",
    "DCOILBRENTEU": "brent_usd",
    "DCOILWTICO": "wti_usd",
    "IRLTLT01FRM156N": "yield_10y_fra",
    "IRLTLT01DEM156N": "yield_10y_deu",
    "IRLTLT01ITM156N": "yield_10y_ita",
    "IRLTLT01ESM156N": "yield_10y_esp",
    "IRLTLT01USM156N": "yield_10y_usa",
}

def fetch_fred(series_id, name):
    url = (
        "https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}"
    )

    df = pd.read_csv(url)

    df.columns = ["date", name]
    df["date"] = pd.to_datetime(df["date"])
    df[name] = pd.to_numeric(
        df[name], errors="coerce"
    )

    return df.set_index("date")[[name]]

# Télécharger et assembler les séries
frames = [
    fetch_fred(series_id, name)
    for series_id, name in SERIES.items()
]

data = pd.concat(frames, axis=1)
data = data.loc[START:END].sort_index()

# Convertir les observations en fréquence mensuelle
# Moyenne des observations disponibles dans le mois
monthly = data.resample("MS").mean()

# Spreads souverains en points de pourcentage
for country in ["fra", "ita", "esp"]:
    monthly[f"spread_10y_{country}_deu"] = (
        monthly[f"yield_10y_{country}"]
        - monthly["yield_10y_deu"]
    )

# Variables additionnelles : variation annuelle
monthly["brent_yoy_pct"] = (
    monthly["brent_usd"].pct_change(12) * 100
)

monthly["wti_yoy_pct"] = (
    monthly["wti_usd"].pct_change(12) * 100
)

monthly.index.name = "date"

# Export
Path("data/raw").mkdir(parents=True, exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)

data.to_csv("data/raw/fred_daily_monthly.csv")
monthly.to_csv("data/processed/fred_monthly.csv")

print(monthly.tail())
print("\nValeurs manquantes :")
print(monthly.isna().sum())
