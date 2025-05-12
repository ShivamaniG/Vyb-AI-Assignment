import json
import os

# Load measurement reference
def load_measurement_ref():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'measurement_ref.json')
    file_path = os.path.abspath(file_path)
    
    with open(file_path, 'r') as f:
        return json.load(f)["measuring_units"]

# Convert ingredient data to household units
def convert_to_household_units(ingredient_data):
    measuring_units = load_measurement_ref()
    
    # Create a dictionary that maps unit names to their conversion value to milliliters (ml)
    unit_to_ml = {unit["unit"].lower(): unit["conversion_to_ml"] for unit in measuring_units if unit["conversion_to_ml"] is not None}
    
    # Create the reverse mapping from ml value to unit name
    ml_to_unit = {v: k for k, v in unit_to_ml.items()} 
    
    # Sort the conversion values in ascending order for easier comparison
    sorted_conversion_values = sorted(unit_to_ml.values())
    
    converted_data = []
    
    # Process each item in ingredient data
    for item in ingredient_data:
        ingredient = item["ingredient"]
        quantity = item["quantity"]
        unit = item["unit"].lower() 
        
        # If the unit is one of the liquid measurements (ml-related), find the closest household unit
        if unit in ["ml", "mls", "milliliters"]:  
            closest_unit = None
            min_difference = float('inf')
            
            # Find the closest matching unit by comparing differences in volume
            for value in sorted_conversion_values:
                difference = abs(quantity - value)
                if difference < min_difference:
                    min_difference = difference
                    closest_unit = ml_to_unit[value]
            
            # Append the converted data to the result list
            converted_data.append({
                "ingredient": ingredient,
                "quantity_ml": quantity,
                "household_unit": closest_unit
            })
    
    return converted_data


# Example Input (you can use your own ingredient data)
ingredient_data = [
    { "ingredient": "milk", "quantity": 150, "unit": "ML" },
    { "ingredient": "oil", "quantity": 10, "unit": "ml" },
    { "ingredient": "sugar", "quantity": 250, "unit": "ML" }
]

# Convert the data
converted_ingredients = convert_to_household_units(ingredient_data)

# Print the output in a readable format
for ingredient in converted_ingredients:
    print(f"{ingredient['ingredient']} - {ingredient['quantity_ml']} ml = {ingredient['household_unit']}")
