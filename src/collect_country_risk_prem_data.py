
import pandas as pd
import requests
from pathlib import Path

url = (
    "https://www.stern.nyu.edu/~adamodar/"
    "pc/datasets/ctryprem.xlsx"
)

raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

file_path = raw_dir / "damodaran_ctryprem.xlsx"

response = requests.get(url, timeout=30)
response.raise_for_status()
file_path.write_bytes(response.content)

# Inspecter les feuilles du classeur
xls = pd.ExcelFile(file_path)

print("Feuilles disponibles :", xls.sheet_names)

for sheet in xls.sheet_names:
    print(f"\n--- {sheet} ---")
    preview = pd.read_excel(
        file_path,
        sheet_name=sheet,
        header=None,
        nrows=12
    )
    print(preview.to_string(index=False, header=False))


print(preview.head(10))