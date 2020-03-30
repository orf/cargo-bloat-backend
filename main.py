import json
from flask import Request, jsonify
from google.cloud.datastore import Client, Entity
import logging

client = Client()

accepted_data = (
    'commit', 'rustc', 'bloat',
)


def fetch(request: Request):
    repo = request.args["repo"]
    toolchain = request.args["toolchain"]

    repo_key = client.key("Bloat", f'{repo}:{toolchain}')
    entity = client.get(repo_key)
    logging.info('Received fetch request for key %s', repo_key)
    if entity is None:
        logging.info('No entity found for key %s', repo_key)
        return jsonify({})

    entity['packages'] = json.loads(entity['packages'])
    return jsonify(entity)


def ingest(request: Request):
    repo = request.args["repo"]
    request_data = request.get_json()
    toolchain = request_data["toolchain"]
    repo_key = client.key("Bloat", f'{repo}:{toolchain}')
    logging.info('Ingesting with key %s', repo_key)

    data = {
        "packages": json.dumps(request_data['packages']),
    }
    data.update({
        key: request_data[key]
        for key in accepted_data
    })

    entity = Entity(repo_key, exclude_from_indexes=tuple(data.keys()))
    entity.update(data)
    client.put(entity)
    return jsonify(ok=True)
