import customtkinter as ctk
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_db, get_session, User

class FitnessTrackerApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Body Recomp Tracker")
        self.geometry("1200x800")
        
        # Set theme to light mode with pastel pink
        ctk.set_appearance_mode("light")
        
        # Custom color scheme - pastel pink and white
        self.colors = {
            'bg': '#FFFFFF',  # White background
            'pink': '#FFB6C1',  # Light pink
            'pink_dark': '#FFB6D9',  # Slightly darker pink
            'text': '#4A4A4A',  # Dark gray text
            'accent': '#FFC0CB',  # Pastel pink accent
        }
        
        # Custom fonts
        self.fonts = {
            'title': ('Georgia', 32, 'bold'),
            'heading': ('Georgia', 24, 'bold'),
            'subheading': ('Georgia', 18),
            'body': ('Georgia', 16),
            'small': ('Georgia', 14),
        }
        
        # Initialize database
        self.engine = init_db('fitness_tracker.db')
        self.session = get_session(self.engine)
        
        # Get or create user
        self.user = self.session.query(User).first()
        if not self.user:
            self.show_user_setup()
        else:
            self.create_main_layout()
    
    def show_user_setup(self):
        """Show initial user setup screen"""
        setup_frame = ctk.CTkFrame(self, fg_color=self.colors['bg'])
        setup_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            setup_frame, 
            text="Welcome! Let's set up your profile",
            font=self.fonts['title'],
            text_color=self.colors['text']
        )
        title.pack(pady=30)
        
        # Create form
        form_frame = ctk.CTkFrame(setup_frame, fg_color=self.colors['pink'])
        form_frame.pack(pady=20)
        
        # Name
        ctk.CTkLabel(form_frame, text="Name:", font=self.fonts['body'], text_color=self.colors['text']).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Age
        ctk.CTkLabel(form_frame, text="Age:", font=self.fonts['body'], text_color=self.colors['text']).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        age_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        age_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Height
        ctk.CTkLabel(form_frame, text="Height (inches):", font=self.fonts['body'], text_color=self.colors['text']).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        height_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        height_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Current Weight
        ctk.CTkLabel(form_frame, text="Current Weight (lbs):", font=self.fonts['body'], text_color=self.colors['text']).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        weight_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        weight_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Target Weight
        ctk.CTkLabel(form_frame, text="Target Weight (lbs):", font=self.fonts['body'], text_color=self.colors['text']).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        target_weight_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        target_weight_entry.grid(row=4, column=1, padx=10, pady=10)
        
        # Activity level for calorie calculation
        ctk.CTkLabel(form_frame, text="Activity Level:", font=self.fonts['body'], text_color=self.colors['text']).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        activity_var = ctk.StringVar(value="Moderate")
        activity_menu = ctk.CTkOptionMenu(
            form_frame, 
            values=["Sedentary", "Light", "Moderate", "Very Active", "Extremely Active"],
            variable=activity_var,
            fg_color="white",
            button_color=self.colors['pink'],
            button_hover_color=self.colors['pink_dark'],
            width=200
        )
        activity_menu.grid(row=5, column=1, padx=10, pady=10)
        
        # Calculate Macros Button
        def calculate_macros():
            try:
                target_weight = float(target_weight_entry.get())
                current_weight = float(weight_entry.get())
                height_in = float(height_entry.get())
                age = int(age_entry.get())
                activity = activity_var.get()
                
                # Activity multipliers
                activity_multipliers = {
                    "Sedentary": 1.2,
                    "Light": 1.375,
                    "Moderate": 1.55,
                    "Very Active": 1.725,
                    "Extremely Active": 1.9
                }
                
                # Calculate BMR using Mifflin-St Jeor (for women)
                # BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age - 161
                weight_kg = current_weight * 0.453592
                height_cm = height_in * 2.54
                bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
                
                # Calculate TDEE
                tdee = bmr * activity_multipliers[activity]
                
                # For body recomp: slight deficit (100-200 cal below TDEE)
                target_calories = tdee - 150
                
                # Macro calculation
                # Protein: 1g per lb of target weight (optimal for muscle retention)
                protein_g = target_weight * 1.0
                
                # Fats: 25% of calories
                fat_calories = target_calories * 0.25
                fat_g = fat_calories / 9
                
                # Carbs: remaining calories
                protein_calories = protein_g * 4
                carb_calories = target_calories - protein_calories - fat_calories
                carb_g = carb_calories / 4
                
                # Fill in the entries
                protein_entry.delete(0, 'end')
                protein_entry.insert(0, str(int(protein_g)))
                
                carbs_entry.delete(0, 'end')
                carbs_entry.insert(0, str(int(carb_g)))
                
                fats_entry.delete(0, 'end')
                fats_entry.insert(0, str(int(fat_g)))
                
                # Show explanation (move to row 10 to avoid overlap)
                # First clear any existing calc_info
                for widget in form_frame.winfo_children():
                    if isinstance(widget, ctk.CTkLabel) and "Calculated for" in widget.cget("text"):
                        widget.destroy()
                
                calc_info = ctk.CTkLabel(
                    form_frame,
                    text=f"Calculated for {int(target_calories)} calories/day\nBased on your stats & activity level!",
                    font=self.fonts['small'],
                    text_color=self.colors['text']
                )
                calc_info.grid(row=10, column=0, columnspan=2, pady=10)
                
            except ValueError:
                # Clear any existing errors first
                for widget in form_frame.winfo_children():
                    if isinstance(widget, ctk.CTkLabel) and ("Please fill" in widget.cget("text") or widget.cget("text_color") == "red"):
                        widget.destroy()
                
                error = ctk.CTkLabel(
                    form_frame,
                    text="Please fill in weight, height, age, and target weight first!",
                    font=self.fonts['small'],
                    text_color="red"
                )
                error.grid(row=10, column=0, columnspan=2, pady=5)
        
        calc_btn = ctk.CTkButton(
            form_frame,
            text="Calculate My Macros",
            command=calculate_macros,
            font=self.fonts['body'],
            fg_color=self.colors['pink_dark'],
            hover_color=self.colors['pink'],
            width=200
        )
        calc_btn.grid(row=6, column=0, columnspan=2, pady=15)
        
        # Protein Target
        ctk.CTkLabel(form_frame, text="Daily Protein Goal (g):", font=self.fonts['body'], text_color=self.colors['text']).grid(row=7, column=0, padx=10, pady=10, sticky="e")
        protein_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        protein_entry.grid(row=7, column=1, padx=10, pady=10)
        
        # Carbs Target
        ctk.CTkLabel(form_frame, text="Daily Carbs Goal (g):", font=self.fonts['body'], text_color=self.colors['text']).grid(row=8, column=0, padx=10, pady=10, sticky="e")
        carbs_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        carbs_entry.grid(row=8, column=1, padx=10, pady=10)
        
        # Fats Target
        ctk.CTkLabel(form_frame, text="Daily Fats Goal (g):", font=self.fonts['body'], text_color=self.colors['text']).grid(row=9, column=0, padx=10, pady=10, sticky="e")
        fats_entry = ctk.CTkEntry(form_frame, width=200, fg_color="white")
        fats_entry.grid(row=9, column=1, padx=10, pady=10)
        
        def save_profile():
            try:
                # Convert imperial to metric for storage
                height_inches = float(height_entry.get())
                weight_lbs = float(weight_entry.get())
                target_weight_lbs = float(target_weight_entry.get())
                
                # Conversions: inches to cm, lbs to kg
                height_cm = height_inches * 2.54
                weight_kg = weight_lbs * 0.453592
                target_weight_kg = target_weight_lbs * 0.453592
                
                # Create new user
                new_user = User(
                    name=name_entry.get(),
                    age=int(age_entry.get()),
                    gender="Female",  # You can add gender selection if needed
                    height_cm=height_cm,
                    current_weight_kg=weight_kg,
                    target_weight_kg=target_weight_kg,
                    target_protein_g=float(protein_entry.get()),
                    target_carbs_g=float(carbs_entry.get()),
                    target_fats_g=float(fats_entry.get()),
                    target_calories=float(protein_entry.get())*4 + float(carbs_entry.get())*4 + float(fats_entry.get())*9
                )
                
                self.session.add(new_user)
                self.session.commit()
                self.user = new_user
                
                # Destroy setup frame and create main layout
                setup_frame.destroy()
                self.create_main_layout()
                
            except ValueError:
                error_label = ctk.CTkLabel(form_frame, text="Please enter valid numbers!", text_color="red", font=self.fonts['small'])
                error_label.grid(row=11, column=0, columnspan=2, pady=10)
        
        # Save button
        save_btn = ctk.CTkButton(
            setup_frame,
            text="Let's Go!",
            command=save_profile,
            font=self.fonts['heading'],
            height=50,
            width=200,
            fg_color=self.colors['pink_dark'],
            hover_color=self.colors['pink']
        )
        save_btn.pack(pady=30)
    
    def create_main_layout(self):
        """Create the main application layout"""
        # Create sidebar navigation
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=self.colors['pink'])
        self.sidebar.pack(side="left", fill="y")
        
        # Logo/Title
        logo = ctk.CTkLabel(
            self.sidebar,
            text="Body Recomp",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        )
        logo.pack(pady=30)
        
        # User info
        user_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Hey {self.user.name}!",
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        )
        user_label.pack(pady=10)
        
        # Navigation buttons
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard,
            height=40,
            font=self.fonts['body'],
            fg_color="white",
            text_color=self.colors['text'],
            hover_color=self.colors['pink_dark']
        )
        self.dashboard_btn.pack(pady=10, padx=20, fill="x")
        
        self.workout_btn = ctk.CTkButton(
            self.sidebar,
            text="Log Workout",
            command=self.show_workout_log,
            height=40,
            font=self.fonts['body'],
            fg_color="white",
            text_color=self.colors['text'],
            hover_color=self.colors['pink_dark']
        )
        self.workout_btn.pack(pady=10, padx=20, fill="x")
        
        self.nutrition_btn = ctk.CTkButton(
            self.sidebar,
            text="Log Nutrition",
            command=self.show_nutrition_log,
            height=40,
            font=self.fonts['body'],
            fg_color="white",
            text_color=self.colors['text'],
            hover_color=self.colors['pink_dark']
        )
        self.nutrition_btn.pack(pady=10, padx=20, fill="x")
        
        self.progress_btn = ctk.CTkButton(
            self.sidebar,
            text="Progress",
            command=self.show_progress,
            height=40,
            font=self.fonts['body'],
            fg_color="white",
            text_color=self.colors['text'],
            hover_color=self.colors['pink_dark']
        )
        self.progress_btn.pack(pady=10, padx=20, fill="x")
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self, fg_color=self.colors['bg'])
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_main_frame(self):
        """Clear the main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show the dashboard view"""
        self.clear_main_frame()
        
        # Convert stored metric units to imperial for display
        current_weight_lbs = self.user.current_weight_kg / 0.453592
        target_weight_lbs = self.user.target_weight_kg / 0.453592
        height_inches = self.user.height_cm / 2.54
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="Dashboard",
            font=self.fonts['title'],
            text_color=self.colors['text']
        )
        title.pack(pady=20)
        
        # Quick stats
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['bg'])
        stats_frame.pack(fill="x", pady=20)
        
        # Current weight
        weight_frame = ctk.CTkFrame(stats_frame, fg_color=self.colors['pink'])
        weight_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        ctk.CTkLabel(
            weight_frame, 
            text="Current Weight", 
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            weight_frame,
            text=f"{current_weight_lbs:.1f} lbs",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        
        # Target weight
        target_frame = ctk.CTkFrame(stats_frame, fg_color=self.colors['pink'])
        target_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        ctk.CTkLabel(
            target_frame, 
            text="Target Weight", 
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            target_frame,
            text=f"{target_weight_lbs:.1f} lbs",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        
        # Height display
        height_frame = ctk.CTkFrame(stats_frame, fg_color=self.colors['pink'])
        height_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        ctk.CTkLabel(
            height_frame, 
            text="Height", 
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            height_frame,
            text=f"{height_inches:.1f} in",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        
        # Macro targets
        macro_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['bg'])
        macro_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            macro_frame, 
            text="Daily Macro Targets", 
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        macros_grid = ctk.CTkFrame(macro_frame, fg_color=self.colors['bg'])
        macros_grid.pack(pady=10)
        
        # Protein
        protein_box = ctk.CTkFrame(macros_grid, fg_color=self.colors['pink_dark'])
        protein_box.grid(row=0, column=0, padx=20, pady=10)
        ctk.CTkLabel(
            protein_box, 
            text="Protein", 
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            protein_box, 
            text=f"{self.user.target_protein_g}g", 
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        
        # Carbs
        carbs_box = ctk.CTkFrame(macros_grid, fg_color=self.colors['pink_dark'])
        carbs_box.grid(row=0, column=1, padx=20, pady=10)
        ctk.CTkLabel(
            carbs_box, 
            text="Carbs", 
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            carbs_box, 
            text=f"{self.user.target_carbs_g}g", 
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        
        # Fats
        fats_box = ctk.CTkFrame(macros_grid, fg_color=self.colors['pink_dark'])
        fats_box.grid(row=0, column=2, padx=20, pady=10)
        ctk.CTkLabel(
            fats_box, 
            text="Fats", 
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            fats_box, 
            text=f"{self.user.target_fats_g}g", 
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
        
        # Calories
        cal_box = ctk.CTkFrame(macros_grid, fg_color=self.colors['pink_dark'])
        cal_box.grid(row=0, column=3, padx=20, pady=10)
        ctk.CTkLabel(
            cal_box, 
            text="Calories", 
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5)
        ctk.CTkLabel(
            cal_box, 
            text=f"{int(self.user.target_calories)}", 
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5)
    
    def show_workout_log(self):
        """Show workout logging view"""
        self.clear_main_frame()
        
        from api.exercisedb import ExerciseDBAPI
        from database.models import Workout, Exercise
        from datetime import date
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="Log Workout",
            font=self.fonts['title'],
            text_color=self.colors['text']
        )
        title.pack(pady=20)
        
        # Create scrollable frame for the whole workout log
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=self.colors['bg'])
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Workout info section
        workout_info_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['pink'])
        workout_info_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            workout_info_frame,
            text="Today's Workout",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Workout type
        type_frame = ctk.CTkFrame(workout_info_frame, fg_color=self.colors['pink'])
        type_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            type_frame,
            text="Workout Type:",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(side="left", padx=5)
        
        workout_type_var = ctk.StringVar(value="Strength")
        workout_type_menu = ctk.CTkOptionMenu(
            type_frame,
            values=["Strength", "Cardio", "Sculpt", "HIIT", "Yoga", "Other"],
            variable=workout_type_var,
            fg_color="white",
            button_color=self.colors['pink_dark'],
            button_hover_color=self.colors['pink']
        )
        workout_type_menu.pack(side="left", padx=5)
        
        # Duration
        duration_frame = ctk.CTkFrame(workout_info_frame, fg_color=self.colors['pink'])
        duration_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            duration_frame,
            text="Duration (minutes):",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(side="left", padx=5)
        
        duration_entry = ctk.CTkEntry(duration_frame, width=100, fg_color="white")
        duration_entry.pack(side="left", padx=5)
        
        # Exercise search section
        search_frame = ctk.CTkFrame(scroll_frame, fg_color="white")
        search_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            search_frame,
            text="Add Exercises",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Search controls
        search_controls = ctk.CTkFrame(search_frame, fg_color="white")
        search_controls.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            search_controls,
            text="Search by:",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(side="left", padx=5)
        
        search_type_var = ctk.StringVar(value="Name")
        search_type_menu = ctk.CTkOptionMenu(
            search_controls,
            values=["Name", "Body Part", "Equipment"],
            variable=search_type_var,
            fg_color=self.colors['pink'],
            button_color=self.colors['pink_dark'],
            button_hover_color=self.colors['pink']
        )
        search_type_menu.pack(side="left", padx=5)
        
        search_entry = ctk.CTkEntry(search_controls, width=200, fg_color=self.colors['bg'], placeholder_text="e.g., squat, chest, dumbbell")
        search_entry.pack(side="left", padx=5)
        
        # Search results
        results_frame = ctk.CTkScrollableFrame(search_frame, height=200, fg_color=self.colors['bg'])
        results_frame.pack(fill="both", padx=20, pady=10)
        
        # Current workout exercises
        exercises_list = []
        
        exercises_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['pink'])
        exercises_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            exercises_frame,
            text="Exercises in Today's Workout",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        exercises_display = ctk.CTkScrollableFrame(exercises_frame, fg_color="white", height=200)
        exercises_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def update_exercises_display():
            """Update the display of exercises in current workout"""
            for widget in exercises_display.winfo_children():
                widget.destroy()
            
            if not exercises_list:
                ctk.CTkLabel(
                    exercises_display,
                    text="No exercises added yet. Search and add exercises above!",
                    font=self.fonts['body'],
                    text_color=self.colors['text']
                ).pack(pady=20)
            else:
                for i, ex in enumerate(exercises_list):
                    ex_frame = ctk.CTkFrame(exercises_display, fg_color=self.colors['pink'])
                    ex_frame.pack(fill="x", pady=5, padx=5)
                    
                    # Exercise info
                    info_label = ctk.CTkLabel(
                        ex_frame,
                        text=f"{ex['name']} ({ex['body_part']})",
                        font=self.fonts['body'],
                        text_color=self.colors['text']
                    )
                    info_label.pack(side="left", padx=10, pady=5)
                    
                    # Sets, reps, weight inputs
                    ctk.CTkLabel(ex_frame, text="Sets:", font=self.fonts['small'], text_color=self.colors['text']).pack(side="left", padx=2)
                    ex['sets_entry'] = ctk.CTkEntry(ex_frame, width=50, fg_color="white")
                    ex['sets_entry'].pack(side="left", padx=2)
                    ex['sets_entry'].insert(0, "3")
                    
                    ctk.CTkLabel(ex_frame, text="Reps:", font=self.fonts['small'], text_color=self.colors['text']).pack(side="left", padx=2)
                    ex['reps_entry'] = ctk.CTkEntry(ex_frame, width=50, fg_color="white")
                    ex['reps_entry'].pack(side="left", padx=2)
                    ex['reps_entry'].insert(0, "10")
                    
                    ctk.CTkLabel(ex_frame, text="Weight (lbs):", font=self.fonts['small'], text_color=self.colors['text']).pack(side="left", padx=2)
                    ex['weight_entry'] = ctk.CTkEntry(ex_frame, width=60, fg_color="white")
                    ex['weight_entry'].pack(side="left", padx=2)
                    ex['weight_entry'].insert(0, "0")
                    
                    # Remove button
                    def remove_exercise(idx=i):
                        exercises_list.pop(idx)
                        update_exercises_display()
                    
                    remove_btn = ctk.CTkButton(
                        ex_frame,
                        text="Remove",
                        command=remove_exercise,
                        width=70,
                        fg_color="red",
                        hover_color="#CC0000",
                        font=self.fonts['small']
                    )
                    remove_btn.pack(side="right", padx=5)
        
        def search_exercises():
            """Search for exercises using ExerciseDB API"""
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            query = search_entry.get().strip()
            if not query:
                ctk.CTkLabel(
                    results_frame,
                    text="Please enter a search term!",
                    font=self.fonts['body'],
                    text_color="red"
                ).pack(pady=10)
                return
            
            # Show loading
            loading = ctk.CTkLabel(
                results_frame,
                text="Searching...",
                font=self.fonts['body'],
                text_color=self.colors['text']
            )
            loading.pack(pady=10)
            
            try:
                api = ExerciseDBAPI()
                search_type = search_type_var.get()
                
                if search_type == "Name":
                    results = api.search_exercises_by_name(query)
                elif search_type == "Body Part":
                    results = api.get_exercises_by_body_part(query.lower())
                elif search_type == "Equipment":
                    results = api.get_exercises_by_equipment(query.lower())
                
                loading.destroy()
                
                if not results:
                    ctk.CTkLabel(
                        results_frame,
                        text=f"No exercises found for '{query}'",
                        font=self.fonts['body'],
                        text_color=self.colors['text']
                    ).pack(pady=10)
                else:
                    # Show first 10 results
                    for exercise in results[:10]:
                        result_frame = ctk.CTkFrame(results_frame, fg_color=self.colors['pink'])
                        result_frame.pack(fill="x", pady=2, padx=5)
                        
                        name = exercise.get('name', 'Unknown')
                        body_part = exercise.get('bodyPart', 'Unknown')
                        equipment = exercise.get('equipment', 'None')
                        target = exercise.get('target', 'Unknown')
                        
                        info_text = f"{name}\nBody Part: {body_part} | Equipment: {equipment}"
                        
                        ctk.CTkLabel(
                            result_frame,
                            text=info_text,
                            font=self.fonts['small'],
                            text_color=self.colors['text'],
                            justify="left"
                        ).pack(side="left", padx=10, pady=5)
                        
                        def add_exercise(ex=exercise):
                            exercises_list.append({
                                'name': ex.get('name', 'Unknown'),
                                'exercise_id': ex.get('id', ''),
                                'body_part': ex.get('bodyPart', 'Unknown'),
                                'target': ex.get('target', 'Unknown'),
                                'equipment': ex.get('equipment', 'None')
                            })
                            update_exercises_display()
                        
                        add_btn = ctk.CTkButton(
                            result_frame,
                            text="Add",
                            command=add_exercise,
                            width=60,
                            fg_color=self.colors['pink_dark'],
                            hover_color=self.colors['pink'],
                            font=self.fonts['small']
                        )
                        add_btn.pack(side="right", padx=5)
                        
            except Exception as e:
                loading.destroy()
                ctk.CTkLabel(
                    results_frame,
                    text=f"Error: {str(e)}\nMake sure your API key is set up!",
                    font=self.fonts['small'],
                    text_color="red"
                ).pack(pady=10)
        
        search_btn = ctk.CTkButton(
            search_controls,
            text="Search",
            command=search_exercises,
            fg_color=self.colors['pink_dark'],
            hover_color=self.colors['pink'],
            font=self.fonts['body']
        )
        search_btn.pack(side="left", padx=5)
        
        # Initialize display
        update_exercises_display()
        
        # Save workout button
        def save_workout():
            try:
                if not exercises_list:
                    error = ctk.CTkLabel(
                        scroll_frame,
                        text="Please add at least one exercise!",
                        font=self.fonts['body'],
                        text_color="red"
                    )
                    error.pack(pady=10)
                    return
                
                # Create workout
                workout = Workout(
                    user_id=self.user.id,
                    date=date.today(),
                    workout_type=workout_type_var.get(),
                    duration_minutes=int(duration_entry.get()) if duration_entry.get() else None
                )
                
                self.session.add(workout)
                self.session.flush()  # Get workout ID
                
                # Add exercises
                for ex in exercises_list:
                    # Convert lbs to kg for storage
                    weight_lbs = float(ex['weight_entry'].get()) if ex['weight_entry'].get() else 0
                    weight_kg = weight_lbs * 0.453592
                    
                    exercise = Exercise(
                        workout_id=workout.id,
                        exercise_name=ex['name'],
                        exercise_id=ex.get('exercise_id', ''),
                        body_part=ex['body_part'],
                        target_muscle=ex.get('target', ''),
                        equipment=ex.get('equipment', ''),
                        sets=int(ex['sets_entry'].get()) if ex['sets_entry'].get() else None,
                        reps=int(ex['reps_entry'].get()) if ex['reps_entry'].get() else None,
                        weight_kg=weight_kg
                    )
                    self.session.add(exercise)
                
                self.session.commit()
                
                # Success message
                success = ctk.CTkLabel(
                    scroll_frame,
                    text="Workout saved successfully!",
                    font=self.fonts['heading'],
                    text_color="green"
                )
                success.pack(pady=10)
                
                # Clear the form
                exercises_list.clear()
                update_exercises_display()
                duration_entry.delete(0, 'end')
                
            except Exception as e:
                self.session.rollback()
                error = ctk.CTkLabel(
                    scroll_frame,
                    text=f"Error saving workout: {str(e)}",
                    font=self.fonts['body'],
                    text_color="red"
                )
                error.pack(pady=10)
        
        save_btn = ctk.CTkButton(
            scroll_frame,
            text="Save Workout",
            command=save_workout,
            font=self.fonts['heading'],
            height=50,
            fg_color=self.colors['pink_dark'],
            hover_color=self.colors['pink']
        )
        save_btn.pack(pady=20)
    
    def show_nutrition_log(self):
        """Show nutrition logging view"""
        self.clear_main_frame()
        
        from api.usda_food import USDAFoodAPI
        from database.models import NutritionLog, Meal
        from datetime import date
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="Log Nutrition",
            font=self.fonts['title'],
            text_color=self.colors['text']
        )
        title.pack(pady=20)
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=self.colors['bg'])
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Get or create today's nutrition log
        today = date.today()
        nutrition_log = self.session.query(NutritionLog).filter_by(
            user_id=self.user.id,
            date=today
        ).first()
        
        if not nutrition_log:
            nutrition_log = NutritionLog(
                user_id=self.user.id,
                date=today
            )
            self.session.add(nutrition_log)
            self.session.commit()
        
        # Macro progress section
        progress_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['pink'])
        progress_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            progress_frame,
            text="Today's Macros",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Macro display with progress
        macros_grid = ctk.CTkFrame(progress_frame, fg_color=self.colors['pink'])
        macros_grid.pack(pady=10, padx=20)
        
        def update_macro_display():
            """Update the macro progress display"""
            for widget in macros_grid.winfo_children():
                widget.destroy()
            
            # Refresh nutrition log from database
            self.session.refresh(nutrition_log)
            
            # Protein
            protein_frame = ctk.CTkFrame(macros_grid, fg_color="white")
            protein_frame.grid(row=0, column=0, padx=10, pady=10)
            ctk.CTkLabel(
                protein_frame,
                text="Protein",
                font=self.fonts['body'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            ctk.CTkLabel(
                protein_frame,
                text=f"{nutrition_log.total_protein_g:.0f}g / {self.user.target_protein_g:.0f}g",
                font=self.fonts['heading'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            
            # Carbs
            carbs_frame = ctk.CTkFrame(macros_grid, fg_color="white")
            carbs_frame.grid(row=0, column=1, padx=10, pady=10)
            ctk.CTkLabel(
                carbs_frame,
                text="Carbs",
                font=self.fonts['body'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            ctk.CTkLabel(
                carbs_frame,
                text=f"{nutrition_log.total_carbs_g:.0f}g / {self.user.target_carbs_g:.0f}g",
                font=self.fonts['heading'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            
            # Fats
            fats_frame = ctk.CTkFrame(macros_grid, fg_color="white")
            fats_frame.grid(row=0, column=2, padx=10, pady=10)
            ctk.CTkLabel(
                fats_frame,
                text="Fats",
                font=self.fonts['body'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            ctk.CTkLabel(
                fats_frame,
                text=f"{nutrition_log.total_fats_g:.0f}g / {self.user.target_fats_g:.0f}g",
                font=self.fonts['heading'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            
            # Calories
            cals_frame = ctk.CTkFrame(macros_grid, fg_color="white")
            cals_frame.grid(row=0, column=3, padx=10, pady=10)
            ctk.CTkLabel(
                cals_frame,
                text="Calories",
                font=self.fonts['body'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
            ctk.CTkLabel(
                cals_frame,
                text=f"{nutrition_log.total_calories:.0f} / {self.user.target_calories:.0f}",
                font=self.fonts['heading'],
                text_color=self.colors['text']
            ).pack(pady=5, padx=20)
        
        # Food search section
        search_frame = ctk.CTkFrame(scroll_frame, fg_color="white")
        search_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            search_frame,
            text="Add Food",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Search controls
        search_controls = ctk.CTkFrame(search_frame, fg_color="white")
        search_controls.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            search_controls,
            text="Search for food:",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(side="left", padx=5)
        
        search_entry = ctk.CTkEntry(
            search_controls,
            width=250,
            fg_color=self.colors['bg'],
            placeholder_text="e.g., chicken breast, banana, oatmeal"
        )
        search_entry.pack(side="left", padx=5)
        
        # Search results
        results_frame = ctk.CTkScrollableFrame(search_frame, height=200, fg_color=self.colors['bg'])
        results_frame.pack(fill="both", padx=20, pady=10)
        
        def search_foods():
            """Search for foods using USDA API"""
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            query = search_entry.get().strip()
            if not query:
                ctk.CTkLabel(
                    results_frame,
                    text="Please enter a food name!",
                    font=self.fonts['body'],
                    text_color="red"
                ).pack(pady=10)
                return
            
            # Show loading
            loading = ctk.CTkLabel(
                results_frame,
                text="Searching...",
                font=self.fonts['body'],
                text_color=self.colors['text']
            )
            loading.pack(pady=10)
            
            try:
                api = USDAFoodAPI()
                results = api.search_foods(query, page_size=10)
                
                loading.destroy()
                
                if not results:
                    ctk.CTkLabel(
                        results_frame,
                        text=f"No foods found for '{query}'",
                        font=self.fonts['body'],
                        text_color=self.colors['text']
                    ).pack(pady=10)
                else:
                    for food in results:
                        result_frame = ctk.CTkFrame(results_frame, fg_color=self.colors['pink'])
                        result_frame.pack(fill="x", pady=2, padx=5)
                        
                        name = food.get('description', 'Unknown')
                        brand = food.get('brand', 'Generic')
                        protein = food.get('protein_g', 0)
                        carbs = food.get('carbs_g', 0)
                        fats = food.get('fats_g', 0)
                        cals = food.get('calories', 0)
                        
                        info_text = f"{name} ({brand})\nP: {protein:.1f}g | C: {carbs:.1f}g | F: {fats:.1f}g | Cals: {cals:.0f}"
                        
                        info_label = ctk.CTkLabel(
                            result_frame,
                            text=info_text,
                            font=self.fonts['small'],
                            text_color=self.colors['text'],
                            justify="left"
                        )
                        info_label.pack(side="left", padx=10, pady=5)
                        
                        def add_food(f=food):
                            # Create popup for serving size
                            popup = ctk.CTkToplevel(self)
                            popup.title("Add Food")
                            popup.geometry("400x300")
                            popup.configure(fg_color=self.colors['bg'])
                            
                            ctk.CTkLabel(
                                popup,
                                text=f"Add: {f.get('description', 'Unknown')}",
                                font=self.fonts['heading'],
                                text_color=self.colors['text']
                            ).pack(pady=20)
                            
                            # Meal type
                            ctk.CTkLabel(
                                popup,
                                text="Meal Type:",
                                font=self.fonts['body'],
                                text_color=self.colors['text']
                            ).pack(pady=5)
                            
                            meal_var = ctk.StringVar(value="Breakfast")
                            meal_menu = ctk.CTkOptionMenu(
                                popup,
                                values=["Breakfast", "Lunch", "Dinner", "Snack"],
                                variable=meal_var,
                                fg_color=self.colors['pink'],
                                button_color=self.colors['pink_dark']
                            )
                            meal_menu.pack(pady=5)
                            
                            # Serving size
                            ctk.CTkLabel(
                                popup,
                                text="Serving Size (g):",
                                font=self.fonts['body'],
                                text_color=self.colors['text']
                            ).pack(pady=5)
                            
                            serving_entry = ctk.CTkEntry(popup, fg_color="white")
                            serving_entry.insert(0, str(f.get('serving_size', 100)))
                            serving_entry.pack(pady=5)
                            
                            def save_food():
                                try:
                                    serving = float(serving_entry.get())
                                    
                                    # Calculate macros for this serving
                                    calculated = api.calculate_macros_for_serving(f, serving)
                                    
                                    # Create meal
                                    meal = Meal(
                                        nutrition_log_id=nutrition_log.id,
                                        meal_type=meal_var.get(),
                                        food_name=f.get('description', 'Unknown'),
                                        serving_size=f"{serving}g",
                                        protein_g=calculated['protein_g'],
                                        carbs_g=calculated['carbs_g'],
                                        fats_g=calculated['fats_g'],
                                        calories=calculated['calories']
                                    )
                                    self.session.add(meal)
                                    
                                    # Update nutrition log totals
                                    nutrition_log.total_protein_g += calculated['protein_g']
                                    nutrition_log.total_carbs_g += calculated['carbs_g']
                                    nutrition_log.total_fats_g += calculated['fats_g']
                                    nutrition_log.total_calories += calculated['calories']
                                    
                                    self.session.commit()
                                    
                                    # Update display
                                    update_macro_display()
                                    update_meals_display()
                                    
                                    popup.destroy()
                                    
                                except ValueError:
                                    error = ctk.CTkLabel(
                                        popup,
                                        text="Please enter a valid number!",
                                        text_color="red"
                                    )
                                    error.pack(pady=5)
                            
                            ctk.CTkButton(
                                popup,
                                text="Add to Log",
                                command=save_food,
                                fg_color=self.colors['pink_dark'],
                                hover_color=self.colors['pink'],
                                font=self.fonts['body']
                            ).pack(pady=20)
                        
                        add_btn = ctk.CTkButton(
                            result_frame,
                            text="Add",
                            command=add_food,
                            width=60,
                            fg_color=self.colors['pink_dark'],
                            hover_color=self.colors['pink'],
                            font=self.fonts['small']
                        )
                        add_btn.pack(side="right", padx=5)
                        
            except Exception as e:
                loading.destroy()
                ctk.CTkLabel(
                    results_frame,
                    text=f"Error: {str(e)}",
                    font=self.fonts['small'],
                    text_color="red"
                ).pack(pady=10)
        
        search_btn = ctk.CTkButton(
            search_controls,
            text="Search",
            command=search_foods,
            fg_color=self.colors['pink_dark'],
            hover_color=self.colors['pink'],
            font=self.fonts['body']
        )
        search_btn.pack(side="left", padx=5)
        
        # Today's meals section
        meals_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['pink'])
        meals_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            meals_frame,
            text="Today's Meals",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        meals_display = ctk.CTkScrollableFrame(meals_frame, fg_color="white", height=200)
        meals_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def update_meals_display():
            """Update the display of today's meals"""
            for widget in meals_display.winfo_children():
                widget.destroy()
            
            # Get all meals for today
            meals = self.session.query(Meal).filter_by(nutrition_log_id=nutrition_log.id).all()
            
            if not meals:
                ctk.CTkLabel(
                    meals_display,
                    text="No meals logged yet. Search and add foods above!",
                    font=self.fonts['body'],
                    text_color=self.colors['text']
                ).pack(pady=20)
            else:
                for meal in meals:
                    meal_frame = ctk.CTkFrame(meals_display, fg_color=self.colors['pink'])
                    meal_frame.pack(fill="x", pady=5, padx=5)
                    
                    meal_info = f"{meal.meal_type}: {meal.food_name} ({meal.serving_size})\n"
                    meal_info += f"P: {meal.protein_g:.1f}g | C: {meal.carbs_g:.1f}g | F: {meal.fats_g:.1f}g | Cals: {meal.calories:.0f}"
                    
                    ctk.CTkLabel(
                        meal_frame,
                        text=meal_info,
                        font=self.fonts['small'],
                        text_color=self.colors['text'],
                        justify="left"
                    ).pack(side="left", padx=10, pady=5)
                    
                    def delete_meal(m=meal):
                        # Update totals
                        nutrition_log.total_protein_g -= m.protein_g
                        nutrition_log.total_carbs_g -= m.carbs_g
                        nutrition_log.total_fats_g -= m.fats_g
                        nutrition_log.total_calories -= m.calories
                        
                        self.session.delete(m)
                        self.session.commit()
                        
                        update_macro_display()
                        update_meals_display()
                    
                    delete_btn = ctk.CTkButton(
                        meal_frame,
                        text="Remove",
                        command=delete_meal,
                        width=70,
                        fg_color="red",
                        hover_color="#CC0000",
                        font=self.fonts['small']
                    )
                    delete_btn.pack(side="right", padx=5)
        
        # Initialize displays
        update_macro_display()
        update_meals_display()
    
    def show_progress(self):
        """Show progress tracking view"""
        self.clear_main_frame()
        
        from database.models import ProgressEntry
        from datetime import date, timedelta
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="Progress Tracker",
            font=self.fonts['title'],
            text_color=self.colors['text']
        )
        title.pack(pady=20)
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=self.colors['bg'])
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Current stats section
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['pink'])
        stats_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="Current Stats",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Get latest progress entry
        latest_entry = self.session.query(ProgressEntry).filter_by(
            user_id=self.user.id
        ).order_by(ProgressEntry.date.desc()).first()
        
        # Display current weight
        stats_grid = ctk.CTkFrame(stats_frame, fg_color=self.colors['pink'])
        stats_grid.pack(pady=10, padx=20)
        
        current_weight_lbs = self.user.current_weight_kg / 0.453592 if self.user.current_weight_kg else 0
        target_weight_lbs = self.user.target_weight_kg / 0.453592 if self.user.target_weight_kg else 0
        
        # Current weight box
        current_box = ctk.CTkFrame(stats_grid, fg_color="white")
        current_box.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(
            current_box,
            text="Current Weight",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5, padx=20)
        ctk.CTkLabel(
            current_box,
            text=f"{current_weight_lbs:.1f} lbs",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5, padx=20)
        
        # Target weight box
        target_box = ctk.CTkFrame(stats_grid, fg_color="white")
        target_box.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(
            target_box,
            text="Target Weight",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5, padx=20)
        ctk.CTkLabel(
            target_box,
            text=f"{target_weight_lbs:.1f} lbs",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5, padx=20)
        
        # Progress box
        remaining = current_weight_lbs - target_weight_lbs
        progress_box = ctk.CTkFrame(stats_grid, fg_color="white")
        progress_box.grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(
            progress_box,
            text="Remaining",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).pack(pady=5, padx=20)
        ctk.CTkLabel(
            progress_box,
            text=f"{remaining:.1f} lbs",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=5, padx=20)
        
        # Log new entry section
        log_frame = ctk.CTkFrame(scroll_frame, fg_color="white")
        log_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            log_frame,
            text="Log Progress",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Input fields
        inputs_frame = ctk.CTkFrame(log_frame, fg_color="white")
        inputs_frame.pack(pady=10, padx=20)
        
        # Weight
        ctk.CTkLabel(
            inputs_frame,
            text="Weight (lbs):",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        weight_entry = ctk.CTkEntry(inputs_frame, width=100, fg_color=self.colors['bg'])
        weight_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Body fat percentage (optional)
        ctk.CTkLabel(
            inputs_frame,
            text="Body Fat % (optional):",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        bf_entry = ctk.CTkEntry(inputs_frame, width=100, fg_color=self.colors['bg'])
        bf_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Measurements (optional)
        ctk.CTkLabel(
            inputs_frame,
            text="Waist (inches, optional):",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        waist_entry = ctk.CTkEntry(inputs_frame, width=100, fg_color=self.colors['bg'])
        waist_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Notes
        ctk.CTkLabel(
            inputs_frame,
            text="Notes (optional):",
            font=self.fonts['body'],
            text_color=self.colors['text']
        ).grid(row=3, column=0, padx=10, pady=5, sticky="ne")
        notes_entry = ctk.CTkTextbox(inputs_frame, width=200, height=60, fg_color=self.colors['bg'])
        notes_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def save_progress():
            try:
                weight_lbs = float(weight_entry.get())
                weight_kg = weight_lbs * 0.453592
                
                # Convert measurements from inches to cm
                waist_in = float(waist_entry.get()) if waist_entry.get() else None
                waist_cm = waist_in * 2.54 if waist_in else None
                
                bf = float(bf_entry.get()) if bf_entry.get() else None
                
                # Create progress entry
                entry = ProgressEntry(
                    user_id=self.user.id,
                    date=date.today(),
                    weight_kg=weight_kg,
                    body_fat_percentage=bf,
                    waist_cm=waist_cm,
                    notes=notes_entry.get("1.0", "end-1c") if notes_entry.get("1.0", "end-1c") else None
                )
                
                self.session.add(entry)
                
                # Update user's current weight
                self.user.current_weight_kg = weight_kg
                
                self.session.commit()
                
                # Success message
                success = ctk.CTkLabel(
                    log_frame,
                    text="Progress logged successfully!",
                    font=self.fonts['body'],
                    text_color="green"
                )
                success.pack(pady=10)
                
                # Clear entries
                weight_entry.delete(0, 'end')
                bf_entry.delete(0, 'end')
                waist_entry.delete(0, 'end')
                notes_entry.delete("1.0", "end")
                
                # Refresh the view
                self.show_progress()
                
            except ValueError:
                error = ctk.CTkLabel(
                    log_frame,
                    text="Please enter a valid weight!",
                    font=self.fonts['body'],
                    text_color="red"
                )
                error.pack(pady=10)
        
        save_btn = ctk.CTkButton(
            log_frame,
            text="Save Progress",
            command=save_progress,
            fg_color=self.colors['pink_dark'],
            hover_color=self.colors['pink'],
            font=self.fonts['body']
        )
        save_btn.pack(pady=10)
        
        # Progress history section
        history_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['pink'])
        history_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            history_frame,
            text="Progress History",
            font=self.fonts['heading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        # Get all progress entries
        entries = self.session.query(ProgressEntry).filter_by(
            user_id=self.user.id
        ).order_by(ProgressEntry.date.desc()).all()
        
        if entries:
            # Create weight trend chart
            dates = [entry.date for entry in reversed(entries)]
            weights_lbs = [entry.weight_kg / 0.453592 for entry in reversed(entries)]
            
            # Chart frame
            chart_info = ctk.CTkFrame(history_frame, fg_color="white")
            chart_info.pack(fill="x", pady=10, padx=20)
            
            ctk.CTkLabel(
                chart_info,
                text=f"Weight Trend - {len(entries)} entries logged",
                font=self.fonts['body'],
                text_color=self.colors['text']
            ).pack(pady=10)
            
            # Show simple trend info
            if len(entries) >= 2:
                first_weight = entries[-1].weight_kg / 0.453592
                latest_weight = entries[0].weight_kg / 0.453592
                change = latest_weight - first_weight
                
                trend_text = f"Total change: {change:+.1f} lbs"
                if change < 0:
                    trend_text += " (Lost weight!)"
                elif change > 0:
                    trend_text += " (Gained weight)"
                
                ctk.CTkLabel(
                    chart_info,
                    text=trend_text,
                    font=self.fonts['body'],
                    text_color=self.colors['text']
                ).pack(pady=5)
            
            # Show recent entries
            history_display = ctk.CTkScrollableFrame(history_frame, fg_color="white", height=200)
            history_display.pack(fill="both", expand=True, padx=20, pady=10)
            
            for entry in entries[:10]:  # Show last 10 entries
                entry_frame = ctk.CTkFrame(history_display, fg_color=self.colors['pink'])
                entry_frame.pack(fill="x", pady=5, padx=5)
                
                weight_lbs = entry.weight_kg / 0.453592
                entry_text = f"{entry.date.strftime('%m/%d/%Y')} - Weight: {weight_lbs:.1f} lbs"
                
                if entry.body_fat_percentage:
                    entry_text += f" | BF: {entry.body_fat_percentage:.1f}%"
                if entry.waist_cm:
                    waist_in = entry.waist_cm / 2.54
                    entry_text += f" | Waist: {waist_in:.1f} in"
                if entry.notes:
                    entry_text += f"\n{entry.notes}"
                
                ctk.CTkLabel(
                    entry_frame,
                    text=entry_text,
                    font=self.fonts['small'],
                    text_color=self.colors['text'],
                    justify="left"
                ).pack(side="left", padx=10, pady=5)
                
                def delete_entry(e=entry):
                    self.session.delete(e)
                    self.session.commit()
                    self.show_progress()
                
                delete_btn = ctk.CTkButton(
                    entry_frame,
                    text="Delete",
                    command=delete_entry,
                    width=60,
                    fg_color="red",
                    hover_color="#CC0000",
                    font=self.fonts['small']
                )
                delete_btn.pack(side="right", padx=5)
        else:
            ctk.CTkLabel(
                history_frame,
                text="No progress entries yet. Log your first one above!",
                font=self.fonts['body'],
                text_color=self.colors['text']
            ).pack(pady=20)
    
    def on_closing(self):
        """Handle window closing"""
        self.session.close()
        self.destroy()


if __name__ == "__main__":
    app = FitnessTrackerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
