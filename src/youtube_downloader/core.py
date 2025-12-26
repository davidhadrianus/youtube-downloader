import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yt_dlp


@dataclass
class DownloadOptions:
    """Options for YouTube downloads"""

    output_path: Path = Path("downloads")
    quality: str = "best"
    audio_only: bool = False
    format: str = "mp4"
    playlist: bool = False
    verbose: bool = False
    progress_hook: Callable[[dict[str, Any]], None] | None = None


class YouTubeDownloader:
    """Main downloader class using yt-dlp library"""

    def __init__(self, options: DownloadOptions | None = None):
        self.options = options or DownloadOptions()
        self.output_path = self.options.output_path
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_available = shutil.which("ffmpeg") is not None

    def download(self, url: str) -> bool:
        """Download a single video or playlist"""
        if not self.ffmpeg_available and self.options.verbose:
            print(
                "Warning: ffmpeg not found. Falling back to lower quality/direct download."
            )

        ydl_opts = self._build_options()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            if self.options.verbose:
                print(f"Error: {e}")
            return False

    def _build_options(self) -> dict[str, Any]:
        """Build yt-dlp options dictionary"""
        opts: dict[str, Any] = {
            "outtmpl": str(self.output_path / "%(title)s.%(ext)s"),
            "quiet": not self.options.verbose,
            "no_warnings": not self.options.verbose,
        }

        if self.options.progress_hook:
            opts["progress_hooks"] = [self.options.progress_hook]

        if self.options.playlist:
            opts["yes_playlist"] = True
            opts["outtmpl"] = str(
                self.output_path / "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
            )
            opts["download_archive"] = str(self.output_path / "archive.txt")
        else:
            opts["noplaylist"] = True

        if self.options.audio_only:
            opts["format"] = "bestaudio/best"
            # Only use postprocessors if ffmpeg is available
            if self.ffmpeg_available:
                opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]
        else:
            if self.ffmpeg_available:
                opts["format"] = self._get_format_string()
                if self.options.format == "mp4":
                    opts["merge_output_format"] = "mp4"
            else:
                # Fallback format that doesn't require merging
                opts["format"] = "best"

        return opts

    def _get_format_string(self) -> str:
        """Get yt-dlp format string based on quality option"""
        quality_map = {
            "best": "bestvideo+bestaudio/best",
            "worst": "worstvideo+worstaudio/worst",
            "hd": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "sd": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        }
        return quality_map.get(self.options.quality, self.options.quality)

    @staticmethod
    def get_available_formats(url: str) -> str:
        """List available formats for a URL"""
        try:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                # We can return a formatted string or just modify the caller to handle dict
                # For now let's mimic the CLI output structure to minimize changes
                # But actually, lets just return the raw text representation if possible or
                # return the list of formats to be processed.
                # To match previous behavior of returning a string:
                return str(info.get("formats", []))
                # Note: The previous CLI implementation returned the raw table from -F.
                # Replicating that exactly with the library is verbose.
                # Let's adjust this to return the formats list directly in a future step if needed,
                # but for now, let's keep it simple or use a simple textual representation.

                # Actually, let's just use the cli implementation for this specific check
                # OR better yet, just let the CLI handle format listing via the library too.
                # For now, I will return a placeholder or simple string representation.

                formats = info.get("formats", [])
                output = []
                for f in formats:
                    output.append(
                        f"{f.get('format_id')} {f.get('ext')} {f.get('resolution')} {f.get('note', '')}"
                    )
                return "\n".join(output)

        except Exception as e:
            return f"Error: {e}"
