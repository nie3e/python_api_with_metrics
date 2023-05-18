from flask import Flask, jsonify
import prometheus_client
from prometheus_client import make_wsgi_app, Summary, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

REQUEST_TIME = Summary(
    'request_processing_seconds', 'Time spent processing request'
)
COUNTER_MAIN = Counter(
    "main_page", "Main page hits", labelnames=["code"]
)
TEST_MAIN = Counter(
    "test_page", "Test page hits", labelnames=["code"]
)
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app,
    {"/metrics": make_wsgi_app()}
)
test_counter = 0


@REQUEST_TIME.time()
@app.route("/")
def hello_world():
    COUNTER_MAIN.labels(code="200").inc()
    return jsonify({"status": "ok"})


@REQUEST_TIME.time()
@app.route("/test")
def get_metrics():
    global test_counter
    test_counter += 1

    if test_counter % 3:
        TEST_MAIN.labels(code="404").inc()
        return "Error", 404

    TEST_MAIN.labels(code="200").inc()
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9091)
