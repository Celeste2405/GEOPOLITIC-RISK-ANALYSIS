"""Construct the monthly AI-GPR / FRED country panel (2000–2025).

Run from the project root:
    python src/build_financial_panel.py

Or specify a project root:
    python src/build_financial_panel.py --project-root /path/to/project
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd

COUNTRIES = ("DEU", "ESP", "FRA", "ITA", "USA")
YIELD_COLS = {country: f"yield_10y_{country.lower()}" for country in COUNTRIES}
SPREAD_COLS = {
    "FRA": "spread_10y_fra_deu",
    "ITA": "spread_10y_ita_deu",
    "ESP": "spread_10y_esp_deu",
}
REQUIRED_GPR = {
    "date", "country", "gpr_country", "gpr_global",
    "gpr_initiator", "gpr_respondent", "gpr_spillover",
}
REQUIRED_FRED = {
    "date", "fed_effective_rate", "ecb_deposit_rate",
    "brent_usd", "wti_usd", "brent_yoy_pct", "wti_yoy_pct",
    *YIELD_COLS.values(), *SPREAD_COLS.values(),
}


def normalize_dates(df: pd.DataFrame, name: str) -> pd.DataFrame:
    if "date" not in df.columns:
        raise ValueError(f"{name}: colonne 'date' absente")
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="raise").dt.to_period("M").dt.to_timestamp()
    return df


def build_panel(root: Path) -> pd.DataFrame:
    processed = root / "data" / "processed"
    gpr_path = processed / "ai_gpr_country_monthly.csv"
    fred_path = processed / "fred_monthly.csv"
    for path in (gpr_path, fred_path):
        if not path.is_file():
            raise FileNotFoundError(f"Fichier introuvable : {path}")

    gpr = normalize_dates(pd.read_csv(gpr_path), "AI-GPR")
    fred = normalize_dates(pd.read_csv(fred_path), "FRED")
    for name, df, required in (("AI-GPR", gpr, REQUIRED_GPR), ("FRED", fred, REQUIRED_FRED)):
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"{name}: colonnes manquantes : {sorted(missing)}")

    gpr = gpr.loc[gpr["country"].isin(COUNTRIES) & gpr["date"].between("2000-01-01", "2025-12-01")].copy()
    fred = fred.loc[fred["date"].between("2000-01-01", "2025-12-01")].copy()
    if gpr.duplicated(["country", "date"]).any():
        raise ValueError("AI-GPR : doublons pays-mois")
    if fred.duplicated(["date"]).any():
        raise ValueError("FRED : doublons mensuels")
    if len(gpr) != 1560 or gpr.groupby("country")["date"].nunique().to_dict() != dict.fromkeys(COUNTRIES, 312):
        raise ValueError("AI-GPR : panel incomplet (attendu : 312 mois par pays)")

    for col in fred.columns.difference(["date"]):
        fred[col] = pd.to_numeric(fred[col], errors="coerce")
    panel = gpr.merge(fred, on="date", how="left", validate="many_to_one", indicator=True)
    if not panel["_merge"].eq("both").all():
        missing_dates = panel.loc[panel["_merge"] != "both", "date"].dt.strftime("%Y-%m").unique().tolist()
        raise ValueError(f"Dates sans correspondance FRED : {missing_dates}")
    panel.drop(columns="_merge", inplace=True)

    # Harmonized country-specific 10-year government yield.
    panel["yield_10y"] = np.nan
    for country, col in YIELD_COLS.items():
        mask = panel["country"].eq(country)
        panel.loc[mask, "yield_10y"] = panel.loc[mask, col].to_numpy()

    # ECB deposit facility rate for euro area, Fed effective rate for USA.
    # These are different monetary-policy instruments, so interpret accordingly.
    panel["policy_rate"] = np.where(
        panel["country"].eq("USA"),
        panel["fed_effective_rate"],
        panel["ecb_deposit_rate"],
    )

    # Spreads against German 10Y yields: only meaningful here for euro-area peers.
    panel["spread_10y_de_pp"] = np.nan
    deu = panel["country"].eq("DEU")
    panel.loc[deu, "spread_10y_de_pp"] = np.where(
        panel.loc[deu, "yield_10y"].notna(), 0.0, np.nan
    )
    for country, col in SPREAD_COLS.items():
        mask = panel["country"].eq(country)
        panel.loc[mask, "spread_10y_de_pp"] = panel.loc[mask, col].to_numpy()
    # USA: NaN by design, not a data-quality failure.

    panel = panel.sort_values(["country", "date"]).reset_index(drop=True)
    for col in ("yield_10y", "policy_rate"):
        if panel[col].isna().all():
            raise ValueError(f"Variable essentielle entièrement manquante : {col}")
        by_country = panel.groupby("country")[col].apply(lambda s: s.notna().sum())
        if (by_country == 0).any():
            raise ValueError(f"{col}: pays sans données : {by_country[by_country == 0].index.tolist()}")
    euro = panel["country"].ne("USA")
    if panel.loc[euro, "spread_10y_de_pp"].isna().all():
        raise ValueError("Spreads zone euro entièrement manquants")

    out = processed / "georisk_financial_panel.csv"
    panel.to_csv(out, index=False, date_format="%Y-%m-%d")
    print(f"Export : {out}")
    print(f"Dimensions : {panel.shape}")
    print("Observations par pays :\n", panel.groupby("country").size().to_string())
    print("Valeurs manquantes :\n", panel[["yield_10y", "policy_rate", "spread_10y_de_pp", "brent_yoy_pct", "wti_yoy_pct"]].isna().sum().to_string())
    print("Note : 312 spreads USA manquants par construction ; 12 premiers mois de variations YoY manquants par pays.")
    return panel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    build_panel(args.project_root.resolve())


if __name__ == "__main__":
    main()
