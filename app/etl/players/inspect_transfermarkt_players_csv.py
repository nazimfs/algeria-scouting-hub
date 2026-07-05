import pandas as pd
from pathlib import Path


CSV_PATH = Path("data/external/transfermarkt/players.csv")
GZIP_PATH = Path("data/external/transfermarkt/players.csv.gz")


def main() -> None:
    if CSV_PATH.exists():
        path = CSV_PATH
    elif GZIP_PATH.exists():
        path = GZIP_PATH
    else:
        raise FileNotFoundError(
            "players.csv or players.csv.gz not found in data/external/transfermarkt"
        )

    df = pd.read_csv(path)

    print("=" * 80)
    print(f"File loaded: {path}")
    print("=" * 80)

    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nShape:")
    print(df.shape)

    print("\nFirst rows:")
    print(df.head(10).to_string())

    print("\nNull counts:")
    print(df.isna().sum().sort_values(ascending=False).head(20))


if __name__ == "__main__":
    main()