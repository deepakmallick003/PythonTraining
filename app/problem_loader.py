"""
Problem loader backed by the generated problem bank storage.
"""

from __future__ import annotations

import json
from pathlib import Path


class ProblemLoader:
    """Loads category and problem data from the editable problem bank."""

    APP_DIR = Path(__file__).resolve().parent
    BANK_DIR = APP_DIR / "problem_bank"
    INDEX_FILE = BANK_DIR / "index.json"

    @staticmethod
    def _load_index() -> dict:
        with ProblemLoader.INDEX_FILE.open("r") as handle:
            return json.load(handle)

    @staticmethod
    def _load_category_file(relative_path: str) -> dict:
        category_path = ProblemLoader.BANK_DIR / relative_path
        with category_path.open("r") as handle:
            return json.load(handle)

    @staticmethod
    def refresh_cache() -> None:
        return None

    @staticmethod
    def get_categories() -> list[dict]:
        categories = []
        for category in ProblemLoader._load_index().get("categories", []):
            categories.append(
                {
                    "id": category["id"],
                    "name": category["name"],
                    "sequence": category["sequence"],
                    "problem_count": category.get("problem_count", 0),
                    "source_reference": category.get("source_reference"),
                }
            )
        return categories

    @staticmethod
    def get_category(category_id: str) -> dict | None:
        for category in ProblemLoader._load_index().get("categories", []):
            if category["id"] == category_id:
                category_data = ProblemLoader._load_category_file(category["file"])
                return {
                    "id": category["id"],
                    "name": category["name"],
                    "sequence": category["sequence"],
                    "problem_count": category.get("problem_count", len(category_data.get("problems", []))),
                    "source_reference": category.get("source_reference"),
                    "problems": category_data.get("problems", []),
                }
        return None

    @staticmethod
    def get_problems_by_category(category_id: str) -> list[dict]:
        category = ProblemLoader.get_category(category_id)
        if not category:
            return []

        problems = []
        for problem in category["problems"]:
            problems.append(
                {
                    "id": problem["id"],
                    "title": problem["title"],
                    "description": problem.get("description", ""),
                    "difficulty": problem.get("difficulty", "Easy"),
                    "sequence": problem.get("sequence", 0),
                    "category_id": category["id"],
                    "category_name": category["name"],
                }
            )
        return sorted(problems, key=lambda problem: problem["sequence"])

    @staticmethod
    def get_all_problems() -> list[dict]:
        all_problems = []
        for category in ProblemLoader._load_index().get("categories", []):
            category_data = ProblemLoader._load_category_file(category["file"])
            for problem in category_data.get("problems", []):
                enriched = dict(problem)
                enriched["category_sequence"] = category["sequence"]
                all_problems.append(enriched)
        return sorted(
            all_problems,
            key=lambda problem: (
                problem.get("category_sequence", 0),
                problem.get("sequence", 0),
            ),
        )

    @staticmethod
    def get_problem(problem_id: str) -> dict | None:
        for category in ProblemLoader._load_index().get("categories", []):
            category_data = ProblemLoader._load_category_file(category["file"])
            for problem in category_data.get("problems", []):
                if problem["id"] == problem_id:
                    full_problem = dict(problem)
                    full_problem["category_name"] = category["name"]
                    full_problem["category_id"] = category["id"]
                    full_problem["category_sequence"] = category["sequence"]
                    return full_problem
        return None
