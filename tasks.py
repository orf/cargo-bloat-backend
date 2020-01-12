from invoke import task


@task
def deploy(c):
    commands = (
        "poetry export -f requirements.txt -o requirements.txt --without-hashes",
        "gcloud --quiet functions deploy webhook --runtime python37 --trigger-http",
        "gcloud --quiet functions deploy fetch --runtime python37 --trigger-http",
        "gcloud --quiet functions deploy ingest --runtime python37 --trigger-http",
    )
    for cmd in commands:
        c.run(cmd, echo=True)
