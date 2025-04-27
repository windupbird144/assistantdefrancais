FROM ghcr.io/astral-sh/uv:python3.12-bookworm
ADD . /app
WORKDIR /app
CMD ["uv", "run", "assistantdefrancais"]