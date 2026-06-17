# Project Dump Tool

A utility for visualizing a project directory structure (similar to tree /f) and dumping file contents with filtering by directories and file extensions.

---

## Features
- Prints full project directory tree
- Excludes directories without descending into them
- Filters files by extension
- Limits file size for output
- Saves output to a file
- Recursive directory traversal

---

## Requirements
- Python 3.8 or higher

---

## Usage

Basic usage
```bash
python dump_project.py D:\Projects\market-os
```

---

Filter by file extensions
```bash
python dump_project.py D:\Projects\market-os --ext .py .env .md
```

---

Exclude directories
```bash
python dump_project.py D:\Projects\market-os --exclude-dirs .git .venv node_modules
```

---

Limit file size
```bash
python dump_project.py D:\Projects\market-os --max-size 200000
```

---

Save output to file
```bash
python dump_project.py D:\Projects\market-os --out dump.txt
```

---

Tree behavior
```bash
- All directories are shown
- Excluded directories are displayed but not expanded
- Example:
project
├── src
│   ├── main.py
│   └── file.py
├── .venv
├── .git
└── README.md
```

---

Default excluded directories
.git
.venv
pycache
node_modules
dist
build

---

Full example
```bash
python main.py . --ext .py .env --exclude-dirs .git .venv --max-size 200000 --out info.txt
```

---