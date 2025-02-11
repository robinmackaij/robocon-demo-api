FROM python:3.13-slim-bookworm

# Update the certificates
RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates && \
    update-ca-certificates

# curl is universally used and not having it may results in silent errors
RUN apt-get update && \
    apt-get install -y  --no-install-recommends curl

# git is needed to install the shared keywords / libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends git

# build-essentials is used for some Python package installs
RUN apt-get update && \
    apt-get install -y  --no-install-recommends build-essential

# Tkinter is not part of the standard lib, but e.g. the RF Dialogs library depends on it
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-tk

#  tmp files cleanup
RUN	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN	python -m pip install --upgrade pip

# Install and configure poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$PATH:$POETRY_HOME/bin"
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.in-project true
RUN poetry self update

# Install and configure uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_LINK_MODE=copy

EXPOSE 8888
ENTRYPOINT ["/bin/sh"]
