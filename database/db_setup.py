from models import init_db, get_session, User
from datetime import datetime

def setup_database():
    """Initialize database and create a default user"""
    print("Setting up database...")
    engine = init_db('fitness_tracker.db')
    session = get_session(engine)
    
    # Check if user already exists
    existing_user = session.query(User).first()
    
    if not existing_user:
        # Create default user (you can customize this later in the app)
        default_user = User(
            name="User",
            age=21,
            gender="Female",
            height_cm=165,
            current_weight_kg=60,
            target_weight_kg=55,
            target_protein_g=120,
            target_carbs_g=150,
            target_fats_g=50,
            target_calories=1800
        )
        session.add(default_user)
        session.commit()
        print("✓ Default user created!")
    else:
        print("✓ User already exists!")
    
    session.close()
    print("✓ Database setup complete!")
    return engine

if __name__ == "__main__":
    setup_database()
