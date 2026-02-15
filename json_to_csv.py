import json
import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DEFAULT_INPUT_FILES = [
    SCRIPT_DIR / "recipes_for_breakfast.json",
    SCRIPT_DIR / "recipes_for_dinner.json",
]
RECIPE_URL_PREFIX = "https://xn--j1agri5c.xn--p1ai/recipes/"
FIELDS = ["name", "slug", "make_time", "link"]
ALLOWED_TAG_NAMES = {"Завтрак", "Обед", "Ужин"}
MAX_MAKE_TIME = 120


def recipe_passes_filter(recipe: dict) -> bool:
    tag_list = recipe.get("tag_list", [])
    has_allowed_tag = any(
        tag.get("name") in ALLOWED_TAG_NAMES for tag in tag_list
    )
    make_time = recipe.get("make_time")
    try:
        make_time_ok = make_time is not None and int(make_time) <= MAX_MAKE_TIME
    except (TypeError, ValueError):
        make_time_ok = False
    return has_allowed_tag and make_time_ok


def process_json_to_csv(input_path: Path) -> None:
    """Read one JSON file, filter recipes, write CSV with same base name."""
    output_path = input_path.with_suffix(".csv")

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    recipe_list = data.get("recipe_list", [])
    if not recipe_list:
        print(f"No recipe_list found in {input_path.name}, skipping.")
        return

    filtered = [r for r in recipe_list if recipe_passes_filter(r)]

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for recipe in filtered:
            slug = recipe.get("slug", "")
            row = {
                "name": recipe.get("name", ""),
                "slug": slug,
                "make_time": recipe.get("make_time", ""),
                "link": RECIPE_URL_PREFIX + slug if slug else "",
            }
            writer.writerow(row)

    print(f"Exported {len(filtered)} recipes to {output_path.name}")


def main():
    if len(sys.argv) > 1:
        input_paths = [Path(p) for p in sys.argv[1:]]
    else:
        input_paths = DEFAULT_INPUT_FILES

    for input_path in input_paths:
        if not input_path.exists():
            print(f"File not found: {input_path}, skipping.")
            continue
        process_json_to_csv(input_path)


if __name__ == "__main__":
    main()
