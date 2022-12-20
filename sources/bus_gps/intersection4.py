from sources.bus_gps.util import true_eval, decrease_confidence


def predict_states(prev_buses, curr_buses, prev_results):
    curr_results = decrease_confidence(prev_results)

    for bus_id, bus in curr_buses.items():
        if bus["line"] in ['1', '6', '8']:
            approach1, approach2 = 120, 300
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor13", "foor15"

        elif bus["line"] in ['34', '38']:
            approach1, approach2 = 135, 315
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor16", "foor15"

        elif bus["line"] == '49':
            approach1, approach2 = 45, 225
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor14", "foor16"

        if id1 is not None and id2 is not None:
            curr_results = true_eval(prev_buses[bus_id], bus, curr_results,
                                     approach1, approach2, leave1, leave2, id1, id2)
    return curr_results
