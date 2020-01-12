from flask import Request, jsonify
from google.cloud.datastore import Client, Entity

client = Client()


def fetch(request: Request):
    repo = request.args["repo"]
    repo_key = client.key("Bloat", repo)
    entity = client.get(repo_key)
    return jsonify(result=entity)


def ingest(request: Request):
    data = request.get_json()
    repo = data["repo"]
    repo_key = client.key("Bloat", repo)
    crates = [[c["name"], c["size"]] for c in data["crates"]]
    data = {
        "commit": data["commit"],
        "file_size": data["file_size"],
        "text_size": data["text_size"],
        "toolchain": data["toolchain"],
        "rustc": data["rustc"],
        "bloat": data["bloat"],
        "crates": crates,
    }
    entity = Entity(repo_key, exclude_from_indexes=tuple(data.keys()))
    entity.update(data)
    client.put(entity)
    return jsonify(ok=True)
