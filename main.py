import os
import argparse
from pathlib import Path

#
#
# python main.py D:/Projects/market-os --ext .py .env --exclude-dirs .git .venv node_modules .idea .ruff_cache
#
#

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}


# ---------- TREE PRINTER ----------

def print_tree(root: Path, prefix="", exclude_dirs=None, output=None):
    exclude_dirs = exclude_dirs or set()

    try:
        entries = sorted(list(root.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
    except PermissionError:
        return

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "

        line = prefix + connector + entry.name

        if output is not None:
            output.append(line)
        else:
            print(line)

        if entry.is_dir():

            # если папка запрещена — показываем, но НЕ заходим внутрь
            if entry.name in exclude_dirs:
                continue

            extension = "    " if is_last else "│   "
            print_tree(entry, prefix + extension, exclude_dirs, output)


# ---------- FILE FILTERS ----------

def should_skip_file(file_path, exts):
    if not exts:
        return False
    return file_path.suffix.lower() not in exts


def in_excluded_dir(path_parts, exclude_dirs):
    return any(part in exclude_dirs for part in path_parts)


def read_file(file_path, max_size):
    try:
        if max_size and file_path.stat().st_size > max_size:
            return "[SKIPPED: too large]\n"
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[ERROR] {e}\n"


# ---------- MAIN ----------

def main():
    parser = argparse.ArgumentParser(description="Tree + filtered file dump tool")

    parser.add_argument("root", help="Project root")

    parser.add_argument(
        "--ext",
        nargs="*",
        default=[".py", ".env", ".md", ".txt"],
        help="Allowed file extensions",
    )

    parser.add_argument(
        "--exclude-dirs",
        nargs="*",
        default=list(DEFAULT_EXCLUDE_DIRS),
        help="Directories to exclude",
    )

    parser.add_argument(
        "--max-size",
        type=int,
        default=0,
        help="Max file size in bytes",
    )

    parser.add_argument(
        "--out",
        default="",
        help="Output file",
    )

    args = parser.parse_args()

    root = Path(args.root)
    exts = set(e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.ext)
    exclude_dirs = set(args.exclude_dirs)

    output = []

    # ---------- TREE ----------
    output.append(str(root))
    print_tree(root, exclude_dirs=exclude_dirs, output=output)

    output.append("\n\n================ FILE CONTENTS ================\n")

    # ---------- FILE DUMP ----------
    for file_path in root.rglob("*"):

        if file_path.is_dir():
            continue

        if should_skip_file(file_path, exts):
            continue

        if in_excluded_dir(file_path.parts, exclude_dirs):
            continue

        output.append("\n" + "=" * 60)
        output.append(f"FILE: {file_path}")
        output.append("=" * 60 + "\n")

        output.append(read_file(file_path, args.max_size))

    result = "\n".join(output)

    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"Saved to {args.out}")
    else:
        print(result)


if __name__ == "__main__":
    main()