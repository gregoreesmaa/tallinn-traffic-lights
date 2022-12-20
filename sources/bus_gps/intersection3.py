from sources.bus_gps.util import true_eval, decrease_confidence

def predict_states(prev_buses, curr_buses, prev_results):
    curr_results = decrease_confidence(prev_results)

    for bus_id, bus in curr_buses.items():
        if bus["line"] in ['1', '5', '8', '34', '38']:
            approach1, approach2 = 0, 180
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor8", "foor7"

        elif bus["line"] in ['29', '35', '44', '51', '60', '63', '66']:
            approach1, approach2 = 0, 180
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor9", "foor6"

        if id1 is not None and id2 is not None:
            curr_results = true_eval(prev_buses[bus_id], bus, curr_results,
                                     approach1, approach2, leave1, leave2, id1, id2)
    return curr_results