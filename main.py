import tkinter as tk
from tkintermapview import TkinterMapView
import json
import random
import math

# GUI window setup
root = tk.Tk()
root.title("City Map - Ambulance Routing")
root.geometry("800x600")

# Create map widget
map_widget = TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# ------------------ Helper Function: Haversine ------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# ------------------ Default Location ------------------
default_lat = 26.9124
default_lon = 75.7873
map_widget.set_position(default_lat, default_lon)
map_widget.set_zoom(13)

# ------------------ Load Hospitals from JSON ------------------
with open("hospital_data.json", "r") as f:
    hospital_data = json.load(f)

hospital_markers = []
for hospital in hospital_data:
    marker = map_widget.set_marker(hospital["lat"], hospital["lon"], text=hospital["name"])
    hospital_markers.append({
        "name": hospital["name"],
        "lat": hospital["lat"],
        "lon": hospital["lon"],
        "marker": marker
    })

# ------------------ Ambulance Setup ------------------
ambulance_position = [default_lat + random.uniform(-0.01, 0.01), default_lon + random.uniform(-0.01, 0.01)]
ambulance_marker = map_widget.set_marker(
    ambulance_position[0], ambulance_position[1],
    text="🚑 Ambulance", marker_color_circle="red", marker_color_outside="black"
)

# ------------------ Path & Info Setup ------------------
path_line = None
target_hospital = None

# ------------------ Functions ------------------

# Move ambulance randomly
def place_ambulance_random():
    global ambulance_marker, ambulance_position
    rand_lat = default_lat + random.uniform(-0.01, 0.01)
    rand_lon = default_lon + random.uniform(-0.01, 0.01)
    ambulance_position = [rand_lat, rand_lon]

    if ambulance_marker:
        ambulance_marker.delete()

    ambulance_marker = map_widget.set_marker(rand_lat, rand_lon, text="🚑 Ambulance", marker_color_circle="red", marker_color_outside="black")

# Search nearest hospital & draw path
def search_nearest_hospital():
    global path_line, target_hospital
    min_dist = float("inf")
    nearest = None
    for hospital in hospital_markers:
        dist = haversine(ambulance_position[0], ambulance_position[1], hospital["lat"], hospital["lon"])
        if dist < min_dist:
            min_dist = dist
            nearest = hospital
    target_hospital = nearest

    # Draw blue line path
    if path_line:
        map_widget.delete(path_line)
    path_line = map_widget.set_path([ambulance_position, [nearest["lat"], nearest["lon"]]])

    info_label.config(text=f"📍 Distance: {round(min_dist, 2)} km | ETA: {round(min_dist * 2, 1)} mins")

# Move ambulance toward hospital
def start_movement():
    if not target_hospital:
        return
    steps = 20
    lat_diff = (target_hospital["lat"] - ambulance_position[0]) / steps
    lon_diff = (target_hospital["lon"] - ambulance_position[1]) / steps

    def move(step=0):
        if step >= steps:
            return
        ambulance_position[0] += lat_diff
        ambulance_position[1] += lon_diff
        ambulance_marker.set_position(ambulance_position[0], ambulance_position[1])
        root.after(200, lambda: move(step + 1))

    move()

# ------------------ Buttons and Info Label ------------------
frame = tk.Frame(root)
frame.pack(pady=10)

info_label = tk.Label(frame, text="📍 Distance: - | ETA: -", font=("Arial", 12))
info_label.pack(pady=5)

move_button = tk.Button(frame, text="Move Ambulance", font=("Arial", 12), command=place_ambulance_random)
move_button.pack(side="left", padx=10)

search_button = tk.Button(frame, text="Search Hospital", font=("Arial", 12), command=search_nearest_hospital)
search_button.pack(side="left", padx=10)

start_button = tk.Button(frame, text="Start", font=("Arial", 12), command=start_movement)
start_button.pack(side="left", padx=10)

# ------------------ Run GUI ------------------
root.mainloop()
