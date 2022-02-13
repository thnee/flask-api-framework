from pathlib import Path

from invoke import task


REPO_ROOT = Path(__file__).parent


@task(aliases=["c"])
def clean(c):
    with c.cd(str(REPO_ROOT)):
        c.run("rm -rf build dist src/*.egg-info", warn=True)
        c.run("rm -rf .pytest_cache .tox .coverage", warn=True)
        c.run("find . -type d -name __pycache__ -print0 | xargs -0 rm -rf", warn=True)
        c.run("rm -rf docs/_build", warn=True)


@task(aliases=["l"])
def lint(c):
    with c.cd(str(REPO_ROOT)):
        ok = True
        print("Running flake8")
        r = c.run("flake8 .", pty=True, warn=True)
        ok = ok and r.ok
        print("Running black")
        r = c.run("black --check .", pty=True, warn=True)
        ok = ok and r.ok
        print("Running isort")
        r = c.run("isort --quiet --check .", pty=True, warn=True)
        ok = ok and r.ok
        if not ok:
            exit(1)


@task(aliases=["f"])
def fmt(c):
    with c.cd(str(REPO_ROOT)):
        c.run("black .", pty=True)
        c.run("isort .", pty=True)


@task(aliases=["t"])
def test(c):
    with c.cd(str(REPO_ROOT)):
        c.run("tox", pty=True)


@task(clean, aliases=["b"])
def build(c):
    with c.cd(str(REPO_ROOT)):
        c.run("python setup.py sdist bdist_wheel")


@task(aliases=["p"])
def publish(c, live=False):
    if live:
        url = "https://upload.pypi.org/legacy/"
    else:
        url = "https://test.pypi.org/legacy/"

    print(f"Uploading to: {url}")

    with c.cd(str(REPO_ROOT)):
        c.run(f"twine upload --repository-url '{url}' dist/*", pty=True)


@task(aliases=["d"])
def docs_auto(c):
    with c.cd(str(REPO_ROOT)):
        c.run("sphinx-autobuild docs docs/_build/html")
