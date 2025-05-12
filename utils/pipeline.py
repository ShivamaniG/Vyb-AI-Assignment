from dotenv import load_dotenv
import google.generativeai as genai
import os
import re

load_dotenv()
from utils.nutrition import map_ingredients_to_nutrition, calculate_total_nutrition
from utils.dish_mapping import load_category_weights, get_dish_type

conversion_units = {
    "Pieces": None,
    "Cup": 150,  
    "glass": 250,       
    "teaspoon": 5,      
    "tablespoon": 15,   
    "teacup": 100,      
}

def fetch_ingredients(dish_name: str) -> list:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

    response = model.generate_content(
        f"Extract only the list of ingredients and their quantities for the dish named '{dish_name}'. Format the output as a clean list showing each ingredient followed by its quantity and unit. Additionally, mention the total quantity or number of servings this dish yields based on the ingredients. Do not include any section headers, instructions, or extra text — only ingredient names with their respective amounts, followed by the yield in grams."
    )

    ingredients_text = response.text


    ingredients = []
    yield_info = ""

    for line in ingredients_text.splitlines():
        line = line.strip("-• ").strip()
        if not line:
            continue
        if "yield" in line.lower():
            # Extract numeric value with units from the yield line
            match = re.search(r'(\d+(\.\d+)?)\s*(grams|g|kg|kilograms)?', line, re.IGNORECASE)
            if match:
                yield_info = match.group(0)  # Store the matched yield info
        elif ":" in line:
            ingredients.append(line.split(":"))

    print("Yield Information:", yield_info)

    converted_ingredients = []

    for ingredient in ingredients:
        name, quantity = ingredient[0].strip(), ingredient[1].strip().lower()

        if "as needed" in quantity or "to taste" in quantity:
            continue

        original_quantity = quantity
        household_unit = ""

        try:
            qty_val = float(quantity.split()[0])
        except:
            qty_val = None

        if 'gram' in quantity and qty_val:
            if qty_val >= 250:
                household_unit = f"{qty_val / 250:.1f} Glass"
            else:
                household_unit = f"{int(qty_val)} grams"

        elif 'ml' in quantity and qty_val:
            if qty_val >= 250:
                household_unit = f"{qty_val / 250:.1f} Glass"
            elif qty_val >= 100:
                household_unit = f"{qty_val / 100:.1f} Teacup"
            elif qty_val >= 15:
                household_unit = f"{qty_val / 15:.1f} Tablespoon"
            elif qty_val >= 5:
                household_unit = f"{qty_val / 5:.1f} Teaspoon"
            else:
                household_unit = f"{qty_val} ml"

        elif any(unit in quantity for unit in ["tablespoon", "tbsp"]):
            household_unit = quantity.replace("tbsp", "Tablespoon").replace("tablespoon", "Tablespoon")
        
        elif any(unit in quantity for unit in ["katori", "cup"]):
            household_unit = quantity.replace("katori", "Cup").replace("cup", "Cup")

        elif any(unit in quantity for unit in ["teaspoon", "tsp"]):
            household_unit = quantity.replace("tsp", "Teaspoon").replace("teaspoon", "Teaspoon")

        elif any(unit in quantity.lower() for unit in ["piece", "pieces", "medium", "large", "small"]) or "-" in quantity or quantity.strip().isdigit():
            count = quantity.split()[0]
            household_unit = f"{count} Pieces"

        converted_ingredients.append({
            "ingredient": name,
            "original_quantity": original_quantity,
            "household_unit": household_unit
        })

    return converted_ingredients,yield_info

if __name__ == "__main__":
    dish_name = "Samosa"
    ingredients,yield_info = fetch_ingredients(dish_name)

    print("Converted Ingredient List:\n")
    print(f"{'Ingredient':<25} {'Original Quantity':<20} {'Household Unit'}")
    for item in ingredients:
        print(f"{item['ingredient']:<25} {item['original_quantity']:<20} {item['household_unit']}")

    print(f"\n{dish_name}: {yield_info}")
    
    mapped_ingredients = map_ingredients_to_nutrition(ingredients)
    print("\nMapped Nutrition for Each Ingredient:\n")
    for item in mapped_ingredients:
        print(f"{item['ingredient']} → {item['matched_name']}")
        if item["nutrition_info"]:
            print(f"  Energy: {item['nutrition_info']['energy_kcal']} kcal")
            print(f"  Carbs: {item['nutrition_info']['carb_g']} g")
            print(f"  Protein: {item['nutrition_info']['protein_g']} g")
            print(f"  Fat: {item['nutrition_info']['fat_g']} g\n")
        else:
            print("  Nutrition data not found.\n")
    total_nutrition = calculate_total_nutrition(mapped_ingredients)

    print(f"\nTotal Nutrition Estimate for {yield_info}:\n")
    print(f"Energy: {total_nutrition['energy_kcal']} kcal")
    print(f"Carbohydrates: {total_nutrition['carb_g']} g")
    print(f"Protein: {total_nutrition['protein_g']} g")
    print(f"Fat: {total_nutrition['fat_g']} g")

    dish_type = get_dish_type(dish_name)
    print(f"\nDish Type: {dish_type}")
    category, weight_cat = dish_type

    weight_in_grams = int(re.findall(r'\d+', yield_info)[0])
    # print(weight_in_grams)
    desired_weight = int(weight_cat.replace("g", "").strip())
    # print(desired_weight)
    scaling_factor = desired_weight / weight_in_grams
    print(f"\nNutrition for {weight_cat} of the {dish_name}:")
    print(f"Energy: {total_nutrition['energy_kcal'] * scaling_factor} kcal")
    print(f"Carbohydrates: {total_nutrition['carb_g'] * scaling_factor} g")
    print(f"Protein: {total_nutrition['protein_g'] * scaling_factor} g")
    print(f"Fat: {total_nutrition['fat_g'] * scaling_factor} g")

