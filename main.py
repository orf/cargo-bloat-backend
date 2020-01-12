import json
from flask import Request, jsonify
from google.cloud.datastore import Client, Entity

client = Client()


def fetch(request: Request):
    repo = request.args["repo"]
    repo_key = client.key("Bloat", repo)
    entity = client.get(repo_key)
    return jsonify(result=entity)


def ingest(request: Request):
    repo = request.args["repo"]
    repo_key = client.key("Bloat", repo)
    data = request.get_json()
    data = {
        "commit": data["commit"],
        "file-size": data["file-size"],
        "text-section-size": data["text-section-size"],
        "toolchain": data["toolchain"],
        "rustc": data["rustc"],
        "bloat": data["bloat"],
        "crates": json.dumps(data['crates']),
    }
    entity = Entity(repo_key, exclude_from_indexes=tuple(data.keys()))
    entity.update(data)
    client.put(entity)
    return jsonify(ok=True)
