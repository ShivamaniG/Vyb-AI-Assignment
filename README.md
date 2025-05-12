# 🍽️ Dish Nutrition Analyzer

A Flask-based API that analyzes a dish name, extracts its ingredients, maps them to a nutrition database, and returns total and scaled nutrition facts.

---

## 🚀 Deployment

✅ Hosted on **Render**: [https://vyb-ai-assignment-04mc.onrender.com](https://vyb-ai-assignment-04mc.onrender.com)

✅ Tested via **Postman**

## ✅ Tasks Completed

###  🧠 Task 1: ✅ Core Pipeline Built

1. **Input**: Accepts the *dish name* as input.
2. **Fetch Ingredients**: Uses **Gemini API** to extract a list of ingredients and their quantities.
3. **Convert Ingredient Units**: Converts ingredient quantities to household units using `data/measurement_ref.json`.
4. **Map Ingredients to Nutrition DB**: Finds the best match in `data/nutrition_db.csv` for each ingredient.
5. **Calculate Total Nutrition**: Computes total nutritional values for the full list of ingredients.
6. **Identify Dish Type**: Uses `data/food_categories.csv` to determine dish type and assign a weight category.
7. **Scale Nutrition per 1 Katori**: Outputs final nutrition facts based on scaled standard serving size (e.g., 180g).

---


### 🧩 Task 2: Handling Synonyms & Missing Data

- ✅ Uses **FuzzyWuzzy** & **Levenshtein distance** for handling fuzzy ingredient matching.
- ✅ If ingredient is not found in the nutrition DB, a "Not Found" message is returned.
- ✅ If dish type is not certain, it is categorized as `"Unknown"` with default weight category set to **180g**.

---

### 🧠 Task 3: Enhanced Reasoning for Best Match

#### Implement in `utils/efficient_mapping.py`

- **Approach 1**: Instead of returning the first match from fuzzy libraries (which may be incorrect), it fetches **a list of similar ingredients** and selects the best match manually using heuristics.
- **Approach 2**: After getting similar matches, **LLM (Gemini)** is used to determine the most accurate final match.

**Example Output:** 
-Final Best Match for Potato: Potato
-Final Best Match for Cumin Seeds: Cumin seeds (Cuminum cyminum)
-Final Best Match for lightly roasted jeera powder: Jal jeera
-Final Best Match for Roasted Potato: Baked potato with skin

## 📌 Files and Their Roles

- `main.py`:
  - The main entry point of the application, this file runs the Flask server and exposes the APIs (/analyze_dish and /analyze_multiple_dishes). It ties together the core pipeline for processing dish names and returning nutrition analysis.
It initializes the Flask app and sets up routes for the API endpoints. The file integrates the core pipeline functions from `utils/pipeline.py`, `utils/nutrition.py`, and `utils/dish_mapping.py`, managing the logic for receiving dish names, processing them through the pipeline, and returning the results in a JSON format. This serves as the main server process for both single dish and multiple dish nutrition analysis.

- `utils/pipeline.py`:
  - The heart of the pipeline, this file orchestrates the entire analysis for a single dish. It uses the `fetch_ingredients()` function to query the Gemini LLM and obtain ingredients and their quantities for the given dish name. The file includes unit conversion logic for ingredients, utilizing the `measurement_ref.json` file, and maps ingredients to the nutrition database in `nutrition.csv`. It calculates the total nutrition for all ingredients and identifies the dish type and weight using `food_categories.csv`. Finally, it scales the nutrition values based on the dish's yield and weight category.


- `utils/nutrition.py`:  
  - `map_ingredients_to_nutrition()`: Uses fuzzy logic to match ingredients to entries in `nutrition.csv`.  
  - `calculate_total_nutrition()`: Sums nutrient values based on weight for each mapped ingredient.

- `utils/dish_mapping.py`:  
  - Matches the dish name to a predefined dish category.
  - Uses `food_categories.csv` to assign weight.
  - If dish is unknown, sets weight to 180g and category to "Unknown".

- `efficient_mapping.py`:  
  - The role of this file is to resolve ingredient synonyms and ambiguous ingredient names using advanced fuzzy matching and LLM integration. In **Approach 1**, instead of relying on just the first match from fuzzy matching, it fetches a list of similar ingredients and selects the best match. In **Approach 2**, after identifying similar matches, LLM (Gemini) is used to refine and enhance the best match.


---

## 📬 API Endpoints Overview

### 🧪 `POST /analyze_dish`

This endpoint takes a single dish name as input and performs the complete nutrition analysis pipeline:

- **Extracts ingredients and their quantities** using Gemini LLM.
- **Converts units to household measurements** using `measurement_ref.json`.
- **Maps ingredients to the closest matches** in the nutrition database.
- **Calculates total nutrition** for the given ingredients.
- **Identifies the dish type** and its corresponding weight category using `dish_category_mapping` and `food_categories.csv`.
- **Computes and returns the scaled nutrition** based on the weight category.

### 🧪 `POST /analyze_multiple_dishes`

This endpoint takes a list of five dish names and performs the same analysis as above for each dish:

- Returns **dish type**, **weight category**, and **scaled nutrition** for each dish in the input list.

## 🔗 Postman Collection

Reference Postman collection for these APIs is available at:

🔗 **[Postman Collection](https://github.com/ShivamaniG/Vyb-AI-Assignment/blob/main/Vyb_Assignment.postman_collection.json)**.




