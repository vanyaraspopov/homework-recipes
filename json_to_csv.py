import json
import csv
from pathlib import Path

INPUT_JSON = Path(__file__).parent / "api.кухня.рф.recipe.search.json"
OUTPUT_CSV = Path(__file__).parent / "recipes.csv"
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


def main():
    with open(INPUT_JSON, encoding="utf-8") as f:
        data = json.load(f)

    recipe_list = data.get("recipe_list", [])
    if not recipe_list:
        print("No recipe_list found in JSON.")
        return

    filtered = [r for r in recipe_list if recipe_passes_filter(r)]

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
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

    print(f"Exported {len(filtered)} recipes to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
