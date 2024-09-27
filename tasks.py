# pylint: disable=missing-function-docstring, unused-argument, wrong-import-position
import pathlib
import subprocess
from importlib.metadata import version

from invoke.context import Context
from invoke.tasks import task

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()
VERSION = version("robocon_demo_api")


@task
def start_api(context: Context) -> None:
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
def run_tests(context: Context) -> None:
    cmd = [
        "python",
        "-m",
        "robot",
        f"--variable=ROOT:{ROOT}",
        f"--outputdir={ROOT}/logs",
        "--loglevel=TRACE:TRACE",
        f"{ROOT}/excercises",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def exercise_log(context: Context) -> None:
    """
    Exercise: Examining the log to determine what causes the test to fail.

    Running this task (after starting the API server using the `start-api` task) should
    result in a failed test run.

    Open the generated log file (ctrl+click on the link in the terminal should work) and
    examine it to find the cause of the test failure.
    """
    cmd = [
        "python",
        "-m",
        "robot",
        f"--variable=ROOT:{ROOT}",
        f"--outputdir={ROOT}/logs",
        "--loglevel=TRACE:INFO",
        f"{ROOT}/intro_robotframework",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def lint(context: Context) -> None:
    subprocess.run(f"mypy {ROOT}", shell=True, check=False)
    subprocess.run(f"pylint {ROOT}/src/robocon_demo_api", shell=True, check=False)
    subprocess.run(f"robocop {ROOT}", shell=True, check=False)


@task
def format_code(context: Context) -> None:
    subprocess.run(f"black {ROOT}", shell=True, check=False)
    subprocess.run(f"isort {ROOT}", shell=True, check=False)
    subprocess.run(f"robotidy {ROOT}", shell=True, check=False)
