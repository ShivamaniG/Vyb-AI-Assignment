import pandas as pd
import difflib
import os
import re
from fuzzywuzzy import process

def load_measurement_ref():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'nutrition_db.csv')
    return os.path.abspath(file_path)

# Load nutrition DB
nutrition_df = pd.read_csv(load_measurement_ref())

# Unit conversion (ml per unit)
unit_conversion = {
    "pieces": None, "pieces count": None,
    "katori": 150, "cup": 150, "glass": 250,
    "teaspoon": 5, "tablespoon": 15,
    "teacup": 100
}

def find_best_match(name, choices):
    name_tokens = set(name.lower().split())
    best_match = None
    max_match = 0
    for choice in choices:
        choice_tokens = set(choice.lower().split())
        common = name_tokens.intersection(choice_tokens)
        if len(common) > max_match:
            max_match = len(common)
            best_match = choice
            
    if best_match:
        return [best_match]  

    matches = difflib.get_close_matches(name.lower(), choices, n=1, cutoff=0.9)
    
    if matches:
        return matches  
    return []  

def extract_quantity_scale(household):
    text = household.lower()
    # Extract numeric values
    nums = re.findall(r"[\d.]+", text)
    quantity = float(nums[0]) if nums else 1

    # Match unit
    for unit, ml in unit_conversion.items():
        if unit in text:
            return quantity if ml is None else quantity * (ml / 100)  # assume DB is per 100ml
    return 1

def map_ingredients_to_nutrition(ingredients):
    # Map ingredients to DB
    mapped_ingredients = []

    for item in ingredients:
        ing_name = item["ingredient"]
        matches = find_best_match(ing_name, nutrition_df["food_name"].str.lower())

        if matches:
            matched_row = nutrition_df[nutrition_df["food_name"].str.lower() == matches[0]].iloc[0]
            scale = extract_quantity_scale(item["household_unit"])
            item["matched_name"] = matched_row["food_name"]
            item["nutrition_info"] = {
                "energy_kcal": round(matched_row["energy_kcal"] * scale, 2),
                "carb_g": round(matched_row["carb_g"] * scale, 2),
                "protein_g": round(matched_row["protein_g"] * scale, 2),
                "fat_g": round(matched_row["fat_g"] * scale, 2),
            }
        else:
            item["matched_name"] = "Not found"
            item["nutrition_info"] = {}

        mapped_ingredients.append(item)

    return mapped_ingredients

def calculate_total_nutrition(mapped_ingredients):
    total_nutrition = {
        "energy_kcal": 0,
        "carb_g": 0,
        "protein_g": 0,
        "fat_g": 0
    }
    
    for ingredient in mapped_ingredients:
        if "nutrition_info" in ingredient and ingredient["nutrition_info"]:
            total_nutrition["energy_kcal"] += ingredient["nutrition_info"]["energy_kcal"]
            total_nutrition["carb_g"] += ingredient["nutrition_info"]["carb_g"]
            total_nutrition["protein_g"] += ingredient["nutrition_info"]["protein_g"]
            total_nutrition["fat_g"] += ingredient["nutrition_info"]["fat_g"]
    
    return total_nutrition
