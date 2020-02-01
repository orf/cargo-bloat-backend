import json
from flask import Request, jsonify
from google.cloud.datastore import Client, Entity
import google.cloud.logging
import logging

client = Client()
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()


def fetch(request: Request):
    repo = request.args["repo"]
    toolchain = request.args["toolchain"]

    repo_key = client.key("Bloat", f'{repo}:{toolchain}')
    entity = client.get(repo_key)
    logging.info('Received fetch request for key %s', repo_key)
    if entity is None:
        logging.info('No entity found for key %s', repo_key)
        return jsonify({})

    entity['crates'] = json.loads(entity['crates'])
    logging.info('Returning entity with %s crates', len(entity['crates']))
    return jsonify(entity)


def ingest(request: Request):
    repo = request.args["repo"]
    data = request.get_json()
    toolchain = data["toolchain"],
    repo_key = client.key("Bloat", f'{repo}:{toolchain}')
    logging.info('Ingesting with key %s', repo_key)

    data = {
        "commit": data["commit"],
        "file_size": data["file_size"],
        "text_section_size": data["text_section_size"],
        "rustc": data["rustc"],
        "bloat": data["bloat"],
        "crates": json.dumps(data['crates']),
    }
    entity = Entity(repo_key, exclude_from_indexes=tuple(data.keys()))
    entity.update(data)
    client.put(entity)
    return jsonify(ok=True)
