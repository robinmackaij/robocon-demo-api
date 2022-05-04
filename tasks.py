# pylint: disable=missing-function-docstring, unused-argument
import pathlib
import subprocess
from importlib.metadata import version

from invoke import task


ROOT = pathlib.Path(__file__).parent.resolve().as_posix()
VERSION = version("robocon_demo_api")


@task
def start_api(context):
    cmd = [
        "python",
        "-m",
        "uvicorn",
        "robocon_demo_api.main:api",
        f"--app-dir {ROOT}/src/robocon_demo_api",
        "--host 0.0.0.0",
        "--port 8000",
        "--reload",
        f"--reload-dir {ROOT}/src/robocon_demo_api",
        f"--log-config {ROOT}/uvicorn_log_config.yaml",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def utests(context):
    cmd = [
        "coverage",
        "run",
        "-m",
        "unittest",
        "discover ",
        f"{ROOT}/tests/unittests",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def lint(context):
    subprocess.run(f"mypy {ROOT}", shell=True, check=False)
    subprocess.run(f"pylint {ROOT}", shell=True, check=False)


@task
def format_code(context):
    subprocess.run(f"black {ROOT}", shell=True, check=False)
    subprocess.run(f"isort {ROOT}", shell=True, check=False)


@task(format_code)
def build(context):
    subprocess.run("poetry build", shell=True, check=False)


@task(post=[build])
def bump_version(context, rule):
    subprocess.run(f"poetry version {rule}", shell=True, check=False)
    subprocess.run("poetry install", shell=True, check=False)
