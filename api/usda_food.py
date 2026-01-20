import requests

class USDAFoodAPI:
    """Wrapper for USDA FoodData Central API - completely free!"""
    
    def __init__(self):
        # USDA FoodData Central API (no key required for basic use)
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        # You can get a free API key from https://fdc.nal.usda.gov/api-key-signup.html
        # For now, we'll use the DEMO_KEY which has limited requests
        self.api_key = "DEMO_KEY"
    
    def search_foods(self, query, page_size=10):
        """Search for foods by name"""
        url = f"{self.base_url}/foods/search"
        params = {
            'query': query,
            'pageSize': page_size,
            'api_key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_search_results(data)
        except requests.exceptions.RequestException as e:
            print(f"Error searching foods: {e}")
            return []
    
    def get_food_details(self, fdc_id):
        """Get detailed nutrition info for a specific food"""
        url = f"{self.base_url}/food/{fdc_id}"
        params = {'api_key': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return self._parse_food_details(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error getting food details: {e}")
            return None
    
    def _parse_search_results(self, data):
        """Parse search results into simplified format"""
        foods = []
        
        if 'foods' not in data:
            return foods
        
        for food in data['foods']:
            food_info = {
                'fdc_id': food.get('fdcId'),
                'description': food.get('description', 'Unknown'),
                'brand': food.get('brandOwner', 'Generic'),
                'serving_size': food.get('servingSize', 100),
                'serving_unit': food.get('servingSizeUnit', 'g'),
            }
            
            # Extract macros from foodNutrients
            nutrients = {}
            if 'foodNutrients' in food:
                for nutrient in food['foodNutrients']:
                    name = nutrient.get('nutrientName', '').lower()
                    value = nutrient.get('value', 0)
                    
                    if 'protein' in name:
                        nutrients['protein_g'] = value
                    elif 'carbohydrate' in name:
                        nutrients['carbs_g'] = value
                    elif 'total lipid' in name or 'fat' in name:
                        nutrients['fats_g'] = value
                    elif 'energy' in name:
                        # Convert kJ to kcal if needed
                        if nutrient.get('unitName', '').upper() == 'KCAL':
                            nutrients['calories'] = value
            
            food_info.update(nutrients)
            foods.append(food_info)
        
        return foods
    
    def _parse_food_details(self, data):
        """Parse detailed food information"""
        food_info = {
            'fdc_id': data.get('fdcId'),
            'description': data.get('description', 'Unknown'),
            'brand': data.get('brandOwner', 'Generic'),
            'serving_size': data.get('servingSize', 100),
            'serving_unit': data.get('servingSizeUnit', 'g'),
        }
        
        # Extract detailed nutrients
        nutrients = {
            'protein_g': 0,
            'carbs_g': 0,
            'fats_g': 0,
            'calories': 0
        }
        
        if 'foodNutrients' in data:
            for nutrient in data['foodNutrients']:
                nutrient_data = nutrient.get('nutrient', {})
                name = nutrient_data.get('name', '').lower()
                value = nutrient.get('amount', 0)
                
                if 'protein' in name:
                    nutrients['protein_g'] = value
                elif 'carbohydrate' in name and 'by difference' in name.lower():
                    nutrients['carbs_g'] = value
                elif 'total lipid' in name or ('fat' in name and 'total' in name):
                    nutrients['fats_g'] = value
                elif 'energy' in name:
                    unit = nutrient_data.get('unitName', '').upper()
                    if unit == 'KCAL':
                        nutrients['calories'] = value
        
        food_info.update(nutrients)
        return food_info
    
    def calculate_macros_for_serving(self, food_info, serving_amount):
        """Calculate macros for a custom serving size"""
        base_serving = food_info.get('serving_size', 100)
        multiplier = serving_amount / base_serving
        
        return {
            'protein_g': food_info.get('protein_g', 0) * multiplier,
            'carbs_g': food_info.get('carbs_g', 0) * multiplier,
            'fats_g': food_info.get('fats_g', 0) * multiplier,
            'calories': food_info.get('calories', 0) * multiplier
        }


# Example usage
if __name__ == "__main__":
    api = USDAFoodAPI()
    
    # Search for chicken
    print("Searching for 'chicken breast'...")
    results = api.search_foods("chicken breast", page_size=3)
    
    for food in results:
        print(f"\n{food['description']}")
        print(f"  Brand: {food.get('brand', 'N/A')}")
        print(f"  Protein: {food.get('protein_g', 0):.1f}g")
        print(f"  Carbs: {food.get('carbs_g', 0):.1f}g")
        print(f"  Fats: {food.get('fats_g', 0):.1f}g")
        print(f"  Calories: {food.get('calories', 0):.0f}")
