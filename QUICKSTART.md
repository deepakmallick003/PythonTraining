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
python -m scripts.problem_bank_builder
```

## Manage Problems

```bash
python -m scripts.create_problem list
python -m scripts.create_problem sync
python -m scripts.create_problem new
python -m scripts.create_problem remove <problem_id>
```

## Docker

```bash
docker build -t python-training .
docker run --rm -p 5000:5000 python-training
```

## Notes

- The live app reads from `app/problem_bank/`.
- `reference/pythonbasics/` is authoring/reference material.
- See `README.md` for architecture, publishing, scaling, and troubleshooting details.
