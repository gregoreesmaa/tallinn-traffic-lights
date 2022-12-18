import math

import cv2
import numpy as np

from configuration import lights

def process_feed_traffic(feed, previous_frame, current_frame, observations, feed_images):
    # Convert the images to grayscale
    previous_frame_gs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    current_frame_gs = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    for traffic_light_id, traffic_light_rules in lights.items():
        for rule_index in range(len(traffic_light_rules)):
            rule = traffic_light_rules[rule_index]

            # Only process "traffic" type rules and rules that match the current feed
            if rule["type"] != "traffic" or rule["feed"] != feed:
                continue

            # Create a mask for the current traffic light region
            mask = np.zeros((previous_frame.shape[0], previous_frame.shape[1]), dtype=np.uint8)
            cv2.fillPoly(mask, rule["polygons"], 1)

            # Find trackable points in the previous frame using the mask
            trackable_points = cv2.goodFeaturesToTrack(previous_frame_gs, 300, 0.1, 2.5, False, mask=mask)
            cv2.cornerSubPix(previous_frame_gs, trackable_points, criteria=(cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.01),
                             winSize=(5, 5), zeroZone=(-1, -1))

            tracked_points, status, error = cv2.calcOpticalFlowPyrLK(previous_frame_gs, current_frame_gs, trackable_points, None, (500, 500), maxLevel=5)

            total_distance = 0
            for i, (new_point, old_point) in enumerate(zip(tracked_points, trackable_points)):
                new_x, new_y = new_point.ravel()
                old_x, old_y = old_point.ravel()
                dx = int(old_y - new_y)
                dy = int(old_x - new_x)
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance != 0:
                    angle = math.degrees(math.acos(dx / distance))

                    # Check if the movement of the point falls within one of the specified angle ranges
                    if any(min_angle <= angle <= max_angle for min_angle, max_angle in rule["angleRanges"]):
                        total_distance += distance

                        # Annotate the frame with a line showing the movement of the point
                        feed_images[feed + "-annotated"] = cv2.line(feed_images[feed + "-annotated"], (int(new_x), int(new_y)), (int(old_x), int(old_y)), (255, 0, 0), 1)

                # Annotate the frame with a circle at the position of the point
                feed_images[feed + "-annotated"] = cv2.circle(feed_images[feed + "-annotated"], (int(new_x), int(new_y)), 3, (255, 255, 255), -1)

            # Calculate a confidence value for the presence of a red traffic light
            # based on the total distance moved by the points of interest. Distance
            # of 100 to be confidence 0.9
            confidence_red = math.e ** (-0.0000105349 * total_distance ** 2)

            # Add the observations for the current traffic light to the observations dictionary
            observations[traffic_light_id].append({
                "total_dist": total_distance,
                "confidence_red": confidence_red * 0.6,
                "confidence_green": (1 - confidence_red) * 0.6,
            })
