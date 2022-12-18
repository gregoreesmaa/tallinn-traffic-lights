import math

from configuration import lights


def opposite_state(state):
    return 'green' if state == 'red' else 'red'


def combine_probabilities(probabilities):
    return 1 - math.prod([1 - probability for probability in probabilities])


def process_logic(observations):
    results = {}

    for id, rules in lights.items():
        confidences = {
            "red": [],
            "green": []
        }

        # Add the confidence values for the current traffic light to the appropriate lists
        if id in observations:
            for observation in observations[id]:
                confidences["green"].append(observation["confidence_green"])
                confidences["red"].append(observation["confidence_red"])

        conditions = filter(lambda r: r["type"] == "condition", rules)
        for condition in conditions:
            if condition["if"] not in observations:
                continue

            light_observations = observations[condition["if"]]
            n = len(light_observations)

            confidence_sums = {
                "red": combine_probabilities([observation["confidence_red"] for observation in light_observations]),
                "green": combine_probabilities([observation["confidence_green"] for observation in light_observations])
            }

            # If the condition is satisfied, add the confidence value to the appropriate list
            if condition["has_state"] == "red" and confidence_sums["red"] > confidence_sums["green"] \
                    or condition["has_state"] == "green" and confidence_sums["green"] > confidence_sums["red"]:
                confidences[condition["state"]].append(confidence_sums[condition["has_state"]])
                confidences[opposite_state(condition["state"])].append(1 - confidence_sums[condition["has_state"]])

        # Calculate the probability of the light being red or green
        confidence_red = combine_probabilities(confidences["red"])
        confidence_green = combine_probabilities(confidences["green"])
        max_confidence = max(confidence_red, confidence_green)

        if max_confidence == 0:
            continue

        # Set the state of the light based on the highest probability
        if confidence_red > confidence_green:
            results[id] = {"state": "red", "confidence": confidence_red}
        else:
            results[id] = {"state": "green", "confidence": confidence_green}

    return results
