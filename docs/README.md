## Preparing your system for this workshop

### Option 1 (recommended): VS Code devcontainer
> Note: this requires Docker to be installed / running on your system

Download and install VS Code: https://code.visualstudio.com/download

After installing, open VS Code and clone this repo:
* press `ctrl + shift + P`
* type `git clone` and select the `Git: Clone` command
* paste the url for this repo in the prompt bar: https://github.com/robinmackaij/robocon-demo-api

Once the repo has been cloned, you can open it when prompted.
After the repo opens, a dialog should pop up in the lower right corner asking if you
want to install the recommended Extensions for this repo.
After installing the recommended Extensions, you should be prompted again, this time
with the question if you want to open the repo in a devcontainer.
If this is not the case, press `ctrl + shift + P` and type `reopen container` which
should find the command to build the devcontainer and open the repo in the container.

Once building the container has finished, you should be able to proceed to the section
`Running the API server using poetry and invoke` to check if everything works as expected.

### Option 2: Python + poetry in a local virtual environment
This repo uses [poetry](https://python-poetry.org/) for Python environment isolation and package management.
Before poetry can be installed, Python must be installed. The minimum version to be installed can be found in the `pyproject.toml` file.
For this workshop Python 3.10 or higher is required.
The appropriate download for your OS can be found [here](https://www.python.org/downloads/).

After installing Python, poetry can be installed. For OSX/ Linux / bashonwindows the command is:

```curl
curl -sSL https://install.python-poetry.org | python3 -
```

For Windows the PowerShell command is:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

To ensure the install succeeded, you can open a new shell and run
```
poetry --version
```
> Windows users: if this does not work, see https://python-poetry.org/docs/#installing-with-the-official-installer point 3

Next poetry can be configured to create virtual environments for repos within the repo
(this makes it easy to locate the .venv for a given repo if you want to clean / delete it):
```
poetry config virtualenvs.in-project true
```
Now that poetry is set up, the project's Python dependencies can be installed:
```
poetry install
```

### Optional (recommended): VS Code user settings
In the repo there is a `.vscode` folder with in it an `example.settings.json` file.
Copy this file and rename it to `settings.json` to have a
default set of launch / debug configurations and base settings.

## Running the API server using poetry and invoke

In addition to poetry, the [invoke](http://www.pyinvoke.org/index.html) package is used to
create tasks that can be ran on all platforms in the same manner. These tasks are defined in
the `tasks.py` file in the root of the repo. To see which tasks are available, run
```
poetry run inv --list
```
> If the `.venv` is activated in the current shell, this can be shortened to `inv --list`


Further information / documentation of the tasks (if available) can be shown using
```
poetry run inv --help <task_name>
```

To start the API server used for the workshop, simply run
```
poetry run inv start-api
```
Once the API server has started, you can connect to the Swagger UI at http://127.0.0.1:8000/docs#/
