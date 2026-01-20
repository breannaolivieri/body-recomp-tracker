import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ExerciseDBAPI:
    """Wrapper for ExerciseDB API via RapidAPI"""
    
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.base_url = "https://exercisedb.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
        }
    
    def get_all_exercises(self, limit=10, offset=0):
        """Get a list of exercises with pagination"""
        url = f"{self.base_url}/exercises"
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exercises: {e}")
            return []
    
    def search_exercises_by_name(self, name):
        """Search for exercises by name"""
        url = f"{self.base_url}/exercises/name/{name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching exercises: {e}")
            return []
    
    def get_exercises_by_body_part(self, body_part):
        """Get exercises for a specific body part"""
        url = f"{self.base_url}/exercises/bodyPart/{body_part}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exercises by body part: {e}")
            return []
    
    def get_exercises_by_target(self, target_muscle):
        """Get exercises for a specific target muscle"""
        url = f"{self.base_url}/exercises/target/{target_muscle}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exercises by target: {e}")
            return []
    
    def get_exercises_by_equipment(self, equipment):
        """Get exercises for specific equipment"""
        url = f"{self.base_url}/exercises/equipment/{equipment}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exercises by equipment: {e}")
            return []
    
    def get_body_part_list(self):
        """Get list of all available body parts"""
        url = f"{self.base_url}/exercises/bodyPartList"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching body part list: {e}")
            return []
    
    def get_target_muscle_list(self):
        """Get list of all target muscles"""
        url = f"{self.base_url}/exercises/targetList"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching target list: {e}")
            return []
    
    def get_equipment_list(self):
        """Get list of all equipment types"""
        url = f"{self.base_url}/exercises/equipmentList"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching equipment list: {e}")
            return []


# Example usage and testing
if __name__ == "__main__":
    api = ExerciseDBAPI()
    
    # Test getting body parts
    print("Available body parts:")
    body_parts = api.get_body_part_list()
    print(body_parts[:5] if body_parts else "No data available")
    
    # Test getting exercises
    print("\nSample exercises:")
    exercises = api.get_all_exercises(limit=3)
    for ex in exercises:
        print(f"- {ex.get('name', 'Unknown')}")
