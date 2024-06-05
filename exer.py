import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('exercises.csv')

# Function to handle rating an exercise
def rate_exercise():
    try:
        exercise_id = int(exercise_id_entry.get())
        star_rating = float(star_rating_entry.get())

        if exercise_id in df['exercise_id'].tolist():
            exercise_name = df[df['exercise_id'] == exercise_id]['exercise_name'].values[0]
            current_avg_rating = df[df['exercise_id'] == exercise_id]['star_rating'].values[0]
            num_ratings = df[df['exercise_id'] == exercise_id]['num_ratings'].values[0]
            new_avg_rating = ((current_avg_rating * num_ratings) + star_rating) / (num_ratings + 1)
            df.loc[df['exercise_id'] == exercise_id, 'star_rating'] = new_avg_rating
            df.loc[df['exercise_id'] == exercise_id, 'num_ratings'] += 1
            df.to_csv('exercises.csv', index=False)
            messagebox.showinfo("Success", f"Thank you for rating '{exercise_name}'. New average star rating: {new_avg_rating:.2f}")
        else:
            messagebox.showerror("Error", "Invalid exercise ID.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

# Function to handle exercise recommendation
def recommend_exercise():
    try:
        exercise_type = exercise_type_entry.get().strip().title()
        muscle_group = muscle_group_entry.get().strip().title()
        difficulty = difficulty_entry.get().strip().title()
        equipment_needed = equipment_needed_entry.get().strip().title()

        filtered_exercises = df.copy()

        if exercise_type:
            filtered_exercises = filtered_exercises[filtered_exercises['exercise_type'].str.lower() == exercise_type.lower()]

        if muscle_group:
            filtered_exercises = filtered_exercises[filtered_exercises['muscle_group'].str.lower() == muscle_group.lower()]

        if difficulty in ['Easy', 'Medium', 'Hard']:
            filtered_exercises = filtered_exercises[filtered_exercises['difficulty'] == difficulty]

        if equipment_needed:
            filtered_exercises = filtered_exercises[filtered_exercises['equipment_needed'].str.lower() == equipment_needed.lower()]

        if not filtered_exercises.empty:
            messagebox.showinfo("Recommended Exercises", filtered_exercises[['exercise_id', 'exercise_name', 'difficulty']].to_string(index=False))
        else:
            messagebox.showinfo("Recommended Exercises", "No exercises match the given criteria.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input.")

# Function to handle showing exercise details
def show_exercise_details():
    try:
        exercise_id = int(exercise_id_entry.get())
        if exercise_id in df['exercise_id'].tolist():
            exercise_details = df[df['exercise_id'] == exercise_id]
            messagebox.showinfo("Exercise Details", exercise_details.to_string(index=False))
        else:
            messagebox.showerror("Error", "Invalid exercise ID.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a numeric exercise ID.")

# Create the main window
root = tk.Tk()
root.title("Exercise Rating System")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

# Define a common style for labels and entries
label_style = {"font": ("Helvetica", 10, "bold"), "bg": "#f0f0f0"}
entry_style = {"font": ("Helvetica", 10)}

# Create labels and entry widgets for exercise ID and star rating
exercise_id_label = tk.Label(root, text="Exercise ID:", **label_style)
exercise_id_entry = tk.Entry(root, **entry_style)

star_rating_label = tk.Label(root, text="Star Rating (0-5):", **label_style)
star_rating_entry = tk.Entry(root, **entry_style)

# Create labels and entry widgets for exercise recommendation
exercise_type_label = tk.Label(root, text="Exercise Type:", **label_style)
exercise_type_entry = tk.Entry(root, **entry_style)

muscle_group_label = tk.Label(root, text="Muscle Group:", **label_style)
muscle_group_entry = tk.Entry(root, **entry_style)

difficulty_label = tk.Label(root, text="Difficulty (Easy, Medium, Hard):", **label_style)
difficulty_entry = tk.Entry(root, **entry_style)

equipment_needed_label = tk.Label(root, text="Equipment Needed:", **label_style)
equipment_needed_entry = tk.Entry(root, **entry_style)

# Create buttons for rating, recommendation, and details
button_style = {"font": ("Helvetica", 10, "bold"), "bg": "#4CAF50", "fg": "white", "relief": "raised"}
rate_button = tk.Button(root, text="Rate Exercise", command=rate_exercise, **button_style)
recommend_button = tk.Button(root, text="Recommend Exercises", command=recommend_exercise, **button_style)
details_button = tk.Button(root, text="Show Exercise Details", command=show_exercise_details, **button_style)

# Positioning widgets using the grid layout
exercise_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
exercise_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

star_rating_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
star_rating_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

exercise_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
exercise_type_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

muscle_group_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
muscle_group_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

difficulty_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
difficulty_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

equipment_needed_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
equipment_needed_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

rate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="we")
recommend_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="we")
details_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Start the GUI main loop
root.mainloop()
