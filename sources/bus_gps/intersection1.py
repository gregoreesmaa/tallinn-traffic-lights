from sources.bus_gps.util import true_eval, decrease_confidence


def predict_states(prev_buses, curr_buses, prev_results):
    curr_results = decrease_confidence(prev_results)

    for bus_id, bus in curr_buses.items():
        id1, id2 = None, None

        if bus["line"] in ['3', '4', '24', '72']:
            approach1, approach2 = 0, 180
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor11", "foor3"

        elif bus["line"] in ['13', '20', '20A']:
            approach1, approach2 = 0, 180
            leave1, leave2 = approach1, approach2
            id1, id2 = None, "foor2"

        elif bus["line"] == '12':
            approach1, approach2 = 0, 180
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor17", "foor1"

        elif bus["line"] == '37':
            approach1, approach2 = 90, 270
            leave1, leave2 = approach1, approach2
            id1, id2 = "foor18", "foor12"

        if id1 is not None and id2 is not None:
            curr_results = true_eval(prev_buses[bus_id], bus, curr_results,
                                     approach1, approach2, leave1, leave2, id1, id2)
    return curr_results
