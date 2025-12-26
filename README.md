# YouTube Downloader

A robust and user-friendly CLI tool to download videos and audio from YouTube, built with Python.

**Author:** David Hadrianus

## Features

- 🚀 **High Performance**: Built on top of the powerful `yt-dlp` library.
- 📊 **Real-time Progress**: Beautiful progress bars using `rich`.
- 🎧 **Audio Extraction**: Easily convert videos to high-quality MP3.
- 📑 **Playlist Support**: Download entire playlists with a single command.
- 🛠️ **Smart Fallback**: Automatically adapts if `ffmpeg` is missing (warns user but continues download).
- 📋 **Format Listing**: View all available video and audio formats.

## Installation

This project is managed with `uv`.

1. **Clone the repository:**

   ```bash
   git clone git@github.com:davidhadrianus/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

   Or manually:

   ```bash
   uv add yt-dlp rich typer python-dotenv
   ```

3. **(Optional) Install FFmpeg:**
   For the best experience (merging video/audio streams, converting to MP3), install [FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.
   Without FFmpeg, the tool will fallback to the best single-file format available.

## Usage

Run the tool using the `main.py` script.

### Download a Video

```bash
python main.py download "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download Audio Only (MP3)

```bash
python main.py download "https://www.youtube.com/watch?v=VIDEO_ID" --audio
```

### Download a Playlist

```bash
python main.py download "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist
```

### Check Available Formats

```bash
python main.py formats "https://www.youtube.com/watch?v=VIDEO_ID"
```

### CLI Options

- `-o, --output`: Specify output directory (default: `downloads`)
- `-q, --quality`: Quality selection (`best`, `worst`, `hd`, `sd`)
- `-v, --verbose`: Enable verbose output for debugging

## Development

1. **Install dev dependencies:**

   ```bash
   uv add --group dev ruff mypy black pytest pytest-mock pre-commit
   ```

2. **Setup pre-commit hooks:**

   ```bash
   uv run pre-commit install
   ```

3. **Run Linting & Formatting:**
   ```bash
   uv run pre-commit run --all-files
   ```
