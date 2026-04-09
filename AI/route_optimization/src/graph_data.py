NODES = {
    "Warehouse": {"lat": 28.6139, "lon": 77.2090},
    "School A": {"lat": 28.6203, "lon": 77.2100},
    "School B": {"lat": 28.6100, "lon": 77.2200},
    "Market": {"lat": 28.6155, "lon": 77.2250},
    "Hospital": {"lat": 28.6185, "lon": 77.2050},
    "Shelter": {"lat": 28.6080, "lon": 77.2150},
    "Community Center": {"lat": 28.6230, "lon": 77.2180},
}

# Edges represent road segments with distance in kilometers and travel time in minutes.
EDGES = [
    ("Warehouse", "School A", 4.2, 10),
    ("Warehouse", "School B", 3.8, 9),
    ("Warehouse", "Hospital", 3.5, 8),
    ("School A", "Market", 2.4, 6),
    ("School A", "Community Center", 3.0, 7),
    ("School B", "Market", 2.1, 5),
    ("School B", "Shelter", 2.8, 7),
    ("Hospital", "Shelter", 2.3, 5),
    ("Hospital", "Community Center", 3.7, 9),
    ("Market", "Community Center", 2.0, 5),
    ("Shelter", "Community Center", 2.2, 5),
]

DEFAULT_NAIVE_ORDER = ["School A", "Market", "Shelter", "Hospital", "Community Center"]
