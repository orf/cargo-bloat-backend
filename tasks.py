from invoke import task


@task
def deploy(c):
    c.run("poetry export -f requirements.txt -o requirements.txt --without-hashes", echo=True)
    c.run("gcloud functions deploy webhook --runtime python37 --trigger-http",
          pty=True, echo=True)
