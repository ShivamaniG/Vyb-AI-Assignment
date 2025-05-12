import pandas as pd
import difflib
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
def load_measurement_ref():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'nutrition_db.csv')
    return os.path.abspath(file_path)

def find_best_matches(name, choices):
    name_tokens = set(name.lower().split())
    matches = []
    max_match = 0
    
    for choice in choices:
        choice_tokens = set(choice.lower().split())
        common = name_tokens.intersection(choice_tokens)
        if len(common) > max_match:
            max_match = len(common)
            matches = [choice]
        elif len(common) == max_match:
            matches.append(choice)
    
    if matches:
        return matches
    
    fuzzy_matches = difflib.get_close_matches(name.lower(), choices, n=5, cutoff=0.7)
    return fuzzy_matches

def map_ingredient_to_nutrition(ingredient_name):
    nutrition_file = load_measurement_ref()
    nutrition_df = pd.read_csv(nutrition_file)
    ingredients = nutrition_df['food_name'].tolist()
    best_matches = find_best_matches(ingredient_name, ingredients)
    
    return best_matches

def find_best_match_with_llm(ingredient_name, best_matches):
    prompt = f"""
            Given the ingredient: "{ingredient_name}"
            And the following possible matches: {best_matches}
            Which one best matches the ingredient? Respond with only the best matching name.
            """
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    test_ingredients = [
        "Potato",
        "Cumin Seeds",
        "lightly roasted jeera powder",
        "Roasted Potato"
    ]
    
    for ingredient in test_ingredients:
        result = map_ingredient_to_nutrition(ingredient)
        # print(f"Best matches for '{ingredient}': {result}")
        best_match = find_best_match_with_llm(ingredient,result)
        print("Final Best Match for", ingredient,":",best_match) 
