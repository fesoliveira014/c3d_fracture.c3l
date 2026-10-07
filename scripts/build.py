#!/usr/bin/env python3
"""Build the public consumer or run a selected standalone test target."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_C3C_VERSION = "0.8.3"
TEST_TARGETS = ("unit", "collision_integration")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("basic", *TEST_TARGETS), default="basic")
    parser.add_argument("--run", action="store_true", help="run the basic consumer after building")
    parser.add_argument("--test-filter", help="run only tests whose names contain this text")
    parser.add_argument("--opt", choices=("O0", "O1", "O2", "O3", "O4", "O5", "Os", "Oz"), default="O0")
    parser.add_argument("--safe", choices=("yes", "no"))
    parser.add_argument("--fp-math", choices=("strict", "relaxed", "fast"))
    parser.add_argument("--c3c", default="c3c")
    args = parser.parse_args()
    if args.test_filter and args.target not in TEST_TARGETS:
        parser.error("--test-filter requires a test target")
    if args.run and args.target in TEST_TARGETS:
        parser.error("test targets already run their selected tests")
    if args.fp_math in ("relaxed", "fast") and args.opt not in ("O4", "O5"):
        parser.error("relaxed or fast math requires --opt O4 or --opt O5")
    action = "test" if args.target in TEST_TARGETS else "run" if args.run else "build"
    command = [args.c3c, action, args.target, "--path", str(ROOT), f"-{args.opt}"]
    if args.test_filter:
        command += ["--test-filter", args.test_filter]
    if args.safe:
        command.append(f"--safe={args.safe}")
    if args.fp_math:
        command.append(f"--fp-math={args.fp_math}")
    try:
        version = subprocess.check_output([args.c3c, "--version"], text=True)
        match = re.search(r"\d+\.\d+\.\d+", version)
        if match is None or match.group() != REQUIRED_C3C_VERSION:
            print(f"C3 {REQUIRED_C3C_VERSION} is required.", file=sys.stderr)
            return 1
        return subprocess.run(command, cwd=ROOT).returncode
    except OSError as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(f"Compiler check failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
