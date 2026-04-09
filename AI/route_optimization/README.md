# Route Optimization

This folder implements a standalone route optimization service using Dijkstra's algorithm.
It returns the best route between locations, calculates total distance and travel time, and renders a map view.

## Features

- Dijkstra algorithm for shortest path optimization
- Route map visualization using `folium`
- Distance + time saved compared to a naive route
- Separate folder from the demand prediction model

## Installation

```bash
cd route_optimization
pip install -r requirements.txt
```

## Run the service

```bash
python src/api_server.py
```

## Endpoints

### `POST /optimize`

Request body:

```json
{
  "start": "Warehouse",
  "end": "Community Center",
  "via": ["School A", "Market"],
  "mode": "distance"
}
```

Response includes:
- `best_path`
- `total_distance_km`
- `total_time_min`
- `baseline_distance_km`
- `baseline_time_min`
- `distance_saved_km`
- `time_saved_min`

### `POST /route-map`

Request body is the same as `/optimize`.
Returns an HTML map of the best route.

## Sample nodes

- Warehouse
- School A
- School B
- Market
- Hospital
- Shelter
- Community Center

## Notes

- Distance/time savings are computed against a naive route that visits the requested via nodes (or default stops) in order.
- The map endpoint returns an interactive route map that can be opened in a browser.
