from flask import Flask, request, redirect
from event_reader import Reader, ConnectionException
import logging
import json

app = Flask(__name__)
reader = Reader()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())

host = '0.0.0.0'
port = 80

@app.route("/")
def index():
    page = "Please choose one of the available topics: <ul>"
    for registered_topic in reader.topics():
        page += f"<li><a href=/events/{registered_topic}>{registered_topic}</a></li>"

    page += "</ul>"
    page += 'Return to <a hfer="/">index</a>'
    return page

@app.route("/events", methods=['GET'])
def redirectToIndex():
    return redirect("/")

@app.route("/events/<topic>", methods=['GET'])
def read_event(topic):
    message={}
    try:
        message = reader.next(topic)
    except ConnectionException:
        return json.dumps({
            'status': 'connection_error',
            'message': 'Unable to read from the message stream.'}), 500

    app.logger.debug("Read this data from the stream: {0}".format(message))
    if message:
        return json.dumps(message), 200
    rooturl = '/'
    return f"Topic '{topic}' empty, Return to <a href='{rooturl}'>index</a>", 200


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
