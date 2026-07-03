"""包级入口：让 `python -m tools.fin_ai` 可用。"""
import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
