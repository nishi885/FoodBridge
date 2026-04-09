from typing import List

import folium

from graph_data import NODES


def build_route_map(path: List[str]) -> str:
    if not path:
        raise ValueError("Path must contain at least one waypoint")

    coords = [(NODES[node]["lat"], NODES[node]["lon"]) for node in path]
    center_lat = sum(lat for lat, _ in coords) / len(coords)
    center_lon = sum(lon for _, lon in coords) / len(coords)

    route_map = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    for index, node in enumerate(path, start=1):
        folium.Marker(
            location=[NODES[node]["lat"], NODES[node]["lon"]],
            popup=f"{index}. {node}",
            tooltip=node,
            icon=folium.Icon(color="blue" if index == 1 or index == len(path) else "green", icon="road", prefix="fa"),
        ).add_to(route_map)

    folium.PolyLine(coords, color="dodgerblue", weight=5, opacity=0.8).add_to(route_map)

    return route_map._repr_html_()
