#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120 (Python 3.13, standard library).

The poster image is drawn by draw_poster.py and shipped as entry.png
beside this file. This program only copies it to the output directory
the grader provides, so both runs produce byte-identical output.

Local run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
print("wrote", OUT / "entry.png", file=sys.stderr)
