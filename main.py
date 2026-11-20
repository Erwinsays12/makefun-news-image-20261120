"""news-image-20261120 entry: copy the rendered poster to the grader output.

The poster itself is rendered by draw_poster.py into entry.png; this
entrypoint only places that file where the grader expects it, so the two
runs of the program write exactly the same bytes.

Run it locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os, shutil, sys


def main(argv):
    target = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    destination = os.path.join(target, "entry.png")
    shutil.copyfile(source, destination)
    print("poster copied to " + destination, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
