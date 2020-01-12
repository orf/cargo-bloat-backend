from flask import Request, jsonify
from google.cloud.datastore import Client, Entity

client = Client()


def fetch(request: Request):
    return jsonify(ok=True)


def ingest(request: Request):
    return jsonify(ok=True)
