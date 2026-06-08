from pathlib import Path

IGNORED_DIRS = {
    ".git",
    ".vs",
    "bin",
    "obj",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv"
}


def build_tree(path, excluded_dirs, prefix=""):
    result = []

    items = sorted(
        [
            item for item in path.iterdir()
            if item.name not in excluded_dirs
        ],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        branch = "└── " if is_last else "├── "
        result.append(prefix + branch + item.name)

        if item.is_dir():
            extension = "    " if is_last else "│   "
            result.extend(
                build_tree(
                    item,
                    excluded_dirs,
                    prefix + extension
                )
            )

    return result


def collect_files(path: Path, extensions: set[str]):
    files = []

    for file in path.rglob("*"):
        if not file.is_file():
            continue

        if any(part in IGNORED_DIRS for part in file.parts):
            continue

        if file.suffix.lower() in extensions:
            files.append(file)

    return files


def main():
    directory = input("Путь к проекту: ").strip()
    extensions = input(
        "Расширения для вывода содержимого (.py,.cs,.js): "
    ).strip()

    ext_set = {
        ext.strip().lower()
        for ext in extensions.split(",")
        if ext.strip()
    }

    root = Path(directory)

    output = []

    output.append("=" * 60)
    output.append("DIRECTORY STRUCTURE")
    output.append("=" * 60)
    output.append(root.name)

    output.extend(build_tree(root))

    output.append("")
    output.append("=" * 60)
    output.append("FILE CONTENTS")
    output.append("=" * 60)

    for file in collect_files(root, ext_set):
        output.append("")
        output.append(f"FILE: {file.relative_to(root)}")
        output.append("-" * 60)

        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
            output.append(content)
        except Exception as ex:
            output.append(f"[ERROR] {ex}")

    result = "\n".join(output)

    output_file = root / "project_snapshot.txt"
    output_file.write_text(result, encoding="utf-8")

    print(f"\nГотово: {output_file}")


if __name__ == "__main__":
    main()