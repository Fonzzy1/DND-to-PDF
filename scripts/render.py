import argparse
import glob
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
import tempfile

from py import render_sheet_tex


def load_character_from_file(file_path):
    module_name = f"character_{Path(file_path).stem}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load python file: {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    characters = [
        value
        for value in vars(module).values()
        if value.__class__.__name__ == "Character"
    ]

    if len(characters) != 1:
        raise RuntimeError(
            f"expected exactly one Character object in {file_path}, found {len(characters)}"
        )

    return characters[0]


def render_character_file(file_path):
    character = load_character_from_file(file_path)
    tex = render_sheet_tex(character)

    py_path = Path(file_path)
    tex_path = py_path.with_suffix(".tex")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    return tex_path


def main():
    parser = argparse.ArgumentParser(
        prog="render",
        usage="render path/to/character.py|dir|glob [...]"
    )
    parser.add_argument("inputs", nargs="+")
    args = parser.parse_args()

    os.makedirs("/work/.cache", exist_ok=True)
    os.makedirs("/work/template/fonts", exist_ok=True)

    found = False

    for input_item in args.inputs:
        if os.path.isdir(input_item):
            files = glob.glob(os.path.join(input_item, "*.py"))
        else:
            files = glob.glob(input_item)

        for file in files:
            if not os.path.exists(file):
                continue

            found = True
            tex_file = render_character_file(file)

            subprocess.run(
                ["latexmk", "-interaction=nonstopmode", "-pdf", "-lualatex", str(tex_file)],
                check=True,
            )

            base = os.path.splitext(os.path.basename(str(tex_file)))[0]
            for ext in [".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".toc", ".xdv", ".tex"]:
                path = base + ext
                if os.path.exists(path):
                    os.remove(path)

    if not found:
        print("no .py files found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

