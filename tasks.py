# pylint: disable=missing-function-docstring, unused-argument, wrong-import-position
# monkey-patch for 3.11 compatibility, see https://github.com/pyinvoke/invoke/issues/833
import inspect

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec  # type: ignore[attr-defined]

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
def run_tests(context):
    cmd = [
        "python",
        "-m",
        "robot",
        f"--variable=ROOT:{ROOT}",
        f"--outputdir={ROOT}/excercises/logs",
        "--loglevel=TRACE:TRACE",
        f"{ROOT}/excercises",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def lint(context):
    subprocess.run(f"mypy {ROOT}", shell=True, check=False)
    subprocess.run(f"pylint {ROOT}/src/robocon_demo_api", shell=True, check=False)


@task
def format_code(context):
    subprocess.run(f"black {ROOT}", shell=True, check=False)
    subprocess.run(f"isort {ROOT}", shell=True, check=False)
