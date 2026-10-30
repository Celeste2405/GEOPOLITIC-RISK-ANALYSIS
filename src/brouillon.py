
from pathlib import Path
import pandas as pd

fred_path = Path("data/processed/fred_monthly.csv")

# Si le notebook est dans notebooks/
if not fred_path.exists():
    fred_path = Path("../data/processed/fred_monthly.csv")

fred = pd.read_csv(fred_path)

print("Dimensions :", fred.shape)
print("\nColonnes exactes :")
for col in fred.columns:
    print(repr(col))

print("\nPremières observations :")
print(fred.head(3).to_string(index=False))
