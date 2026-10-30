import requests
import pandas as pd

countries = ["FRA", "DEU", "ITA", "ESP", "USA"]

indicators = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation",
    "SL.UEM.TOTL.ZS": "unemployment",
    "NE.TRD.GNFS.ZS": "trade_pct_gdp",
}

def fetch_indicator(code, name):
    url = (
        "https://api.worldbank.org/v2/country/"
        f"{';'.join(countries)}/indicator/{code}"
    )

    response = requests.get(
        url,
        params={
            "format": "json",
            "date": "2000:2025",
            "per_page": 20000
        },
        timeout=30
    )
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Réponse inattendue : {code}")

    records = payload[1] or []

    return pd.DataFrame([
        {
            "country": item["countryiso3code"],
            "year": int(item["date"]),
            name: item["value"]
        }
        for item in records
        if item["countryiso3code"] in countries
    ])

frames = [
    fetch_indicator(code, name)
    for code, name in indicators.items()
]

macro = frames[0]

for frame in frames[1:]:
    macro = macro.merge(
        frame,
        on=["country", "year"],
        how="outer",
        validate="one_to_one"
    )

macro = macro.sort_values(["country", "year"])

macro.to_csv(
    "data/raw/macroeconomic_data.csv",
    index=False
)

print(macro.head())
