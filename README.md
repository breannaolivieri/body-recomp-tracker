# Body Recomp Tracker 

A beautiful desktop fitness tracking application built with Python that helps you track workouts, nutrition, and body composition progress!

## Features

- **Workout Logging**: Track exercises, sets, reps, and weights using the ExerciseDB API
- **Nutrition Tracking**: Log meals and track macros (protein, carbs, fats) using USDA FoodData Central
- **Progress Tracking**: Monitor body measurements and weight over time
- **Data Visualization**: Beautiful charts showing your progress
- **Local Database**: All your data stored securely on your computer

## Tech Stack

- **GUI**: CustomTkinter (modern, dark-mode interface)
- **Database**: SQLite with SQLAlchemy ORM
- **APIs**:
  - ExerciseDB (via RapidAPI) - 11,000+ exercises
  - USDA FoodData Central - 300,000+ food items (completely free!)
- **Visualization**: Plotly & Matplotlib
- **Data Processing**: Pandas

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

Download this project folder to your computer.

### Step 2: Install Dependencies

Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

### Step 3: Get Your ExerciseDB API Key

1. Go to [RapidAPI](https://rapidapi.com/)
2. Sign up for a free account
3. Search for "ExerciseDB" in the API marketplace
4. Subscribe to the **FREE tier** (you get 100 requests/day for free!)
5. Copy your API key from the "X-RapidAPI-Key" field

### Step 4: Set Up Environment Variables

1. Copy the `.env.example` file and rename it to `.env`
2. Open `.env` and paste your RapidAPI key:

```
RAPIDAPI_KEY=your_actual_api_key_here
```

### Step 5: Initialize the Database

Run the database setup script:

```bash
cd database
python db_setup.py
cd ..
```

## Running the App

From the project root directory:

```bash
python main.py
```

The app will open and prompt you to set up your profile on first run!

## Project Structure

```
body-recomp-tracker/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Your API keys (create this!)
├── fitness_tracker.db     # SQLite database (created automatically)
│
├── database/
│   ├── models.py          # Database models (User, Workout, Exercise, etc.)
│   └── db_setup.py        # Database initialization script
│
├── api/
│   ├── exercisedb.py      # ExerciseDB API wrapper
│   └── usda_food.py       # USDA FoodData Central API wrapper
│
├── gui/
│   ├── dashboard.py       # Dashboard view
│   ├── workout_log.py     # Workout logging interface
│   ├── nutrition_log.py   # Nutrition tracking interface
│   └── progress.py        # Progress tracking view
│
└── utils/
    └── visualizations.py  # Chart/graph generation
```

## Usage

### First Time Setup
1. Run the app
2. Enter your profile information (name, age, height, weight, macro goals)
3. Click "Let's Go!"

### Dashboard
- View your current stats and macro targets
- Quick overview of your fitness journey

### Log Workout
- Search for exercises using ExerciseDB
- Add sets, reps, and weight
- Track different workout types (strength, cardio, sculpt classes)

### Log Nutrition
- Search for foods using USDA database
- Enter serving sizes
- Track macros throughout the day

### Progress Tracking
- Log body measurements
- Add progress photos
- View weight trends over time

## API Information

### ExerciseDB API
- **Cost**: FREE (100 requests/day on free tier)
- **Data**: 11,000+ exercises with images, videos, and instructions
- **Sign up**: https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb

### USDA FoodData Central API
- **Cost**: Completely FREE (no API key needed for basic use)
- **Data**: 300,000+ food items with full nutrition info
- **Optional**: You can get a free API key for higher rate limits at https://fdc.nal.usda.gov/api-key-signup.html

## Future Enhancements

-  Export data to CSV
-  ML model to predict progress
-  Progress photo comparisons
-  Reminder notifications
-  More detailed analytics
-  Achievement badges

## Troubleshooting

### "ModuleNotFoundError"
Make sure you installed all dependencies:
```bash
pip install -r requirements.txt
```

### API Not Working
- Check your `.env` file has the correct RapidAPI key
- Make sure you're connected to the internet
- Verify you haven't exceeded the free tier limits (100 requests/day for ExerciseDB)

### Database Issues
Delete `fitness_tracker.db` and run `database/db_setup.py` again to reset the database.

## Contributing

This is a personal project, but feel free to fork it and make it your own!

## License

MIT License - feel free to use and modify!

---

Built with Python!
