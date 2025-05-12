import pandas as pd
import os
from fuzzywuzzy import fuzz

dish_category_mapping = {
    "Dry Rice Item": ["Rice", "Pulav", "Biryani"],
    "Wet Rice Item": ["Pulao", "Khichdi", "Curd Rice"],
    "Veg Gravy": ["Paneer Butter Masala", "Mixed Vegetable Curry", "Aloo Gobi"],
    "Veg Fry": ["Aloo Fry", "Bhindi Fry", "Gobi Fry"],
    "Non - Veg Gravy": ["Chicken Curry", "Mutton Curry", "Fish Gravy"],
    "Non - Veg Fry": ["Chicken Fry", "Fish Fry"],
    "Dals": ["Dal Tadka", "Sambar", "Toor Dal"],
    "Wet Breakfast Item": ["Upma", "Poha"],
    "Dry Breakfast Item": ["Paratha", "Chilla"],
    "Chutneys": ["Coconut Chutney", "Tomato Chutney"],
    "Plain Flatbreads": ["Roti", "Chapati"],
    "Stuffed Flatbreads": ["Paratha", "Aloo Paratha"],
    "Salads": ["Cucumber Salad", "Tomato Salad"],
    "Raita": ["Boondi Raita", "Cucumber Raita"],
    "Plain Soups": ["Tomato Soup", "Lentil Soup"],
    "Mixed Soups": ["Chicken Soup", "Vegetable Soup"],
    "Hot Beverages": ["Tea", "Coffee"],
    "Beverages": ["Juice", "Lemonade"],
    "Snacks": ["Samosa", "Pakora", "Vada"],
    "Sweets": ["Gulab Jamun", "Jalebi"]
}

def load_category_weights():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'food_categories.csv')  # Adjust the path as needed
    return pd.read_csv(file_path)

category_df = load_category_weights()

category_weights = {row['Food category name']: row['Weight Cat'] for _, row in category_df.iterrows()}

from fuzzywuzzy import fuzz

def get_dish_type(dish_name):
    max_score = 0
    best_match = ("Unknown", None)

    for category, dishes in dish_category_mapping.items():
        for dish in dishes:
            score = fuzz.partial_ratio(dish_name.lower(), dish.lower())
            if score > max_score and score > 70:  # Threshold
                max_score = score
                weight_cat = category_weights.get(category, None)
                best_match = (category, weight_cat)

    return best_match


# dish_name = "Samosa"
# dish_type, weight_cat = get_dish_type(dish_name)
# print(f"The dish type for '{dish_name}' is: {dish_type}, Weight Category: {weight_cat}")
