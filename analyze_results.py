"""
analyze_results.py

Visualize and summarize outfit‑recommendation test results.

Usage:
    python analyze_results.py [path/to/test_results.json]

If no path is supplied, the script looks for **test_results_option2.json**
in the current working directory.

Outputs
-------
Figures:
  • prompt_performance.png                 – bar chart of overall accuracy per prompt
  • scenario_performance_heatmap.png       – heat‑map of every scenario’s score

Console:
  • A neatly formatted table showing each scenario’s percentage score per prompt.
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_results(path: str) -> dict:
    """Load the JSON results file."""
    with open(path, "r", encoding="utf‑8") as fp:
        return json.load(fp)


# ────────────────────────── Figure helpers ────────────────────────── #
def plot_prompt_performance(results: dict, save_dir: Path) -> None:
    """Bar chart of overall prompt performance percentages."""
    data = results["prompt_performance"]
    df = pd.DataFrame(
        [{"prompt": name, "percentage": metrics["percentage"]}
         for name, metrics in data.items()]
    ).sort_values("percentage", ascending=False)

    plt.figure(figsize=(8, 4))
    plt.bar(df["prompt"], df["percentage"])
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)
    plt.title("Overall Prompt Performance")
    plt.tight_layout()

    outfile = save_dir / "prompt_performance.png"
    plt.savefig(outfile)
    print(f"Saved {outfile.resolve()}")
    plt.close()


def plot_scenario_heatmap(results: dict, save_dir: Path) -> None:
    """Heat‑map of every scenario (%) across prompt types."""
    rows = []
    for sc in results["scenarios"]:
        for prompt, metrics in sc["evaluations"].items():
            rows.append(
                {
                    "scenario": sc["description"],
                    "prompt": prompt,
                    "percentage": metrics["percentage"],
                }
            )

    df = pd.DataFrame(rows)
    pivot = df.pivot(index="scenario", columns="prompt", values="percentage")

    plt.figure(figsize=(10, max(4, pivot.shape[0] * 0.4)))
    im = plt.imshow(pivot, aspect="auto", interpolation="nearest")
    plt.colorbar(im, label="Score (%)")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha="right")
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.title("Scenario Performance Heat‑map")
    plt.tight_layout()

    outfile = save_dir / "scenario_performance_heatmap.png"
    plt.savefig(outfile)
    print(f"Saved {outfile.resolve()}")
    plt.close()


# ────────────────────────── Console helper ────────────────────────── #
def print_scenario_table(results: dict) -> None:
    """
    Display a table of scenario results in the terminal.

    Columns: Scenario description + a column for each prompt (% score, 1 dp).
    """
    records = []
    for sc in results["scenarios"]:
        row = {"Scenario": sc["description"]}
        for prompt, metrics in sc["evaluations"].items():
            row[prompt] = f"{metrics['percentage']:.1f}%"
        records.append(row)

    df = pd.DataFrame(records)
    print("\nScenario Results (percentage scores)")
    print(df.to_string(index=False))


# ────────────────────────── Main ────────────────────────── #
def main() -> None:
    json_path = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else Path.cwd() / "test_results_option2.json"
    )

    if not json_path.exists():
        sys.exit(f"Error: {json_path} not found.")

    results = load_results(json_path)

    # Visual summaries
    plot_prompt_performance(results, json_path.parent)
    plot_scenario_heatmap(results, json_path.parent)

    # Console table
    print_scenario_table(results)


if __name__ == "__main__":
    main()