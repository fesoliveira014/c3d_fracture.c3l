#!/usr/bin/env python3
"""Initialize pinned c3d dependencies and prepare their generated assets."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C3D = ROOT / "lib" / "c3d.c3l"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c3c", default="c3c")
    parser.add_argument("--glslang", default="glslangValidator")
    args = parser.parse_args()
    commands = [
        (["git", "submodule", "update", "--init", "--", "lib/c3d.c3l"], ROOT),
        ([sys.executable, str(C3D / "scripts" / "build.py"), "--init-deps", "--skip-build",
          "--c3c", args.c3c, "--glslang", args.glslang], C3D),
    ]
    try:
        for command, directory in commands:
            subprocess.run(command, cwd=directory, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Setup failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
