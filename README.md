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
4. **Map Ingredients to Nutrition DB**: Finds the best match in `data/nutrition.csv` for each ingredient.
5. **Calculate Total Nutrition**: Computes total nutritional values for the full list of ingredients.
6. **Identify Dish Type**: Uses `data/food_categories.csv` to determine dish type and assign a weight category.
7. **Scale Nutrition per 1 Katori**: Outputs final nutrition facts based on scaled standard serving size (e.g., 180g).

---


### 🧩 Task 2: Handling Synonyms & Missing Data

- ✅ Uses **FuzzyWuzzy** & **Levenshtein distance** for handling fuzzy ingredient matching.
- ✅ If ingredient is not found in the nutrition DB, a "Not Found" message is returned.
- ✅ If dish type is not certain, it is categorized as `"Unknown"` with default weight set to **180g**.

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

- `utils/pipeline.py`:  
  Main pipeline – uses `fetch_ingredients()` to query Gemini, converts units, maps to nutrition DB, calculates nutrition, identifies dish type and category, and scales nutrition to 1 katori (based on yield and category weight).

- `utils/nutrition.py`:  
  - `map_ingredients_to_nutrition()`: Uses fuzzy logic to match ingredients to entries in `nutrition.csv`.  
  - `calculate_total_nutrition()`: Sums nutrient values based on weight for each mapped ingredient.

- `utils/dish_mapping.py`:  
  - Matches the dish name to a predefined dish category.
  - Uses `food_categories.csv` to assign weight.
  - If dish is unknown, sets weight to 180g and category to "Unknown".

- `efficient_mapping.py`:  
  - Advanced LLM + fuzzy logic for resolving synonyms and ambiguous names.

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




