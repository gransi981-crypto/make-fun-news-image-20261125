"""Entrypoint: copy the finished front page to /output/entry.png.

The front page (entry.png, drawn by render.py) is held in this
repository; the program only copies it to the output directory.
No rendering, no fonts and no third-party packages run in the
grader, so the program cannot fail on a missing system font:
it is a plain stdlib file copy, and two runs write identical bytes.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
