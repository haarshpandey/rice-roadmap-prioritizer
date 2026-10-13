"""
RICE Roadmap Prioritizer
========================
Score a feature backlog with the RICE framework
(Reach x Impact x Confidence / Effort) and print a ranked roadmap.

RICE refresher:
  - Reach:      how many users/period this affects
  - Impact:     3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal
  - Confidence: % certainty in the estimates (e.g. 80 = 80%)
  - Effort:     person-months

Usage:
  python prioritize.py features.csv
  python prioritize.py --demo        # runs on the bundled sample backlog

The sample backlog (features.csv) is fictional — a SaaS backlog used to
demonstrate the tool.
"""

import argparse
import csv
import sys
from pathlib import Path

IMPACT_LABELS = {3: "massive", 2: "high", 1: "medium", 0.5: "low", 0.25: "minimal"}


def rice_score(reach: float, impact: float, confidence: float, effort: float) -> float:
    if effort <= 0:
        raise ValueError("Effort must be positive")
    return (reach * impact * (confidence / 100.0)) / effort


def load_backlog(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {"feature", "reach", "impact", "confidence", "effort"}
    if not required.issubset(rows[0].keys()):
        raise SystemExit(f"CSV must have columns: {sorted(required)}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank a backlog with RICE scoring.")
    parser.add_argument("csv", nargs="?", help="Backlog CSV file")
    parser.add_argument("--demo", action="store_true", help="Use the bundled sample backlog")
    parser.add_argument("--top", type=int, default=0, help="Show only the top N")
    args = parser.parse_args()

    if args.demo:
        path = Path(__file__).parent / "features.csv"
    elif args.csv:
        path = Path(args.csv)
    else:
        parser.print_help()
        sys.exit(1)

    backlog = load_backlog(path)
    scored = []
    for row in backlog:
        try:
            score = rice_score(
                float(row["reach"]), float(row["impact"]),
                float(row["confidence"]), float(row["effort"]),
            )
        except ValueError as e:
            raise SystemExit(f"Bad row {row['feature']!r}: {e}")
        scored.append((score, row))
    scored.sort(key=lambda s: s[0], reverse=True)
    if args.top:
        scored = scored[: args.top]

    print(f"\n{'Rank':<6}{'Feature':<32}{'R':>8}{'I':>8}{'C%':>6}{'E':>6}{'RICE':>10}")
    print("-" * 76)
    for i, (score, row) in enumerate(scored, 1):
        print(f"{i:<6}{row['feature']:<32}{row['reach']:>8}{row['impact']:>8}"
              f"{row['confidence']:>6}{row['effort']:>6}{score:>10.1f}")

    winner = scored[0][1]
    print(f"\nTop pick: {winner['feature']} "
          f"(impact: {IMPACT_LABELS.get(float(winner['impact']), '?')}, "
          f"effort: {winner['effort']} person-months)")


if __name__ == "__main__":
    main()
