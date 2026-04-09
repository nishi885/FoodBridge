from heapq import heappop, heappush
from itertools import permutations
from typing import Dict, List, Optional, Tuple

from graph_data import DEFAULT_NAIVE_ORDER, EDGES

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


def _merge_segments(paths: List[List[str]]) -> List[str]:
    merged: List[str] = []
    for segment in paths:
        if not segment:
            continue
        if not merged:
            merged.extend(segment)
        else:
            merged.extend(segment[1:])
    return merged


def _build_route_for_stop_order(stops: List[str], mode: str) -> Tuple[List[str], float, float]:
    segment_paths: List[List[str]] = []
    for source, target in zip(stops, stops[1:]):
        segment_path, _, _ = dijkstra(source, target, mode=mode)
        segment_paths.append(segment_path)

    full_path = _merge_segments(segment_paths)
    total_distance_km, total_time_min = compute_route_distance_time(full_path)
    return full_path, total_distance_km, total_time_min


def build_naive_route(start: str, end: str, via: Optional[List[str]] = None) -> List[str]:
    if via:
        stops = [node for node in via if node not in {start, end}]
    else:
        stops = [node for node in DEFAULT_NAIVE_ORDER if node not in {start, end}]

    naive_route, _, _ = _build_route_for_stop_order([start, *stops, end], mode="distance")
    return naive_route


def optimize_route(
    start: str,
    end: str,
    via: Optional[List[str]] = None,
    mode: str = "distance",
) -> Dict[str, object]:
    requested_via = [node for node in (via or []) if node not in {start, end}]

    if requested_via:
        best_result = None
        for candidate_order in permutations(requested_via):
            path, distance_km, time_min = _build_route_for_stop_order(
                [start, *candidate_order, end],
                mode=mode,
            )
            candidate_metric = distance_km if mode == "distance" else time_min
            if best_result is None or candidate_metric < best_result["metric"]:
                best_result = {
                    "path": path,
                    "distance_km": distance_km,
                    "time_min": time_min,
                    "ordered_via": list(candidate_order),
                    "metric": candidate_metric,
                }

        best_path = best_result["path"]
        best_distance = best_result["distance_km"]
        best_time = best_result["time_min"]
        optimized_via_order = best_result["ordered_via"]
    else:
        best_path, best_distance, best_time = dijkstra(start, end, mode=mode)
        optimized_via_order = []

    baseline_path = build_naive_route(start, end, via=requested_via or None)
    baseline_distance, baseline_time = compute_route_distance_time(baseline_path)

    return {
        "start": start,
        "end": end,
        "via": requested_via,
        "optimized_via_order": optimized_via_order,
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
