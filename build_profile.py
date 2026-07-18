"""Build README.md from profile_template.md.

This profile intentionally stays static. Do not add private repo counts,
private infrastructure details, employer details, or real-name profile copy here.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "profile_template.md"
OUTPUT = ROOT / "README.md"


def main() -> int:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"template missing at {TEMPLATE}")
    OUTPUT.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
