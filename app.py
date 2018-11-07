# from models import Test
import datetime
from flask import Flask, Response, make_response, jsonify
from prometheus_client import (generate_latest,
                               CONTENT_TYPE_LATEST,
                               Counter, Summary)

application = Flask(__name__)

COUNTER_EVEN = Counter('ws_srv_is_now_even',
                           'count even now aligned on second',
                           ['even'])

COUNT_FCT = Summary('ws_srv_func', 'stats of the index function')

@application.route('/')
@COUNT_FCT.time()
def index():
    """Now service to get date time on the server."""

    now = datetime.datetime.now()

    if int(now.timestamp()) % 2 == 0:
        COUNTER_EVEN.labels(even='yes').inc()
    else:
        COUNTER_EVEN.labels(even='no').inc()

    return make_response(jsonify({
        'date': str(now)
    }), 200)


@application.route('/metrics')
def metrics():
    """Flask endpoint to gather the metrics, will be called by Prometheus."""
    return Response(generate_latest(),
                    mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    application.run()
