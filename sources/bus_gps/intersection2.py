from sources.bus_gps.util import decrease_confidence, green, red


def predict_states(prev_buses, curr_buses, prev_results):
    curr_results = decrease_confidence(prev_results)

    actions = [curr_buses[bus]["action"] for bus in curr_buses]
    if 'leaving' in actions:
        curr_results = {"foor5": green()}
    else:
        for bus in curr_buses:
            if bus in prev_buses:
                if prev_buses[bus]["distance"] - curr_buses[bus]["distance"] > 50:
                    # kui buss pole ristmikku ületanud ja liigub rohkem kui 50 meetrit eelmisest mõõtmisest
                    curr_results = {"foor5": green()}
                else:
                    curr_results = {"foor5": red()}
                break
    return curr_results
