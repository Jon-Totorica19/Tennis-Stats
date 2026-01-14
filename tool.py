"""
Command Line Interface (CLI) for tennis stats tool

Example uses: 
    python tool.py summary tennis_stats.csv
    python tool.py match tennis_stats.csv --date 2025-10-08
    python tool.py plot tennis_stats.csv --metric first_serve_pct

"""


import argparse
import os
import matplotlib.pyplot as plt

from analysis import load_matches, compute_summary, find_match_by_date, compute_match_metrics, summary_to_json

# Allowed metrics for plotting

ALLOWED_METRICS = {
    "first_serve_pct",
    "first_serve_pts_won_pct",
    "second_serve_pts_won_pct",
    "break_points_saved_pct",
}

# Create/ensure results folder exsists before writing files
def ensure_results():
    os.makedirs("results", exist_ok=True)

# Summary command: Computes all matches summary and writes results/summary.json
def cmd_summary(args):
    ensure_results()

    # Load raw table
    df = load_matches(args.csv)

    # Compute all matches statistics
    s = compute_summary(df)

    # Save to JSON results file
    summary_path = os.path.join("results", "summary.json")
    summary_to_json(s, summary_path)

    # Print result summary to terminal
    print("=== Summary ===")
    print(f"Matches: {s.matches}  Wins: {s.wins}  Losses: {s.losses}  Win percentage: {s.win_rate:.3f}%")
    print(f"Average aces: {s.avg_aces:.2f}   Average double faults: {s.avg_double_faults:.2f}")
    print(f"1st serve in percentage: {s.first_serve_pct:.3f}%")
    print(f"1st serve points won percentage: {s.first_serve_pts_won_pct:.3f}%")
    print(f"2nd serve points won percentage: {s.second_serve_pts_won_pct:.3f}%")
    print(f"Break points saved percentage: {s.break_points_saved_pct:.3f}%")
    print(f"\nWrote: {summary_path}")

# Match command. Prints computed metrics for a single match date
def cmd_match(args):
    df = load_matches(args.csv)
    row = find_match_by_date(df, args.date)
    # Fail if date isnt found
    if row is None:
        raise SystemExit(f"No match found for date {args.date}. Try one from the CSV.")
    m = compute_match_metrics(row)

    print("=== Match ===")
    print(f"Date: {row['date'].date()}  Opponent: {row['opponent']}  Surface: {row['surface']}")
    print(f"Result: {row['result']}  Score: {row['score']}")
    print(f"Aces: {row['aces']}  Double Faults: {row['double_faults']}")
    print(f"1st serve in percentage: {m['first_serve_pct']:.3f}%")
    print(f"1st serve pts won percentage: {m['first_serve_pts_won_pct']:.3f}%")
    print(f"2nd serve pts won percentage: {m['second_serve_pts_won_pct']:.3f}%")
    print(f"Break Ponints saved percentage: {m['break_points_saved_pct']:.3f}%")

# Plot command. Plots a selected metric over time and saves it to results/<metric>.png
def cmd_plot(args):
    ensure_results()
    df = load_matches(args.csv)

    metric = args.metric
    if metric not in ALLOWED_METRICS:
        raise SystemExit("metric must be one of: first_serve_pct, first_serve_pts_won_pct, second_serve_pts_won_pct, break_points_saved_pct")

    # Build y-values. Compute chosen metric for each match row
    vals = []
    for index, row in df.iterrows():
        vals.append(compute_match_metrics(row)[metric])

    # X values are the chronological dates
    x = df["date"]

    # Create and save plot
    plt.plot(x, vals, marker="o")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.title(f"{metric} over time")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Build output file
    out = os.path.join("results", f"{metric}.png")
    plt.savefig(out, dpi=200)
    plt.close()
    print(f"Wrote: {out}")

# Build and return the top level argparse parser
def build_parser():
    parser = argparse.ArgumentParser(description="Tennis stats CLI tool (Python portfolio project)")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    summary_parser = subparsers.add_parser("summary", help="Compute season summary + write results/summary.json")
    summary_parser.add_argument("csv", help="Path to tennis_stats.csv")
    summary_parser.set_defaults(func=cmd_summary)

    match_parser = subparsers.add_parser("match", help="Show computed metrics for a specific match date")
    match_parser.add_argument("csv", help="Path to tennis_stats.csv")
    match_parser.add_argument("--date", required=True, help="Match date (YYYY-MM-DD)")
    match_parser.set_defaults(func=cmd_match)

    plot_parser = subparsers.add_parser("plot", help="Plot a metric over time to results/*.png")
    plot_parser.add_argument("csv", help="Path to tennis_stats.csv")
    plot_parser.add_argument("--metric", required=True, help=f"Metric name ({', '.join(sorted(ALLOWED_METRICS))})")
    plot_parser.set_defaults(func=cmd_plot)

    return parser

# Entry point. Parse CLI args and branch to chosen subcommand handler
def main() -> None:
    """
    Entry point: parse CLI args and dispatch to the chosen subcommand handler.
    """
    parser = build_parser()
    args = parser.parse_args()

    # Dispatch: args.func was set by the selected subcommand
    args.func(args)


if __name__ == "__main__":
    main()
