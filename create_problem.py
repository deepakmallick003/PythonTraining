#!/usr/bin/env python3
"""
Problem bank manager.

The Flask app reads from the generated problem bank in ``app/problem_bank``.
Use this script to sync from the reference material once, then list, add, or
remove stored problems without changing the runtime loader design.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from problem_bank_builder import (
    PROBLEM_BANK_CATEGORIES_DIR,
    PROBLEM_BANK_DIR,
    build_minimum_test_cases,
    build_problem_bank,
    build_problem_id,
    slugify,
)


INDEX_FILE = PROBLEM_BANK_DIR / "index.json"


def load_index() -> dict:
    if not INDEX_FILE.exists():
        return {"categories": []}
    return json.loads(INDEX_FILE.read_text())


def save_index(index: dict) -> None:
    PROBLEM_BANK_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, indent=2))


def load_category_file(relative_file: str) -> tuple[Path, dict]:
    category_path = PROBLEM_BANK_DIR / relative_file
    return category_path, json.loads(category_path.read_text())


def save_category_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def rebuild_index_from_category_files() -> dict:
    categories = []
    for category_path in sorted(PROBLEM_BANK_CATEGORIES_DIR.glob("*.json")):
        category_data = json.loads(category_path.read_text())
        categories.append(
            {
                "id": category_data["category_id"],
                "name": category_data["category_name"],
                "sequence": category_data["sequence"],
                "file": f"categories/{category_path.name}",
                "problem_count": len(category_data.get("problems", [])),
                "source_reference": category_data.get("source_reference"),
            }
        )

    categories.sort(key=lambda category: category["sequence"])
    index = {"categories": categories}
    save_index(index)
    return index


def resequence_category_problems(category_data: dict) -> None:
    category_id = category_data["category_id"]
    for sequence, problem in enumerate(category_data.get("problems", []), start=1):
        problem["sequence"] = sequence
        problem["id"] = build_problem_id(category_id, sequence, problem["title"])
        problem["category_id"] = category_id
        problem["category_name"] = category_data["category_name"]


def list_storage() -> None:
    index = load_index()
    categories = index.get("categories", [])
    if not categories:
        print("No problem bank found yet. Run: python3 create_problem.py sync")
        return

    total = sum(category["problem_count"] for category in categories)
    print(f"\nStored Categories: {len(categories)}")
    print(f"Stored Problems: {total}\n")
    for category in categories:
        print(
            f"{category['sequence']:02d}. {category['name']} "
            f"({category['problem_count']} problems)"
        )


def sync_from_reference() -> None:
    index = build_problem_bank()
    print(
        f"Problem bank synced: {len(index['categories'])} categories, "
        f"{sum(category['problem_count'] for category in index['categories'])} problems."
    )


def choose_category(index: dict) -> dict | None:
    categories = index.get("categories", [])
    if not categories:
        print("No categories found. Run a sync first.")
        return None

    print("\nAvailable categories:")
    for position, category in enumerate(categories, start=1):
        print(f"{position}. {category['name']} ({category['problem_count']} problems)")

    raw_choice = input("\nChoose a category number: ").strip()
    if not raw_choice.isdigit():
        print("Invalid category selection.")
        return None

    selected_index = int(raw_choice) - 1
    if not 0 <= selected_index < len(categories):
        print("Invalid category selection.")
        return None
    return categories[selected_index]


def prompt_multiline(prompt: str, terminator: str = "END") -> str:
    print(f"{prompt} (type {terminator} on its own line to finish)")
    lines = []
    while True:
        line = input()
        if line.strip() == terminator:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def add_problem_interactive() -> None:
    index = load_index()
    category_entry = choose_category(index)
    if not category_entry:
        return

    category_path, category_data = load_category_file(category_entry["file"])

    title = input("Problem title: ").strip()
    if not title:
        print("Problem title cannot be empty.")
        return

    prompt = input("Prompt/description: ").strip()
    if not prompt:
        prompt = title + "."

    difficulty = input("Difficulty [Easy/Medium/Hard] (default Easy): ").strip() or "Easy"
    if difficulty not in {"Easy", "Medium", "Hard"}:
        difficulty = "Easy"

    starter_code = prompt_multiline("Starter code", terminator="END")
    if not starter_code:
        starter_code = "# Write your solution here.\n"

    solution = prompt_multiline("Reference solution", terminator="END")
    if not solution:
        solution = "# Add a reference solution here.\n"

    example_input = prompt_multiline("Example input/setup", terminator="END")
    example_output = prompt_multiline("Example output", terminator="END")

    new_problem = {
        "id": "",
        "sequence": 0,
        "category_id": category_data["category_id"],
        "category_name": category_data["category_name"],
        "title": title,
        "description": prompt,
        "prompt": prompt,
        "difficulty": difficulty,
        "starter_code": starter_code if starter_code.endswith("\n") else starter_code + "\n",
        "solution": solution if solution.endswith("\n") else solution + "\n",
        "examples": [],
        "test_cases": [],
        "notes": ["Added manually through create_problem.py."],
        "source_reference": {"file": "manual-entry", "question": None},
    }

    if example_input or example_output:
        new_problem["examples"] = [
            {
                "input": example_input or "No explicit input setup required.",
                "output": example_output or "(No output)",
            }
        ]
        if example_output:
            new_problem["test_cases"] = build_minimum_test_cases(example_input, example_output)

    category_data.setdefault("problems", []).append(new_problem)
    resequence_category_problems(category_data)
    save_category_file(category_path, category_data)
    rebuild_index_from_category_files()
    print(f"Added problem '{title}' to {category_data['category_name']}.")


def remove_problem(problem_id: str) -> bool:
    index = load_index()
    for category in index.get("categories", []):
        category_path, category_data = load_category_file(category["file"])
        original_count = len(category_data.get("problems", []))
        category_data["problems"] = [
            problem
            for problem in category_data.get("problems", [])
            if problem["id"] != problem_id
        ]
        if len(category_data["problems"]) != original_count:
            resequence_category_problems(category_data)
            save_category_file(category_path, category_data)
            rebuild_index_from_category_files()
            print(f"Removed problem: {problem_id}")
            return True
    print(f"Problem not found: {problem_id}")
    return False


def remove_problem_interactive() -> None:
    problem_id = input("Problem ID to remove: ").strip()
    if not problem_id:
        print("Problem ID cannot be empty.")
        return
    remove_problem(problem_id)


def print_usage() -> None:
    print("Usage: python3 create_problem.py [sync|list|new|remove <problem_id>]")


def main() -> None:
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "sync":
            sync_from_reference()
            return
        if command == "list":
            list_storage()
            return
        if command == "new":
            add_problem_interactive()
            return
        if command == "remove":
            if len(sys.argv) > 2:
                remove_problem(sys.argv[2])
            else:
                remove_problem_interactive()
            return
        print_usage()
        return

    while True:
        print("\n" + "=" * 60)
        print("  Problem Bank Manager")
        print("=" * 60)
        print("1. Sync from reference")
        print("2. List stored categories")
        print("3. Add new problem")
        print("4. Remove problem")
        print("5. Exit")
        print("=" * 60)

        choice = input("Choose option (1-5): ").strip()
        if choice == "1":
            sync_from_reference()
        elif choice == "2":
            list_storage()
        elif choice == "3":
            add_problem_interactive()
        elif choice == "4":
            remove_problem_interactive()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
