import cv2
import numpy as np

from configuration import lights

lower_red, upper_red = np.array([0, 10, 150]), np.array([8, 255, 255])
lower_red_2, upper_red_2 = np.array([140, 10, 150]), np.array([180, 255, 255])
lower_green, upper_green = np.array([32, 10, 150]), np.array([128, 255, 255])  # Including blue tones as well
lower_bright, upper_bright = np.array([0, 0, 200]), np.array([180, 50, 255])


def create_gaussian_kernel(size, stddev=1.0, mean=0):
    # Inspired by https://www.geeksforgeeks.org/how-to-generate-2-d-gaussian-array-using-numpy/
    # create a mesh grid of x and y values
    x_values, y_values = np.meshgrid(np.linspace(-1, 1, size[1]), np.linspace(-1, 1, size[0]))

    # compute the distance from the mean for each point in the mesh grid
    distance_from_mean = np.sqrt(x_values ** 2 + y_values ** 2)

    # compute the coefficient for the exponential term in the gaussian function
    coefficient = 1 / (2 * np.pi * stddev ** 2)

    # compute the gaussian kernel
    kernel = np.exp(-((distance_from_mean - mean) ** 2 / (2 * stddev ** 2))) * coefficient

    # normalize the kernel
    return kernel / kernel.sum()


def get_square_around_point(point, side_length=30):
    return slice(max(0, point[1] - side_length), max(0, point[1] + side_length)), \
           slice(max(0, point[0] - side_length), max(0, point[0] + side_length))


def process_feed_direct(feed, img, observations, light_images):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = (cv2.inRange(img_hsv, lower_red, upper_red) + cv2.inRange(img_hsv, lower_red_2, upper_red_2)) / 255
    green_mask = cv2.inRange(img_hsv, lower_green, upper_green) / 255
    brightness_mask = cv2.inRange(img_hsv, lower_bright, upper_bright) / 255

    for traffic_light_id, traffic_light_rules in lights.items():
        for rule_index in range(len(traffic_light_rules)):
            rule = traffic_light_rules[rule_index]

            # Only process "direct" type rules and rules that match the current feed
            if rule["type"] != "direct" or rule["feed"] != feed:
                continue

            light_rule_id = traffic_light_id + "-" + str(rule_index)

            # Find slice size based on distance between the lights, if not overridden.
            lights_dist = (
                                  (rule["red_pos"][0] - rule["green_pos"][0]) ** 2 +
                                  (rule["red_pos"][1] - rule["green_pos"][1]) ** 2
                          ) ** 0.5
            slice_size = rule["slice_size"] if "slice_size" in rule else int(lights_dist / 2)

            # Get the slices around the red and green lights
            red_slice = get_square_around_point(rule["red_pos"], side_length=slice_size)
            green_slice = get_square_around_point(rule["green_pos"], side_length=slice_size)

            # Get color and brightness values for red and green slices
            red_light_color_mask = red_mask[red_slice]
            red_light_brightness_mask = brightness_mask[red_slice]
            green_light_color_mask = green_mask[green_slice]
            green_light_brightness_mask = brightness_mask[green_slice]

            # Create Gaussian kernels for weighted detection
            color_stddev = 0.5
            brightness_stddev = 0.2
            red_light_color_kernel = create_gaussian_kernel(red_light_color_mask.shape, stddev=color_stddev)
            red_light_brightness_kernel = create_gaussian_kernel(red_light_brightness_mask.shape, stddev=brightness_stddev)
            green_light_color_kernel = create_gaussian_kernel(green_light_color_mask.shape, stddev=color_stddev)
            green_light_brightness_kernel = create_gaussian_kernel(green_light_brightness_mask.shape, stddev=brightness_stddev)

            # Apply multipliers to the color and brightness values
            red_light_brightness_mask = red_light_brightness_mask * (rule["brightness_multiplier"] if "brightness_multiplier" in rule else 1)
            green_light_brightness_mask = green_light_brightness_mask * (rule["brightness_multiplier"] if "brightness_multiplier" in rule else 1)
            red_light_color_mask = red_light_color_mask * (rule["color_multiplier"] if "color_multiplier" in rule else 1)
            green_light_color_mask = green_light_color_mask * (rule["color_multiplier"] if "color_multiplier" in rule else 1)

            # Apply the Gaussian kernels to the color and brightness squares
            red_result = np.maximum(red_light_color_kernel * red_light_color_mask,
                                    red_light_brightness_kernel * red_light_brightness_mask)
            green_result = np.maximum(green_light_color_kernel * green_light_color_mask,
                                      green_light_brightness_kernel * green_light_brightness_mask)

            # Store results for visualization
            light_images[light_rule_id] = {
                "red": {
                    "source": img[red_slice],
                    "color": red_light_color_mask,
                    "brightness": red_light_brightness_mask,
                    "result": red_result
                },
                "green": {
                    "source": img[green_slice],
                    "color": green_light_color_mask,
                    "brightness": green_light_brightness_mask,
                    "result": green_result
                }
            }

            # Calculate the total activity values for the red and green lights
            v_red = np.sum(red_result)
            v_green = np.sum(green_result)
            v_sum = v_red + v_green

            measurement_confidence = rule["confidence"] if "confidence" in rule else 1

            if v_sum == 0:
                continue

            if v_red < 0.05 and v_green < 0.05:
                # If too few of both lights, assume red with confidence corresponding to its brightness as follows: 0.05 -> 0.5, 0.0 -> 1
                confidence_red = 1048576 ** -v_red
                confidence_green = 1 - confidence_red
            elif min(v_red, v_green) > 0 and max(v_red, v_green) / min(v_red, v_green) < 2:
                # If lights have similar activities, assume red with increasing confidence, the closer the values are.
                confidence_red = min(v_red, v_green) / max(v_red, v_green)
                confidence_green = 1 - confidence_red
            else:
                # Normally, use relativistic activities as confidences
                confidence_red = v_red / v_sum
                confidence_green = v_green / v_sum

            # Append the confidence values to the list of observations
            observations[traffic_light_id].append({
                "v_red": v_red,
                "v_green": v_green,
                "confidence_red": measurement_confidence * confidence_red,
                "confidence_green": measurement_confidence * confidence_green,
            })
