# Quick Start

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Rebuild Problem Bank

```bash
python problem_bank_builder.py
```

## Manage Problems

```bash
python create_problem.py list
python create_problem.py sync
python create_problem.py new
python create_problem.py remove <problem_id>
```

## Notes

- The live app reads from `app/problem_bank/`, not `app/problems/`.
- `reference/pythonbasics/` is authoring/reference material.
- See `README.md` for architecture, publishing, scaling, and troubleshooting details.
