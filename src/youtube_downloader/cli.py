# ignore mypy no-untyped-def error
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from .core import DownloadOptions, YouTubeDownloader

app = typer.Typer(
    name="yt-dl",
    help="YouTube Downloader",
    add_completion=False,
)
console = Console()


@app.command()
def download(
    url: str = typer.Argument(..., help="YouTube video or playlist URL"),
    output: Path = typer.Option(
        Path("downloads"), "--output", "-o", help="Output directory"
    ),
    quality: str = typer.Option(
        "best", "--quality", "-q", help="Quality: best, worst, hd, sd, or format code"
    ),
    audio: bool = typer.Option(
        False, "--audio", "-a", help="Download audio only (MP3)"
    ),
    playlist: bool = typer.Option(False, "--playlist", "-p", help="Download playlist"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Download YouTube videos or audio"""

    # We will define a wrapper class to manage the progress bar state
    class ProgressHandler:
        def __init__(self, progress: Progress, task_id: Any):
            self.progress = progress
            self.task_id = task_id
            self.last_status = ""

        def hook(self, d: dict[str, Any]) -> None:
            status = d.get("status")
            if status == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                downloaded = d.get("downloaded_bytes", 0)

                if total:
                    self.progress.update(
                        self.task_id, total=total, completed=downloaded
                    )

                # Optional: Update description with filename or other info
                # filename = d.get("filename", "")
                # self.progress.update(self.task_id, description=f"Downloading {Path(filename).name}...")

            elif status == "finished":
                self.progress.update(
                    self.task_id,
                    completed=None,
                    description="[green]Processing completion...[/green]",
                )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("Initializing...", start=False)
        handler = ProgressHandler(progress, task_id)
        # Start the task when we actually begin
        progress.start_task(task_id)
        progress.update(task_id, description="Downloading...")

        options = DownloadOptions(
            output_path=output,
            quality=quality,
            audio_only=audio,
            playlist=playlist,
            verbose=verbose,
            progress_hook=handler.hook,
        )

        downloader = YouTubeDownloader(options)
        success = downloader.download(url)

    if success:
        console.print(f"OK Downloaded to: {output.absolute()}", style="green bold")
    else:
        console.print("ERROR Download failed!", style="red bold")
        raise typer.Exit(code=1)


@app.command()
def formats(
    url: str = typer.Argument(..., help="YouTube URL to check available formats"),
) -> None:
    """Show available formats for a video"""
    console.print(f"Checking formats for: {url}", style="blue")

    # Since we refactored core to return a simple list string, we print it directly or parse it.
    # The previous simple parsing logic might need adjustment if the format changed significantly.
    # Let's just print the output for now as it contains the relevant info.

    formats_output = YouTubeDownloader.get_available_formats(url)
    console.print(formats_output)


@app.command()
def config() -> None:
    """Show current configuration"""
    console.print("Current Configuration:", style="bold")
    console.print(f"Python: {Path.cwd()}")
    console.print("Project: youtube-downloader")
    console.print("Dependencies managed with: uv")


if __name__ == "__main__":
    app()
