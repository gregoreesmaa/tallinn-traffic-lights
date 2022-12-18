import numpy as np
import pyproj

crs_web = pyproj.CRS.from_epsg('3857')
crs_gps = pyproj.CRS.from_epsg('4326')
geod = pyproj.Geod(ellps="WGS84")


def azimuth(point1, point2):
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360


def get_angle(az1, az2):
    positive = abs(min(az1 - az2, az2 - az1)) % 360
    return positive if positive < 180 else 360 - positive


def action(angle):
    return 'approaching' if angle < 90 else 'leaving'


def true_eval(prev_bus, curr_bus, curr_results, approach1, approach2, leave1, leave2, id1, id2):
    if curr_bus["action"] == 'approaching' and prev_bus:
        if approach1 < curr_bus["direction"] < approach2:
            curr_results[id1] = green() if prev_bus["distance"] - curr_bus["distance"] > 50 else red()
        else:
            curr_results[id2] = green() if prev_bus["distance"] - curr_bus["distance"] > 50 else red()
    elif curr_bus["action"] == 'leaving':
        if leave1 < curr_bus["direction"] < leave2:
            curr_results[id1] = green()
        else:
            curr_results[id2] = green()
    return curr_results


def decrease_confidence(results):
    for id, result in results.items():
        result["confidence"] = 0 if round(result["confidence"], 3) <= 0 else result["confidence"] - 1 / 12
    return results


def green():
    return {
        "state": "green",
        "confidence": 1
    }


def red():
    return {
        "state": "red",
        "confidence": 1
    }
