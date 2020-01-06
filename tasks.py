from invoke import task, Context


@task
def deploy(c):
    c.run("poetry export -f requirements.txt -o requirements.txt --without-hashes", echo=True)
    c.run("chalice deploy --stage=prod --api-gateway-stage=prod", pty=True, echo=True)
