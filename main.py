# SPDX-License-Identifier: MIT
"""Loading Screen Gold — make.fun bounty entry.

Writes one fresh loading-screen tip to /output/entry.txt and prints
it to stdout: a line for stressed developers and the AI coding agents
beside them, sharp enough to land mid-build. Deterministic: the same
bytes on every run. No network, no randomness, no input files, no clock.

The tip turns on a shared habit — the agent rewrites code without
asking, and the developer recognises where that confidence came from.
"""

import os

TIP = (
    "Tip: Your agent just rewrote your function without asking. "
    "Relax \u2014 it learned that confidence from watching you "
    "ship code at 2 a.m."
)


def check_tip(tip: str) -> str:
    """Return the tip unchanged, or raise ValueError if it breaks the gate.

    The gate accepts UTF-8 text of 1 to 200 characters that is not only
    whitespace. A line break would split the tip in two, and control
    characters other than tab would read as noise to the judge, so both
    are refused here too.
    """
    size = len(tip)
    if not (1 <= size <= 200):
        raise ValueError(f"tip is {size} characters, must be 1-200")
    if not tip.strip():
        raise ValueError("tip must not be only whitespace")
    if tip != tip.strip():
        raise ValueError("tip must not start or end with whitespace")
    if "\n" in tip or "\r" in tip:
        raise ValueError("tip must be a single line")
    bad = [c for c in tip if ord(c) < 0x20 and c != "\t"]
    if bad:
        raise ValueError(f"tip holds control characters: {bad!r}")
    return tip


def main() -> int:
    tip = check_tip(TIP)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(tip)
    print(tip)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
