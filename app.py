import uuid

from flask import Flask, session
from rq import Queue

from helpers import save_file
from redis_worker import conn


app = Flask(__name__)
app.secret_key = "data"
q = Queue(connection=conn)


@app.before_request
def set_session_uid():
    uid = str(uuid.uuid4())
    session["uid"] = uid


@app.route("/", methods=["POST", "GET"])
def home():
    return 'app is healthy'


@app.route("/health", methods=["POST", "GET"])
def health():
    return 'app is healthy'


@app.route("/predict", methods=["POST"])
def predict():
    uid = session.get("uid")
    job = q.enqueue_call(
            func=save_file, args=(uid, ), result_ttl=500
    )
    return {"uid": uid}
