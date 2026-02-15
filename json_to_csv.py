"""
Parse api.кухня.рф.recipe.search.json and export name, slug, make_time to CSV.
"""
import json
import csv
from pathlib import Path

INPUT_JSON = Path(__file__).parent / "api.кухня.рф.recipe.search.json"
OUTPUT_CSV = Path(__file__).parent / "recipes.csv"
FIELDS = ["name", "slug", "make_time"]


def main():
    with open(INPUT_JSON, encoding="utf-8") as f:
        data = json.load(f)

    recipe_list = data.get("recipe_list", [])
    if not recipe_list:
        print("No recipe_list found in JSON.")
        return

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for recipe in recipe_list:
            row = {
                "name": recipe.get("name", ""),
                "slug": recipe.get("slug", ""),
                "make_time": recipe.get("make_time", ""),
            }
            writer.writerow(row)

    print(f"Exported {len(recipe_list)} recipes to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
