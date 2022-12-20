from sources.cam_feeds.main import process_feed
from sources.bus_gps.main import process_gps

gps_results = {}

def process_sources(timestep, observations):
    global gps_results

    feed_results = process_feed()

    gps_results = process_gps() if timestep % 5 == 0 else gps_results

    for id, results in feed_results.items():
        observations[id] += results
    for intersection_id, intersection_observations in gps_results.items():
        for id, result in intersection_observations.items():
            observations[id] += [result]

