import json
import csv
from pathlib import Path

INPUT_JSON = Path(__file__).parent / "api.кухня.рф.recipe.search.json"
OUTPUT_CSV = Path(__file__).parent / "recipes.csv"
RECIPE_URL_PREFIX = "https://xn--j1agri5c.xn--p1ai/recipes/"
FIELDS = ["name", "slug", "make_time", "link"]


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
            slug = recipe.get("slug", "")
            row = {
                "name": recipe.get("name", ""),
                "slug": slug,
                "make_time": recipe.get("make_time", ""),
                "link": RECIPE_URL_PREFIX + slug if slug else "",
            }
            writer.writerow(row)

    print(f"Exported {len(recipe_list)} recipes to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
