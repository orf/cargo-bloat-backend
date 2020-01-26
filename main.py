import json
from flask import Request, jsonify
from google.cloud.datastore import Client, Entity

client = Client()


def fetch(request: Request):
    repo = request.args["repo"]
    toolchain = request.args["toolchain"]

    repo_key = client.key("Bloat", f'{repo}:{toolchain}')
    entity = client.get(repo_key)
    if entity is None:
        return jsonify({})

    entity['crates'] = json.loads(entity['crates'])
    return jsonify(entity)


def ingest(request: Request):
    repo = request.args["repo"]
    data = request.get_json()
    toolchain = data["toolchain"],
    repo_key = client.key("Bloat", f'{repo}:{toolchain}')

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
