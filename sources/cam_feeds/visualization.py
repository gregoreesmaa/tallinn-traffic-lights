import cv2
import numpy as np

from configuration import lights


def overlay(img1, img2, pos):
    # Inspired by https://stackoverflow.com/a/14102014/4466695
    img1[pos[1]:pos[1] + img2.shape[0], pos[0]:pos[0] + img2.shape[1]] = img2


def thumbnail(img, size=50):
    h = img.shape[0]
    w = img.shape[1]
    ar = w / h
    if ar < 1:
        new_h = size
        new_w = new_h * ar
    else:
        new_w = size
        new_h = new_w / ar

    return cv2.resize(img, (int(new_w), int(new_h)))


def visualize_feed(feed, feed_images):
    for id, rules in lights.items():
        for rule_idx in range(len(rules)):
            rule = rules[rule_idx]
            if rule["type"] != "direct" or rule["feed"] != feed:
                continue

            cv2.putText(feed_images[feed + "-annotated"],
                        id + "-" + str(rule_idx),
                        rule["green_pos"],
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (147, 20, 255),
                        2,
                        cv2.LINE_AA)

    dim = feed_images[feed + "-annotated"].shape
    res = cv2.resize(feed_images[feed + "-annotated"], (int(dim[1] * 300.0 / dim[0]), 300))
    cv2.imshow(feed, res)


def visualize_analysis(light_images):
    y = 0
    lights_monitor_img = np.ones(((len(light_images.keys())) * 50 * 2, 200 + 4 * 50, 3), dtype=np.uint8) * 255
    for light_id, redgreen in light_images.items():
        for name, rg_images in redgreen.items():
            rg_id = light_id + "-" + name
            cv2.putText(lights_monitor_img, rg_id, (0, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            overlay(lights_monitor_img, thumbnail(rg_images["source"]), (200, y))
            overlay(lights_monitor_img, thumbnail(cv2.cvtColor((rg_images["color"] * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)), (250, y))
            overlay(lights_monitor_img, thumbnail(cv2.cvtColor((rg_images["brightness"] * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)), (300, y))
            overlay(lights_monitor_img, thumbnail(cv2.cvtColor((rg_images["result"] * 2550).astype(np.uint8), cv2.COLOR_GRAY2BGR)), (350, y))
            y += 50

    cv2.imshow("Lights monitor", lights_monitor_img)


def visualize(feeds, feed_images, light_images):
    for feed in feeds:
        visualize_feed(feed, feed_images)
    try:
        visualize_analysis(light_images)
    except:
        pass
