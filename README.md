# Flask CLI – Project Template & Dependency Manager  
*Version 1.1.0 – Built for Python 3.11+*

> A lightweight command‑line interface for scaffolding a Flask application, adding custom files, and installing
> the required dependencies in a virtual‑env.

> **TL;DR** – Run `python flask_CLI.py` and then type `flaskapp create` to get a skeleton folder tree, or `flaskapp install` to set up a virtual‑env and install the packages listed in `requirements.txt`.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Overview](#overview) | What the script does |
| [Prerequisites](#prerequisites) | Software required |
| [Installation](#installation) | How to get the script onto your machine |
| [Usage](#usage) | Running the CLI and its commands |
| [Project Structure](#project-structure) | What the generated files look like |
| [Installing Dependencies](#installing-dependencies) | Running `flaskapp install` |

---

## Overview

`flask_CLI.py` is a small, self‑contained Python script that:

| Command | What it does |
|---------|--------------|
| `flaskapp create` | Creates a *basic* folder tree (`src/`, `config/`, `templates/`, `static/`, …) for a Flask app. |
| `flaskapp custom` | Same as `create` but prompts you for a custom folder name. |
| `flaskapp install` | 1. Verifies that **pip** is available, 2. Creates a virtual‑env called `.env`, 3. Validates that a `requirements.txt` exists, and 4. Installs the listed dependencies. |
| `flaskapp exit` | Exits the interactive shell. |
| `flaskapp help` | Shows the command list. |
| `flaskapp -v / --version` | Prints the CLI’s version. |

The script uses Python’s `cmd` module for an interactive shell and `concurrent.futures.ThreadPoolExecutor` for running the install steps in sequence.

---

## Prerequisites

| Software | Minimum Version | Install |
|----------|-----------------|---------|
| **Python** | 3.11 or newer | `https://www.python.org/downloads/` |
| **pip** | Comes with Python ≥3.4 | `python -m ensurepip` |
| **git** | Optional (for cloning the repo) | `https://git-scm.com/downloads` |

> **NOTE:** The script *does not* require any third‑party libraries beyond the Python standard library.

---

## Installation

Simply download the single file `flask_CLI.py` to any folder on your machine.

---

## Usage

1. **Start the interactive shell**

   ```bash
   python flask_CLI.py
   ```

   or, if you made it executable:

   ```bash
   ./flask_CLI.py
   ```

   You’ll see:

   ```text
   Welcome to the Flask CLI. Use this to create a template based on your Flask app needs.
   >>>
   ```

2. **Run a command**

   ```text
   >>> flaskapp create
   ```

   The CLI will create the folder tree and return a message.

3. **Show help**

   ```text
   >>> flaskapp help
   ```

4. **Check the CLI version**

   ```text
   >>> flaskapp -v
   1.1.0
   ```

5. **Exit**

   ```text
   >>> flaskapp exit
   ```
---

## Project Structure

When you run `flaskapp create` or `flaskapp custom`, the script will generate (inside `src/` by default or a custom name you provide):

```
src/
├── run.py
├── requirements.txt
├── README.md
├── .gitignore
├── __init__.py
├── config/
│   ├── __init__.py
│   └── config.py
├── models.py
├── utils.py
├── routes.py
├── templates/
│   └── base.html
└── static/
    └── main.css
```

All files are initially empty (except the placeholder imports in `__init__` files) so you can immediately start adding your own code.

---

## Installing Dependencies

After generating the skeleton, you should add a `requirements.txt` file with the packages your Flask app needs.

Once that file is in place, run:

```text
>>> flaskapp install
```

The install sequence:

1. **Verify pip** – Checks that `pip` is available.
2. **Create a virtual‑environment** – `python -m venv .env`.
3. **Verify `requirements.txt`** – Makes sure the file exists and is not empty.
4. **Run `pip install -r requirements.txt`** – Installs the packages into the `.env` virtual‑env.

If any step fails, the script stops and prints a helpful error message.

> **NOTE** – The script uses `subprocess.run("pip install …")`. On Windows you might need to specify the full path to the `pip` executable inside the virtual‑env (`.env\Scripts\pip.exe`). The script has not been tested with that exact syntax, but you can replace the line `subprocess.run(f"pip install -r {filepath}")` with `subprocess.run([sys.executable, "-m", "pip", "install", "-r", filepath])` if you encounter issues.

---



---

## FAQ & Troubleshooting

| Problem | Explanation & Fix |
|---------|-------------------|
| **`pip --version` returns nothing** | Ensure `pip` is installed (`python -m ensurepip`). On Windows, you may need to add `Scripts` to your PATH. |
| **`flaskapp install` fails because `.env` already exists** | The script doesn’t yet check for an existing environment. Remove `.env` manually or modify `create_venv()` to skip if present. |
| **`subprocess.run("pip install …")` throws “FileNotFoundError”** | On Windows, the command needs to be run via `python -m pip`. Edit `run_pip_install()` accordingly. |
| **The script creates duplicate directories** | The function `get_cwdirs()` removes items from a list while iterating, which can skip entries. Replace with a list comprehension: `dirs = [d for d in os.listdir(os.getcwd()) if not (d.endswith('.py') or d.startswith('.env'))]`. |
| **Python 3.10 works but I need 3.11** | The script only uses standard library features available since 3.7, so any 3.11‑compatible interpreter will work. Check `python --version` to confirm. |
| **I want to run the script directly from the terminal without `python`** | Add the shebang line `#!/usr/bin/env python3` at the top of `flask_CLI.py` and make it executable (`chmod +x flask_CLI.py`). Then run `./flask_CLI.py`. |

---
