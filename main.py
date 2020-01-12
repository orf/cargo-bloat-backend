from flask import Request, jsonify
from google.cloud import datastore

client = datastore.Client()


def handle_installation(data: dict):
    action = data['action']
    install_id = data['installation']['id']
    install_key = client.key("Installation", install_id)
    if action == "deleted":
        client.delete(install_key)
        return jsonify(status="deleted install")
    elif action == "created":
        repo_names = [r['full_name'] for r in data['repositories']]
        install_object = datastore.Entity(key=install_key, exclude_from_indexes=("account",))
        install_object['repos'] = repo_names
        install_object['user'] = data['installation']['account']['login']
        client.put(install_object)
        return jsonify(status="created install")
    return jsonify(error=f'unhandled action {action}'), 400


def handle_installation_repositories(data: dict):
    install_id = data['installation']['id']
    install_key = client.key("Installation", install_id)
    added = {r['full_name'] for r in data['repositories_added']}
    removed = {r['full_name'] for r in data['repositories_removed']}
    install_object = datastore.Entity(key=install_key)
    install_object['repos'] = list((set(install_object['repos']) | added) - removed)
    client.put(install_object)
    return jsonify(status='updated install')


def webhook(request: Request):
    data = request.get_json()
    event = request.headers['X-GitHub-Event']

    if event == "installation":
        return handle_installation(data)
    elif event == "installation_repositories":
        return handle_installation_repositories(data)
    else:
        return jsonify(status="unhandled")


def fetch(request: Request):
    return 'Hello World!'
