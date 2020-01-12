from flask import Request, jsonify
from google.cloud.datastore import Client, Entity

client = Client()


def fetch(request: Request):
    return "Hello World!"


def ingest(request: Request):
    return "Hello World!"
