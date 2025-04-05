import tkinter as tk
from tkinter import messagebox
import random
from dijkstra import dijkstra
import os

HISTORY_FILE = "trip_history.txt"
trip_history = []

# Load previous history from file
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        for line in f:
            try:
                dist, time = line.strip().split(',')
                trip_history.append((float(dist), int(time)))
            except:
                continue

# Initial map layout
map_data = [
    ['.', '.', '.', '+', '.'],
    ['.', '.', '.', '.', '.'],
    ['.', 'A', '.', '.', '+'],
    ['.', '.', '.', '.', '.'],
    ['+', '.', '.', '.', '.'],
]

# Save original hospital positions
original_hospitals = [(i, j) for i in range(len(map_data)) for j in range(len(map_data[i])) if map_data[i][j] == '+']

# Create window
root = tk.Tk()
root.title("Ambulance Routing Map")
root.geometry("350x350")

# Store label widgets
labels = []

def update_map():
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            labels[i][j].config(text=map_data[i][j], bg='SystemButtonFace')

def move_ambulance():
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == 'A':
                if (i, j) in original_hospitals:
                    map_data[i][j] = '+'
                else:
                    map_data[i][j] = '.'

    empty_cells = [(i, j) for i in range(len(map_data)) for j in range(len(map_data[i])) if map_data[i][j] == '.']
    new_pos = random.choice(empty_cells)
    map_data[new_pos[0]][new_pos[1]] = 'A'
    update_map()

# Grid display
for i in range(len(map_data)):
    row_labels = []
    for j in range(len(map_data[i])):
        cell = tk.Label(root, text=map_data[i][j], width=4, height=2, font=('Arial', 14), borderwidth=1, relief="solid")
        cell.grid(row=i, column=j)
        row_labels.append(cell)
    labels.append(row_labels)

# Move Ambulance Button
move_btn = tk.Button(root, text="Move Ambulance", command=move_ambulance, font=('Arial', 12))
move_btn.grid(row=len(map_data), column=0, columnspan=5, pady=10)

def open_next_page(distance_steps):
    new_window = tk.Toplevel(root)
    new_window.title("Route Summary")
    new_window.geometry("300x200")

    distance_km = distance_steps * 5
    estimated_minutes = round(distance_km * 3)  # 1km ≈ 3 min

    # Save trip to history
    trip_history.append((distance_km, estimated_minutes))
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{distance_km},{estimated_minutes}\n")

    tk.Label(new_window, text="✅ Ambulance Reached Hospital", font=('Arial', 14, 'bold')).pack(pady=10)
    tk.Label(new_window, text=f"Distance: {distance_km} km", font=('Arial', 12)).pack(pady=5)
    tk.Label(new_window, text=f"Estimated Time: {estimated_minutes} minutes", font=('Arial', 12)).pack(pady=5)

def animate_movement(path, nearest, distance):
    def step(index):
        if index >= len(path):
            r, c = nearest
            labels[r][c].config(bg='green')
            status_label.config(text="✅ Ambulance Reached the Hospital!")
            open_next_page(distance)
            return

        r, c = path[index]

        # Remove old ambulance
        for i in range(len(map_data)):
            for j in range(len(map_data[i])):
                if map_data[i][j] == 'A':
                    if (i, j) in original_hospitals:
                        map_data[i][j] = '+'
                    else:
                        map_data[i][j] = '.'

        # Place new ambulance
        map_data[r][c] = 'A'
        update_map()
        labels[r][c].config(bg='lightblue')

        status_label.config(
            text=f"🚑 Step {index+1} of {len(path)} | At: ({r},{c}) | Distance: {(index+1)*5} km"
        )

        root.after(500, lambda: step(index + 1))

    step(0)

def search_nearest_hospital():
    ambulance_pos = None
    hospital_positions = []

    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == 'A':
                ambulance_pos = (i, j)
            elif map_data[i][j] == '+':
                hospital_positions.append((i, j))

    if ambulance_pos is None or not hospital_positions:
        print("Ambulance ya hospital position nahi mili.")
        return

    distance, path, nearest = dijkstra(map_data, ambulance_pos, hospital_positions)

    if path:
        print(f"[A] Ambulance is at: {ambulance_pos}")
        print(f"[+] Nearest hospital is at: {nearest}")
        print(f"[PATH] {path}")
        print(f"[DISTANCE] {distance} steps")
        animate_movement(path, nearest, distance)
    else:
        print("NO PATH: Koi raasta nahi mila hospital tak.")

# Search Button
search_btn = tk.Button(root, text="Search Hospital", command=search_nearest_hospital, font=('Arial', 12))
search_btn.grid(row=len(map_data)+1, column=0, columnspan=5, pady=5)

# 📋 Trip History
def show_history():
    if not trip_history:
        messagebox.showinfo("Trip History", "No trips yet.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("Trip History")
    history_window.geometry("300x250")

    tk.Label(history_window, text="📋 Trip History", font=('Arial', 14, 'bold')).pack(pady=10)

    for idx, (dist, time) in enumerate(trip_history, 1):
        tk.Label(history_window, text=f"{idx}. Distance: {dist} km | Time: {time} min", font=('Arial', 11)).pack()

# History Button
history_btn = tk.Button(root, text="View Trip History", command=show_history, font=('Arial', 11))
history_btn.grid(row=len(map_data)+3, column=0, columnspan=5, pady=5)

# Live Status Label
status_label = tk.Label(root, text="Status: Waiting for search...", font=('Arial', 11), fg='blue')
status_label.grid(row=len(map_data)+2, column=0, columnspan=5, pady=5)

# Start GUI
root.mainloop()
