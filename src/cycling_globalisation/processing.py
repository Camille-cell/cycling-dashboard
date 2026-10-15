from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "cycling_rankings_by_year.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "yearly"
YEARS = [2024, 2020, 2000, 1980, 1960, 1940, 1920, 1910]
OLD_COUNTRIES = ["France", "Germany", "Italy", "Spain", "Belgium"]


def process_rankings(input_path=INPUT_PATH, output_dir=OUTPUT_DIR):
    """Aggregate ranking points by country and save one CSV per year."""
    df = pd.read_csv(input_path)
    start_indices = df.index[df["ranking"] == 1].tolist()
    start_indices.append(len(df))
    segments = len(start_indices) - 1

    if segments != len(YEARS):
        raise ValueError(
            f"Expected {len(YEARS)} yearly ranking segments, found {segments} "
            f"in {input_path}."
        )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []

    for index, year in enumerate(YEARS):
        segment_df = df.iloc[start_indices[index]:start_indices[index + 1]]
        country_points = segment_df.groupby("country")["points"].sum().reset_index()
        country_points["Type"] = np.where(
            country_points["country"].isin(OLD_COUNTRIES),
            "Old Country",
            "New Country",
        )
        output_path = output_dir / f"clean_data_peryear{year}.csv"
        country_points.to_csv(output_path, index=False)
        outputs.append(output_path)

    return outputs


if __name__ == "__main__":
    for output_path in process_rankings():
        print(f"Saved {output_path}")