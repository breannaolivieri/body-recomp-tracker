from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User profile information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(20))
    height_cm = Column(Float)  # height in cm
    current_weight_kg = Column(Float)  # current weight
    target_weight_kg = Column(Float)  # goal weight
    
    # Macro targets
    target_protein_g = Column(Float)
    target_carbs_g = Column(Float)
    target_fats_g = Column(Float)
    target_calories = Column(Float)
    
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user")
    nutrition_logs = relationship("NutritionLog", back_populates="user")
    progress_entries = relationship("ProgressEntry", back_populates="user")


class Workout(Base):
    """Workout session information"""
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    workout_type = Column(String(50))  # e.g., "Strength", "Cardio", "Sculpt"
    duration_minutes = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")


class Exercise(Base):
    """Individual exercises within a workout"""
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    exercise_name = Column(String(200), nullable=False)
    exercise_id = Column(String(100))  # ExerciseDB ID if available
    body_part = Column(String(100))
    target_muscle = Column(String(100))
    equipment = Column(String(100))
    
    # Exercise details
    sets = Column(Integer)
    reps = Column(Integer)
    weight_kg = Column(Float)
    
    # Relationships
    workout = relationship("Workout", back_populates="exercises")


class NutritionLog(Base):
    """Daily nutrition tracking"""
    __tablename__ = 'nutrition_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    
    # Macros
    total_protein_g = Column(Float, default=0)
    total_carbs_g = Column(Float, default=0)
    total_fats_g = Column(Float, default=0)
    total_calories = Column(Float, default=0)
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="nutrition_logs")
    meals = relationship("Meal", back_populates="nutrition_log", cascade="all, delete-orphan")


class Meal(Base):
    """Individual meals/foods within a day"""
    __tablename__ = 'meals'
    
    id = Column(Integer, primary_key=True)
    nutrition_log_id = Column(Integer, ForeignKey('nutrition_logs.id'))
    meal_type = Column(String(50))  # e.g., "Breakfast", "Lunch", "Dinner", "Snack"
    food_name = Column(String(200), nullable=False)
    serving_size = Column(String(100))
    
    # Macros for this meal
    protein_g = Column(Float)
    carbs_g = Column(Float)
    fats_g = Column(Float)
    calories = Column(Float)
    
    # Relationships
    nutrition_log = relationship("NutritionLog", back_populates="meals")


class ProgressEntry(Base):
    """Track body measurements and progress photos"""
    __tablename__ = 'progress_entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    
    # Body measurements
    weight_kg = Column(Float)
    body_fat_percentage = Column(Float)
    waist_cm = Column(Float)
    chest_cm = Column(Float)
    arms_cm = Column(Float)
    thighs_cm = Column(Float)
    
    # Progress photo path (optional)
    photo_path = Column(String(500))
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="progress_entries")


# Database initialization function
def init_db(db_path='fitness_tracker.db'):
    """Initialize the database and create all tables"""
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Create and return a database session"""
    Session = sessionmaker(bind=engine)
    return Session()
