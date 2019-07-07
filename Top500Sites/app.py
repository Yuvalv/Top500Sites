import threading
import requests
import time
from flask_cors import CORS, cross_origin
from flask import Flask
from sites import Sites
from json_encoder import JSONEncoder
app = Flask(__name__)
CORS(app)

@app.before_first_request
def activate_job():
    def run_job():
        while True:
            Sites.get_data_from_site_and_store()

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/')
def get_sites_data():
    sites = Sites.get_sites_from_db()
    return JSONEncoder().encode(sites)


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == "__main__":
    start_runner()
    app.run()

