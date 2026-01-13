# Tennis Stats Tool (Python CLI)

A Python command-line tool that takes tennis match stats from a CSV file, computes derived serve/pressure metrics, prints season and per-match stats, and generates metric-over-time plots.

This project is designed as :
- CLI design with `argparse`
- Data loading/cleaning with `pandas`
- Plot generation with `matplotlib`
- Unit testing with `pytest`
- Structured outputs via JSON reporting

## Project Structure
tennis-stats-tool/
tool.py # CLI entry point (summary/match/plot)
analysis.py # data loading + metric calculations (pure logic)
tennis_stats.csv # sample match dataset
requirements.txt # dependencies
results/ # generated outputs (created at runtime)
tests/
test_analysis.py # unit tests for core calculation

## Setup (WSL/Linux)

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
1) Season Summary (Prints to terminal & Writes JSON)
```bash
python tool.py summary tennis_stats.csv
   ```
Creates
- results/summary.json

2) Single Match Report (Computed metrics)
```bash
python tool.py match tennis_stats.csv --date 2025-10-08
   ```

3) Plot a metric over time (saves PNG) 
```bash
python tool.py plot tennis_stats.csv --metric first_serve_pct
```
Creates
- results/first_serve_pct.png

**Allowed Metrics**:
- first_serve_pct
- first_serve_pts_won_pct
- second_serve_pts_won_pct
- break_points_saved_pct

## Tests
Run all unit tests:
```bash
pytest -q
```

Expected Output:
- 2 passed

## Notes
- Percentages in the season summary are computed using totals (sum made / sum attempted), which weights matches properly.
- The analysis.py file contains only the core logic to keep calculations testable and reusable.
- Outputs are written to results/ (created automatically)

## Verification Checklist

From the project root:

```bash
source .venv/bin/activate
pytest -q
python tool.py summary tennis_stats.csv
python tool.py match tennis_stats.csv --date 2025-10-08
python tool.py plot tennis_stats.csv --metric first_serve_pct
ls -la results
```
You should see:
- results/summary.json
- results/first_serve_pct.png



  
