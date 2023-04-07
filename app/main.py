from flask import Flask, jsonify
from prometheus_client import start_http_server, Summary, Counter
import uuid

API_UUID = uuid.uuid4()
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
COUNTER_MAIN = Counter(
    "main_page", "Main page hits", labelnames=["uuid", "code"]
)
TEST_MAIN = Counter(
    "test_page", "Test page hits", labelnames=["uuid", "code"]
)


app = Flask(__name__)

test_counter = 0


@REQUEST_TIME.time()
@app.route("/")
def hello_world():
    COUNTER_MAIN.labels(code="200", uuid=API_UUID).inc()
    return jsonify({"status": "ok"})


@REQUEST_TIME.time()
@app.route("/test")
def get_metrics():
    global test_counter
    test_counter += 1

    if test_counter % 3:
        TEST_MAIN.labels(code="404", uuid=API_UUID).inc()
        return "Error", 404

    TEST_MAIN.labels(code="200", uuid=API_UUID).inc()
    return "ok", 200


if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=9091)