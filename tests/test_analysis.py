"""
Unit tests for analysis.py
"""


import sys, os

# Ensure project root is on sys.path so import analysis works reliably when pytest runs from different working directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from analysis import compute_summary, compute_match_metrics

# Verify compute_match_metrics returns correct percentages for a single match 
def test_compute_match_metrics_basic():
    row = pd.Series({
        "first_serve_in": 40, "first_serve_total": 50,
        "first_serve_points_won": 30, "first_serve_points_total": 40,
        "second_serve_points_won": 10, "second_serve_points_total": 20,
        "break_points_saved": 6, "break_points_faced": 8
    })
    m = compute_match_metrics(row)

    # Use tolerance for floats
    assert abs(m["first_serve_pct"] - 0.8) < 1e-9
    assert abs(m["first_serve_pts_won_pct"] - 0.75) < 1e-9
    assert abs(m["second_serve_pts_won_pct"] - 0.5) < 1e-9
    assert abs(m["break_points_saved_pct"] - 0.75) < 1e-9

# Verify compute_summary counts match, wins, losses correctly and computes a win rate
def test_compute_summary_counts_and_rates():
    df = pd.DataFrame([
        {"result":"W","aces":5,"double_faults":1,"first_serve_in":40,"first_serve_total":50,
         "first_serve_points_won":30,"first_serve_points_total":40,
         "second_serve_points_won":10,"second_serve_points_total":20,
         "break_points_saved":6,"break_points_faced":8},
        {"result":"L","aces":1,"double_faults":3,"first_serve_in":30,"first_serve_total":60,
         "first_serve_points_won":18,"first_serve_points_total":30,
         "second_serve_points_won":12,"second_serve_points_total":30,
         "break_points_saved":2,"break_points_faced":6},
    ])
    s = compute_summary(df)
    assert s.matches == 2
    assert s.wins == 1
    assert s.losses == 1
    assert abs(s.win_rate - 0.5) < 1e-9
