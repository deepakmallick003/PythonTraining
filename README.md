# Python Training Practice App

An interactive Flask app for practicing Python fundamentals through ordered, category-based exercises.

This project turns the reference material in `reference/pythonbasics/` into a structured runtime problem bank, then serves those problems in a browser UI with:

- category navigation in learning order
- starter code and reference solutions
- runnable snippets or test-backed exercises
- a Python editor UI for practice
- lightweight local user progress tracking

## What This Project Is

This app is a local-first Python practice environment.

It is designed for gradual learning: each file in `reference/pythonbasics/` maps to a practice category, and the generated problem bank preserves the original category order and in-file sequence so learners can move through topics progressively.

## Why This Exists

The reference files are useful for authoring and maintenance, but they are not ideal as a runtime source of truth.

This project separates those concerns:

- `reference/pythonbasics/` is the human-maintained source material
- `app/problem_bank/` is the structured runtime dataset used by the app
- `problem_bank_builder.py` converts reference material into the editable problem bank
- `create_problem.py` lets you inspect, add, remove, or resync stored problems without making the app parse the reference files on every request

That split keeps the runtime simple while still making the content maintainable.

## Current Capabilities

- 29 ordered problem categories
- 242 generated problems
- starter code with `main(...)` scaffolds where applicable
- at least 3 test cases for test-backed exercises
- unique input variants for generated tests
- local login and progress tracking
- VS Code launch configuration for one-click app startup

## Project Layout

```text
PythonTraining/
├── run.py                         # App entry point, fixed to port 5000
├── requirements.txt               # Python dependencies
├── problem_bank_builder.py        # Builds runtime problem bank from reference files
├── create_problem.py              # Problem bank manager (sync/list/new/remove)
├── reference/pythonbasics/        # Manual source/reference material
├── app/
│   ├── __init__.py                # Flask app factory
│   ├── routes.py                  # UI and API routes
│   ├── code_executor.py           # Safe subprocess-based code execution
│   ├── problem_loader.py          # Reads runtime problem bank
│   ├── user_manager.py            # Local user/progress storage
│   ├── data/                      # Runtime-only local state
│   ├── problem_bank/              # Runtime problem dataset used by the app
│   ├── static/                    # CSS and JS
│   └── templates/                 # Flask templates
└── .vscode/launch.json            # VS Code run/debug configuration
```

## How It Works

### Content flow

1. Reference content lives in `reference/pythonbasics/`.
2. `problem_bank_builder.py` parses those files and writes normalized storage into `app/problem_bank/`.
3. `ProblemLoader` reads only from `app/problem_bank/`.
4. The Flask app renders categories and problems from that bank.

### Runtime flow

1. User opens the app and signs in locally.
2. User selects a category and problem.
3. The browser loads starter code and test metadata from `/api/problem/<problem_id>`.
4. Submitted code is executed by `CodeExecutor` in a subprocess with timeout protection.
5. If a test-backed problem passes fully, user progress is recorded in `app/data/progress.json`.

## Requirements

- Python 3.10+ recommended
- macOS, Linux, or another environment with Python and `venv`
- `pip`

## Local Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run The App

### Standard run

```bash
source venv/bin/activate
python run.py
```

The app is fixed to `http://127.0.0.1:5000`.

If an older copy of this same app is already running on port `5000`, `run.py` will replace that older app process and keep the new server on `5000`.

If some other non-project process owns `5000`, startup will stop with an error instead of silently jumping to another port.

### Run from VS Code

Use the `Python Practice App` launch configuration from `.vscode/launch.json`.

That config:

- uses the project virtualenv
- launches `run.py`
- targets port `5000`

## First Login

The app currently uses simple local demo authentication.

- entering a new username creates a local user automatically
- progress is stored in `app/data/progress.json`
- users are stored in `app/data/users.json`

This is intended for local practice only and is not production-grade authentication.

## Build or Rebuild The Problem Bank

Use the builder when the reference files change:

```bash
source venv/bin/activate
python problem_bank_builder.py
```

That regenerates:

- `app/problem_bank/index.json`
- `app/problem_bank/categories/*.json`

## Manage Stored Problems

Use the manager for bank operations:

```bash
python create_problem.py sync
python create_problem.py list
python create_problem.py new
python create_problem.py remove <problem_id>
```

### Command meanings

- `sync`: rebuild the bank from `reference/pythonbasics/`
- `list`: show category and problem counts
- `new`: add a manual problem into an existing category
- `remove`: delete a stored problem by ID

## Data Model

The runtime bank is JSON-based and grouped by category.

Each stored problem includes fields such as:

- `id`
- `sequence`
- `category_id`
- `title`
- `prompt`
- `starter_code`
- `solution`
- `examples`
- `test_cases`
- `notes`
- `source_reference`

This gives you a consistent structure that is easy to edit, validate, diff, and extend.

## Scaling Guidance

This codebase is intentionally simple and local-first. If you want to scale it, these are the natural next steps:

### Content scaling

- move problem bank storage from JSON files to a database
- add explicit schema validation for problem definitions
- add CI checks that rebuild and diff the problem bank

### Execution scaling

- run code execution in isolated containers instead of plain subprocesses
- queue execution jobs instead of running inline with Flask
- add per-user and per-IP rate limiting

### User scaling

- replace local JSON auth with a real user store
- hash passwords
- add roles, sessions, and account recovery

### Deployment scaling

- move from Flask dev server to Gunicorn or another WSGI server
- put a reverse proxy in front
- externalize persistent state into a database and object storage

## Troubleshooting

### App will not start on port 5000

If the process using `5000` is another copy of this project, `run.py` should replace it automatically.

If startup still fails, the port is likely owned by another app on your machine. Find it with:

```bash
lsof -n -P -i tcp:5000 -sTCP:LISTEN
```

Then stop that process and run the app again.

### Problem changes are not showing up

Rebuild the bank:

```bash
python problem_bank_builder.py
```

If you changed only runtime bank JSON files directly, refresh the page and reload the relevant problem.

### Tests are failing unexpectedly

Check that:

- the problem has the correct `main(...)` signature
- the solution uses the provided input variables
- the generated `test_cases` include the correct `call`

### Login or progress looks broken

The local state files can be reset by deleting:

- `app/data/users.json`
- `app/data/progress.json`

They will be recreated automatically on next run.

### Legacy `app/problems/` JSON files are confusing

`app/problems/` is legacy content and is not used by the current runtime path.

The active runtime source is `app/problem_bank/`.

## Security Notes

This project is for local practice and internal/demo usage.

Important limitations:

- authentication is intentionally simple
- passwords are not production-safe
- code execution uses subprocess isolation, not container isolation
- there is no hardened multi-tenant security model

Do not deploy this as-is to an untrusted public environment.

## Files Intended For Git

These should be committed:

- source code
- templates, static assets, and icons used by the app
- `reference/pythonbasics/`
- generated runtime bank in `app/problem_bank/`
- documentation and repo metadata

These should not be committed:

- virtualenvs
- local runtime user/progress data
- `__pycache__` and `.pyc` files
- OS/editor junk files
- temporary assets and scratch files
- the legacy `app/problems/` folder

## Publishing Notes

Before pushing to GitHub, make sure:

1. local runtime data is empty or ignored
2. `.gitignore` is in place
3. the runtime bank is up to date
4. you are not committing secrets or machine-specific artifacts

## License

This repository includes an MIT license in `LICENSE`.
