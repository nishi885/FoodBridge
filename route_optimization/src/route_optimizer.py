from heapq import heappush, heappop
from typing import Dict, List, Optional, Tuple

from graph_data import EDGES, NODES, DEFAULT_NAIVE_ORDER

GraphType = Dict[str, List[Tuple[str, float, float]]]


def build_graph() -> GraphType:
    graph: GraphType = {}
    for source, target, distance_km, time_min in EDGES:
        graph.setdefault(source, []).append((target, distance_km, time_min))
        graph.setdefault(target, []).append((source, distance_km, time_min))
    return graph


def dijkstra(start: str, end: str, mode: str = "distance") -> Tuple[List[str], float, float]:
    graph = build_graph()
    if start not in graph or end not in graph:
        raise ValueError(f"Unknown location: {start} or {end}")

    distances = {start: (0.0, 0.0, None)}
    pending = [(0.0, 0.0, start)]

    while pending:
        cost, elapsed, node = heappop(pending)
        if node == end:
            break

        if distances[node][0] < cost or distances[node][1] < elapsed:
            continue

        for neighbor, seg_dist, seg_time in graph[node]:
            next_cost = seg_dist if mode == "distance" else seg_time
            candidate_cost = cost + next_cost
            candidate_time = elapsed + seg_time
            best = distances.get(neighbor)
            if best is None or (candidate_cost, candidate_time) < (best[0], best[1]):
                distances[neighbor] = (candidate_cost, candidate_time, node)
                heappush(pending, (candidate_cost, candidate_time, neighbor))

    if end not in distances:
        raise ValueError(f"No path found from {start} to {end}")

    path: List[str] = []
    current = end
    while current is not None:
        path.append(current)
        current = distances[current][2]
    path.reverse()

    total_distance_km, total_time_min, _ = distances[end]
    if mode != "distance":
        total_distance_km, total_time_min = compute_route_distance_time(path)
    else:
        total_distance_km, total_time_min = compute_route_distance_time(path)

    return path, total_distance_km, total_time_min


def compute_route_distance_time(path: List[str]) -> Tuple[float, float]:
    graph = build_graph()
    total_distance = 0.0
    total_time = 0.0

    for i in range(len(path) - 1):
        source, target = path[i], path[i + 1]
        edge = next(
            ((dist, time) for neighbor, dist, time in graph[source] if neighbor == target),
            None,
        )
        if edge is None:
            raise ValueError(f"No road segment defined between {source} and {target}")
        dist, time = edge
        total_distance += dist
        total_time += time

    return round(total_distance, 2), round(total_time, 1)


def build_naive_route(start: str, end: str, via: Optional[List[str]] = None) -> List[str]:
    if via:
        stops = [node for node in via if node not in {start, end}]
    else:
        stops = [node for node in DEFAULT_NAIVE_ORDER if node not in {start, end}]

    naive_route = [start]
    for next_stop in stops + [end]:
        segment_path, _, _ = dijkstra(naive_route[-1], next_stop, mode="distance")
        naive_route.extend(segment_path[1:])

    # Remove duplicates while preserving path order
    final_route = []
    for node in naive_route:
        if not final_route or final_route[-1] != node:
            final_route.append(node)
    return final_route


def optimize_route(
    start: str,
    end: str,
    via: Optional[List[str]] = None,
    mode: str = "distance",
) -> Dict[str, object]:
    best_path, best_distance, best_time = dijkstra(start, end, mode=mode)
    baseline_path = build_naive_route(start, end, via=via)
    baseline_distance, baseline_time = compute_route_distance_time(baseline_path)

    return {
        "start": start,
        "end": end,
        "via": via or [],
        "mode": mode,
        "best_path": best_path,
        "best_distance_km": best_distance,
        "best_time_min": best_time,
        "baseline_path": baseline_path,
        "baseline_distance_km": baseline_distance,
        "baseline_time_min": baseline_time,
        "distance_saved_km": round(max(0.0, baseline_distance - best_distance), 2),
        "time_saved_min": round(max(0.0, baseline_time - best_time), 1),
    }
