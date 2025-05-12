import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify
from utils.pipeline import fetch_ingredients
from utils.nutrition import map_ingredients_to_nutrition, calculate_total_nutrition
from utils.dish_mapping import get_dish_type
import re

app = Flask(__name__)
@app.route('/')
def home():
    return "Flask is working!"

# import logging
# import traceback

# logging.basicConfig(filename="debug-log.txt", level=logging.DEBUG)

@app.route('/analyze_dish', methods=['POST'])
def analyze_dish():
    try:
        data = request.get_json()
        dish_name = data.get("dish_name")

        if not dish_name:
            # logging.error("Dish name not provided.")
            return jsonify({"error": "Dish name is required"}), 400

        # logging.info(f"Analyzing dish: {dish_name}")

        ingredients, yield_info = fetch_ingredients(dish_name)
        # logging.debug(f"Fetched ingredients: {ingredients}, Yield: {yield_info}")

        mapped_ingredients = map_ingredients_to_nutrition(ingredients)
        total_nutrition = calculate_total_nutrition(mapped_ingredients)
        dish_type = get_dish_type(dish_name)
        category, weight_cat = dish_type

        if not weight_cat:
            # logging.warning(f"No category weight found for: {category}. Using default 180g.")
            weight_cat = "180g"

        weight_in_grams = int(re.findall(r'\d+', yield_info)[0])
        desired_weight = int(weight_cat.replace("g", "").strip())
        scaling_factor = desired_weight / weight_in_grams
        # logging.debug(f"Scaling factor: {scaling_factor}")

        scaled_nutrition = {
            "energy_kcal": total_nutrition['energy_kcal'] * scaling_factor,
            "carb_g": total_nutrition['carb_g'] * scaling_factor,
            "protein_g": total_nutrition['protein_g'] * scaling_factor,
            "fat_g": total_nutrition['fat_g'] * scaling_factor,
        }

        return jsonify({
            "ingredients": ingredients,
            "yield_info": yield_info,
            "mapped_nutrition": mapped_ingredients,
            "total_nutrition": total_nutrition,
            "dish_type": {
                "category": category,
                "weight_category": weight_cat
            },
            "scaled_nutrition": scaled_nutrition
        })

    except Exception as e:
        # logging.error("Error analyzing dish:")
        # logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route('/analyze_multiple_dishes', methods=['POST'])
def analyze_multiple_dishes():
    try:
        data = request.get_json()
        dish_names = data.get('dishes', [])

        if len(dish_names) != 5:
            return jsonify({"error": "Please provide exactly 5 dish names."}), 400

        result = []

        for dish_name in dish_names:
            ingredients, yield_info = fetch_ingredients(dish_name)

            mapped_ingredients = map_ingredients_to_nutrition(ingredients)
            total_nutrition = calculate_total_nutrition(mapped_ingredients)

            dish_type = get_dish_type(dish_name)
            category, weight_cat = dish_type

            weight_in_grams = int(re.findall(r'\d+', yield_info)[0])
            desired_weight = int(weight_cat.replace("g", "").strip())
            scaling_factor = desired_weight / weight_in_grams

            scaled_nutrition = {
                "carb_g": total_nutrition['carb_g'] * scaling_factor,
                "energy_kcal": total_nutrition['energy_kcal'] * scaling_factor,
                "fat_g": total_nutrition['fat_g'] * scaling_factor,
                "protein_g": total_nutrition['protein_g'] * scaling_factor,
            }

            result.append({
                "dish": dish_name,
                "scaled_nutrition": scaled_nutrition,
                "dish_type": {
                    "category": category,
                    "weight_category": weight_cat
                }
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
