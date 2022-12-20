import time
import threading
from collections import defaultdict

import cv2
from flask import Flask

from logic import process_logic
from sources.main import process_sources

app = Flask(__name__)

results = {}


@app.route("/")
def get_states():
    return results



def run_loop(timestep):
    observations = defaultdict(lambda: [])

    process_sources(timestep, observations)

    results = process_logic(dict(observations))

    return results


def background_loop():
    global results
    timestep = 0

    while True:
        try:
            start = time.time()
            results = run_loop(timestep)
            delta = time.time() - start

            sleepTime = 1 - delta
            if sleepTime > 0:
                time.sleep(sleepTime)

            if cv2.waitKey(10) == ord('q'):
                print('User input "q" - quit terminating the application ...')
                break

            timestep += 1
        except KeyboardInterrupt:
            pass

    cv2.destroyAllWindows()


if __name__ == "__main__":
    #background_loop()
    threading.Thread(target=background_loop, args=[]).start()
    app.run(host='localhost', port='8080')

