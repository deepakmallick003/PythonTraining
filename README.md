# Python Training Practice App

An interactive Flask app for practicing Python fundamentals and classic algorithms through ordered, category-based exercises.

This project turns the reference material in `reference/pythonbasics/` and `reference/algos/` into a structured runtime problem bank, then serves those problems in a browser UI with:

- category navigation in learning order
- starter code and reference solutions
- runnable snippets or test-backed exercises
- a Python editor UI for practice
- lightweight local user progress tracking

## What This Project Is

This app is a local-first Python practice environment.

It is designed for gradual learning: Python basics are generated from `reference/pythonbasics/`, and a second algorithms track is generated from `reference/algos/`, so learners can move from language fundamentals into common algorithm patterns progressively.

## Why This Exists

The reference files are useful for authoring and maintenance, but they are not ideal as a runtime source of truth.

This project separates those concerns:

- `reference/pythonbasics/` and `reference/algos/` are the human-maintained source material
- `app/problem_bank/` is the structured runtime dataset used by the app
- `scripts/problem_bank_builder.py` converts reference material into the editable problem bank
- `scripts/create_problem.py` lets you inspect, add, remove, or resync stored problems without making the app parse the reference files on every request

That split keeps the runtime simple while still making the content maintainable.

## Current Capabilities

- 38 ordered problem categories
- 305 generated problems
- starter code with `main(...)` scaffolds where applicable
- at least 3 test cases for test-backed exercises
- unique input variants for generated tests
- local login and progress tracking
- last successful code state is saved per problem and restored on revisit
- VS Code launch configuration for one-click app startup

## Project Layout

```text
PythonTraining/
├── run.py                         # App entry point, defaults to port 5000
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Containerized app runtime
├── scripts/
│   ├── problem_bank_builder.py    # Builds runtime problem bank from reference files
│   └── create_problem.py          # Problem bank manager (sync/list/new/remove)
├── reference/pythonbasics/        # Manual source/reference material for Python basics
├── reference/algos/               # Manual source/reference material for algorithms
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

1. Reference content lives in `reference/pythonbasics/` and `reference/algos/`.
2. `scripts/problem_bank_builder.py` parses those files and writes normalized storage into `app/problem_bank/`.
3. `ProblemLoader` reads only from `app/problem_bank/`.
4. The Flask app renders categories and problems from that bank.

### Runtime flow

1. User opens the app and signs in locally.
2. User selects a category and problem.
3. The browser loads starter code and test metadata from `/api/problem/<problem_id>`.
4. Submitted code is executed by `CodeExecutor` in a subprocess with timeout protection.
5. If a test-backed problem passes fully, user progress is recorded in `app/data/progress.json`.
6. The last successfully run code for a problem is also saved and restored on future visits.

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

## Run With Docker

Build the image:

```bash
docker build -t python-training .
```

Run the app in a container:

```bash
docker run --rm -p 5000:5000 python-training
```

If you want progress and local users to persist on the host, mount the data folder:

```bash
docker run --rm -p 5000:5000 -v "$(pwd)/app/data:/app/app/data" python-training
```

The container runs with:

- `HOST=0.0.0.0`
- `PORT=5000`
- `FLASK_DEBUG=0`
- `OPEN_BROWSER=0`

## Demo

A visible demo of the running app:

![Python Practice app demo](app/assets/PythonTrainingDemo.gif)

## First Login

The app currently uses simple local demo authentication.

- entering a new username creates a local user automatically
- progress is stored in `app/data/progress.json`
- users are stored in `app/data/users.json`
- the last successfully run solution for each problem is saved in `app/data/progress.json` and restored when you revisit that problem

This is intended for local practice only and is not production-grade authentication.

## Build or Rebuild The Problem Bank

Use the builder when the reference files change:

```bash
source venv/bin/activate
python -m scripts.problem_bank_builder
```

That regenerates:

- `app/problem_bank/index.json`
- `app/problem_bank/categories/*.json`

## Manage Stored Problems

Use the manager for bank operations:

```bash
python -m scripts.create_problem sync
python -m scripts.create_problem list
python -m scripts.create_problem new
python -m scripts.create_problem remove <problem_id>
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

## Latest Updates

- Added per-user persistence of the last successfully run solution for each problem.
- Problem editor now restores previous successful code instead of always resetting to starter code.
- Navigation now warns before leaving a problem if the current code has unsaved or failed changes.
- The browser favicon now matches the desktop app icon.

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
python -m scripts.problem_bank_builder
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
- maintenance scripts in `scripts/`
- documentation and repo metadata

These should not be committed:

- virtualenvs
- local runtime user/progress data
- `__pycache__` and `.pyc` files
- OS/editor junk files
- temporary assets and scratch files

## Publishing Notes

Before pushing to GitHub, make sure:

1. local runtime data is empty or ignored
2. `.gitignore` is in place
3. the runtime bank is up to date
4. you are not committing secrets or machine-specific artifacts

## License

This repository includes an MIT license in `LICENSE`.
