from collections import defaultdict

import requests
from configuration import intersections
from shapely.geometry import Point, LineString
from sources.bus_gps.intersection1 import predict_states as eval1
from sources.bus_gps.intersection2 import predict_states as eval2
from sources.bus_gps.intersection3 import predict_states as eval3
from sources.bus_gps.intersection4 import predict_states as eval4
from sources.bus_gps.util import geod, azimuth, get_angle, action


def get_buses():
    data = requests.get('https://gis.ee/tallinn/gps').json()

    return [
        {
            "id": elem['properties']['id'],
            "line": str(elem['properties']['line']),
            "direction": elem['properties']['direction'],
            "coordinate": Point(elem['geometry']['coordinates'])
        }
        for elem in data['features']
    ]


def filter_buses_near_intersection(intersection):
    result = defaultdict(lambda: {})
    for bus in get_buses():
        line = LineString([bus["coordinate"], intersection["coordinate"]])
        distance = geod.geometry_length(line)
        if distance <= intersection["max_bus_distance"]:
            az = azimuth(bus["coordinate"], intersection["coordinate"])
            angle = get_angle(az, bus["direction"])
            act = action(angle)
            result[bus["id"]] = {
                "line": bus["line"],
                "direction": bus["direction"],
                "distance": distance,
                "action": act
            }
    return result


def evaluate_intersection(intersection, prev_intersection_buses, curr_intersection_buses, current_intersection_evals):
    if intersection["id"] == "intersection1":
        return eval1(prev_intersection_buses, curr_intersection_buses, current_intersection_evals)
    elif intersection["id"] == "intersection2":
        return eval2(prev_intersection_buses, curr_intersection_buses, current_intersection_evals)
    elif intersection["id"] == "intersection3":
        return eval3(prev_intersection_buses, curr_intersection_buses, current_intersection_evals)
    elif intersection["id"] == "intersection4":
        return eval4(prev_intersection_buses, curr_intersection_buses, current_intersection_evals)


prev_buses = defaultdict(lambda: defaultdict(lambda: {}))
current_evals = defaultdict(lambda: {})


def process_gps():
    global current_evals, prev_buses

    curr_buses = defaultdict(lambda: defaultdict(lambda: {}))
    for intersection in intersections:
        id = intersection["id"]
        curr_buses[id] = filter_buses_near_intersection(intersection)
        current_evals[id] = evaluate_intersection(intersection, prev_buses[id], curr_buses[id], current_evals[id])

    prev_buses = curr_buses
    return current_evals
