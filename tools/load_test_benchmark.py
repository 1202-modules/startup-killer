#!/usr/bin/env python3
"""Measure local deterministic engine-round latency and process peak RSS."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.balance_simulation import benchmark_round, enumerate_all_paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--startup", default="coffeebot")
    args = parser.parse_args()
    if args.iterations < 1:
        parser.error("--iterations must be positive")
    startups, catalog, _ = enumerate_all_paths()
    if args.startup not in startups:
        parser.error(f"unknown startup slug: {args.startup}")
    print(json.dumps(benchmark_round(startups[args.startup], catalog, args.iterations), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
