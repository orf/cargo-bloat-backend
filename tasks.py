from invoke import task
import tempfile


@task
def deploy(c, env="prod"):
    temp_dir = tempfile.mkdtemp()
    c.run("poetry export -f requirements.txt -o requirements.txt --without-hashes", echo=True)
    c.run("poetry run chalice package %s" % temp_dir)
    c.run("aws cloudformation package "
          "--template-file=%s/sam.json "
          "--s3-bucket=cargo-bloat-deploy "
          "--output-template-file=%s/packaged.yaml" % (temp_dir, temp_dir),
          pty=True, echo=True)
    c.run("aws cloudformation deploy --template-file=%s/packaged.yaml "
          "--stack-name=cargo-bloat-%s "
          "--capabilities CAPABILITY_IAM" % (temp_dir, env),
          pty=True, echo=True)
