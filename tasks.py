from invoke import task


@task
def deploy(c):
    c.run(
        "poetry export -f requirements.txt -o requirements.txt --without-hashes",
        echo=True,
    )
    c.run(
        "gcloud --quiet functions deploy webhook --runtime python37 --trigger-http",
        echo=True,
    )
    c.run(
        "gcloud --quiet functions deploy fetch --runtime python37 --trigger-http",
        echo=True,
    )
