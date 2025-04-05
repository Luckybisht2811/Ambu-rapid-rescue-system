# 5x5 map: 0 = road, 1 = building, 'H' = hospital
grid_map = [
    [0, 0, 1, 0, 'H'],     # Hospital 1
    [1, 0, 1, 0, 0],
    [0, 0, 'H', 1, 0],     # Hospital 2
    [0, 1, 0, 0, 0],
    ['H', 0, 'H', 0, 0]    # Hospital 3 and 4
]

# 🚑 Ambulance ki starting position (row, col)
ambulance_position = (3, 0)

# 🏥 Hospitals ki list of positions
hospitals = [
    (0, 4),   # Hospital 1
    (2, 2),   # Hospital 2
    (4, 0),   # Hospital 3
    (4, 2)    # Hospital 4
]

