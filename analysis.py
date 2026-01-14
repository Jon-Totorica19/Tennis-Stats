"""
Math logic for tennis stats tool
- Only contains data loading and calculations
- No CLI parsing and minimal printing to terminal
"""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import pandas as pd

# Summary metrics computed across all match data
@dataclass
class Summary:
    matches: int
    wins: int
    losses: int
    win_rate: float
    avg_aces: float
    avg_double_faults: float
    first_serve_pct: float
    first_serve_pts_won_pct: float
    second_serve_pts_won_pct: float
    break_points_saved_pct: float

# Helper method: Avoid ZeroDivisionError
def _safe_div(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0

# Load match data from a CSV to a DataFrame
def load_matches(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Parse date strings into datetime
    df["date"] = pd.to_datetime(df["date"], errors="raise")

    # Normalize results column to "W" or "L"
    df["result"] = df["result"].str.upper().str.strip()

    # Sort by date. Reset index to 0
    return df.sort_values("date").reset_index(drop=True)

# Compute metrics for a single match (one row)
def compute_match_metrics(row: pd.Series) -> Dict[str, float]:
    first_serve_pct = _safe_div(row["first_serve_in"], row["first_serve_total"])
    first_pts_won_pct = _safe_div(row["first_serve_points_won"], row["first_serve_points_total"])
    second_pts_won_pct = _safe_div(row["second_serve_points_won"], row["second_serve_points_total"])
    bp_saved_pct = _safe_div(row["break_points_saved"], row["break_points_faced"])
    return {
        "first_serve_pct": first_serve_pct,
        "first_serve_pts_won_pct": first_pts_won_pct,
        "second_serve_pts_won_pct": second_pts_won_pct,
        "break_points_saved_pct": bp_saved_pct,
    }

# Compute season wide metris across al matches in the DataFrame
def compute_summary(df: pd.DataFrame) -> Summary:
    matches = int(len(df))
    wins = int((df["result"] == "W").sum())
    losses = int((df["result"] == "L").sum())
    win_rate = _safe_div(wins, matches)

    # Per match averages
    avg_aces = float(df["aces"].mean()) if matches else 0.0
    avg_double_faults = float(df["double_faults"].mean()) if matches else 0.0

    # Calculate season percentages
    first_serve_pct = _safe_div(df["first_serve_in"].sum(), df["first_serve_total"].sum())
    first_pts_won_pct = _safe_div(df["first_serve_points_won"].sum(), df["first_serve_points_total"].sum())
    second_pts_won_pct = _safe_div(df["second_serve_points_won"].sum(), df["second_serve_points_total"].sum())
    bp_saved_pct = _safe_div(df["break_points_saved"].sum(), df["break_points_faced"].sum())

    return Summary(
        matches=matches,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        avg_aces=avg_aces,
        avg_double_faults=avg_double_faults,
        first_serve_pct=first_serve_pct,
        first_serve_pts_won_pct=first_pts_won_pct,
        second_serve_pts_won_pct=second_pts_won_pct,
        break_points_saved_pct=bp_saved_pct,
    )

# Find single match row statistics by exact date string (YYYY-MM-DD)
def find_match_by_date(df: pd.DataFrame, date_str: str) -> Optional[pd.Series]:
    d = pd.to_datetime(date_str)
    hit = df[df["date"] == d]
    if hit.empty:
        return None
    return hit.iloc[0]

# Write Summary object to a JSON file
def summary_to_json(summary: Summary, out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(asdict(summary), f, indent=2)
