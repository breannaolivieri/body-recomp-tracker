# Quick Start Guide - Getting Your API Key 🔑

## Step-by-Step: Getting ExerciseDB API Key from RapidAPI

### 1. Go to RapidAPI
Open your browser and go to: https://rapidapi.com/

### 2. Sign Up
- Click "Sign Up" in the top right
- You can sign up with:
  - Email
  - Google account
  - GitHub account
- It's completely FREE!

### 3. Search for ExerciseDB
- Once logged in, use the search bar at the top
- Type "ExerciseDB"
- Click on the "ExerciseDB" API (should be the first result)

### 4. Subscribe to FREE Plan
- You'll see different pricing tiers
- Click "Subscribe to Test" on the **FREE (BASIC)** plan
  - This gives you 100 requests per day
  - Perfect for this project!
- Confirm the subscription (it's free, no credit card needed)

### 5. Get Your API Key
- After subscribing, you'll be on the API page
- Look for the "Code Snippets" section on the right
- You'll see headers that look like:
  ```
  X-RapidAPI-Key: abc123def456ghi789...
  X-RapidAPI-Host: exercisedb.p.rapidapi.com
  ```
- Copy the long string after "X-RapidAPI-Key:" - that's your API key!

### 6. Add Key to Your Project
- Open the `.env` file in your project folder
- Replace `your_rapidapi_key_here` with your actual key:
  ```
  RAPIDAPI_KEY=abc123def456ghi789...
  ```
- Save the file

### 7. Test It Out!
Run the ExerciseDB test script to make sure it's working:

```bash
cd api
python exercisedb.py
```

If you see a list of body parts and exercises, you're all set! 🎉

## Optional: USDA FoodData API Key

The USDA API works without a key, but if you want higher rate limits:

1. Go to: https://fdc.nal.usda.gov/api-key-signup.html
2. Fill out the form (takes 1 minute)
3. Check your email for the API key
4. In `api/usda_food.py`, replace:
   ```python
   self.api_key = "DEMO_KEY"
   ```
   with:
   ```python
   self.api_key = "your_usda_api_key"
   ```

But honestly, DEMO_KEY works fine for this project!

## Ready to Go!

Once you have your ExerciseDB API key set up, you can run the app:

```bash
python main.py
```

Have fun tracking your fitness journey! 💪
