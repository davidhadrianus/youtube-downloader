# youtube-downloader
YouTube Downloader

# Instala dependências principais
uv add yt-dlp rich typer python-dotenv

# Instala dependências de desenvolvimento
uv add --group dev ruff mypy black pytest pytest-mock pre-commit

# Verifica instalação
uv run python --version

# Inicializa pre-commit
uv run pre-commit install
