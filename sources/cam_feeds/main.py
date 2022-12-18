from collections import defaultdict
from urllib.request import urlopen

import cv2
import numpy as np
from configuration import intersections
from sources.cam_feeds.direct import process_feed_direct
from sources.cam_feeds.traffic import process_feed_traffic
from sources.cam_feeds.visualization import visualize


def do_process_feed(feed, observations, prev_feed_images, feed_images, light_images):
    req = urlopen('https://ristmikud.tallinn.ee/last/' + feed + '.jpg')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)

    feed_images[feed] = img
    feed_images[feed + "-annotated"] = np.copy(img)

    process_feed_direct(feed, img, observations, light_images)
    if feed in prev_feed_images:
        process_feed_traffic(feed, prev_feed_images[feed], img, observations, feed_images)


prev_feed_images = {}


def process_feed():
    global prev_feed_images
    observations = defaultdict(lambda: [])
    feed_images = {}
    light_images = {}

    # Loop all feeds.
    feeds = [feed for intersection in intersections for feed in intersection["feeds"]]
    for feed in feeds:
        try:
            do_process_feed(feed, observations, prev_feed_images, feed_images, light_images)
        except Exception as e:
            # traceback.print_exc()
            print("Failed to process", feed, str(e))

    # Does not work in background thread :(
    # visualize(feeds, feed_images, light_images)

    prev_feed_images = feed_images
    return observations
