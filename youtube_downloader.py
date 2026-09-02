#!/usr/bin/env python3
"""
YouTube Downloader
-------------------
A simple command-line tool for downloading YouTube videos or audio using yt-dlp.

IMPORTANT: Only download content you own, that is public domain, licensed
under Creative Commons, or that you otherwise have permission to download.
Downloading copyrighted content without permission may violate YouTube's
Terms of Service and copyright law.

Setup:
    pip install yt-dlp

Usage:
    python yt_downloader.py <url>
    python yt_downloader.py <url> --audio-only
    python yt_downloader.py <url> --quality 720
    python yt_downloader.py <url> -o ~/Downloads
"""

import argparse
import sys
import os

try:
    import yt_dlp
except ImportError:
    print("Missing dependency. Install it with:\n    pip install yt-dlp")
    sys.exit(1)


def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        sys.stdout.write(f"\r  {percent}  speed: {speed}  eta: {eta}   ")
        sys.stdout.flush()
    elif d["status"] == "finished":
        print("\n  Download finished, now post-processing...")


def build_options(args):
    outtmpl = os.path.join(args.output, "%(title)s.%(ext)s")

    if args.audio_only:
        format_spec = "bestaudio/best"
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
        merge_output_format = None
    else:
        # Default cap of 1080p if the user didn't specify --quality.
        max_height = args.quality or 1080

        # Prefer H.264 video + AAC audio in an mp4 container -- this is the
        # combo virtually every player (including VLC) supports natively.
        # YouTube's mp4 formats are sometimes VP9 or AV1 instead of H.264,
        # which some players handle poorly, so we pin the codec explicitly
        # rather than just matching on file extension.
        format_spec = (
            f"bestvideo[vcodec^=avc1][height<={max_height}]+bestaudio[acodec^=mp4a]"
            f"/best[vcodec^=avc1][ext=mp4][height<={max_height}]"
            f"/bestvideo[ext=mp4][height<={max_height}]+bestaudio[ext=m4a]"
            f"/best[ext=mp4][height<={max_height}]"
        )
        # Remux (no quality loss, fast) rather than re-encode. yt-dlp only
        # re-encodes if the merged streams truly can't be packaged as mp4.
        postprocessors = [{"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"}]
        merge_output_format = "mp4"

    opts = {
        "format": format_spec,
        "outtmpl": outtmpl,
        "postprocessors": postprocessors,
        "progress_hooks": [progress_hook],
        "noplaylist": not args.playlist,
        "quiet": True,
        "no_warnings": True,
        # YouTube's "SABR streaming" rollout breaks format extraction for some
        # client types (e.g. tv_downgraded, web/web_safari), causing a
        # "The page needs to be reloaded" error. Falling back through a list
        # of alternate clients works around this in most cases.
        # Note: as of Aug 2026, android_vr requires a PO token and will 403
        # on yt-dlp versions older than 2026.08.19 -- update yt-dlp if you
        # want to re-add it to this list.
        # See: https://github.com/yt-dlp/yt-dlp/issues/12482
        #      https://github.com/yt-dlp/yt-dlp/issues/17348
        "extractor_args": {
            "youtube": {
                "player_client": args.player_client.split(",") if args.player_client else
                    ["tv", "web", "default", "android_vr"],
            }
        },
    }

    if merge_output_format:
        opts["merge_output_format"] = merge_output_format

    return opts


def download(url, args):
    base_opts = build_options(args)
    clients = base_opts["extractor_args"]["youtube"]["player_client"]

    last_error = None
    for i, client in enumerate(clients):
        ydl_opts = dict(base_opts)
        ydl_opts["extractor_args"] = {"youtube": {"player_client": [client]}}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Fetching info for: {url}" + (f"  (client: {client})" if i > 0 else ""))
                info = ydl.extract_info(url, download=False)

                title = info.get("title", "Unknown title")
                duration = info.get("duration")
                uploader = info.get("uploader", "Unknown uploader")

                print(f"  Title:    {title}")
                print(f"  Uploader: {uploader}")
                if duration:
                    mins, secs = divmod(duration, 60)
                    print(f"  Duration: {mins}m {secs}s")
                print()

                print("Starting download...")
                ydl.download([url])
                print(f"\nSaved to: {args.output}")
                return
        except yt_dlp.utils.DownloadError as e:
            last_error = e
            if i < len(clients) - 1:
                print(f"\n  Client '{client}' failed, trying next fallback ({clients[i + 1]})...\n")
            continue

    raise last_error


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos or audio (yt-dlp wrapper).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "url", nargs="?", default=None, help="YouTube video (or playlist) URL (optional; you'll be prompted if omitted)"
    )
    parser.add_argument(
        "--audio-only", action="store_true", help="Download audio only as mp3"
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=None,
        help="Max video height in pixels, e.g. 720 or 1080 (ignored with --audio-only)",
    )
    parser.add_argument(
        "-o", "--output", default=os.getcwd(), help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--playlist", action="store_true", help="Download full playlist if URL is part of one"
    )
    parser.add_argument(
        "--player-client",
        default=None,
        help=(
            "Comma-separated YouTube player client(s) to try, in order, e.g. "
            "'android_vr,tv,web,default'. Overrides the built-in fallback list. "
            "Useful if you're hitting 'The page needs to be reloaded' errors."
        ),
    )

    args = parser.parse_args()

    if not args.url:
        args.url = input("Enter YouTube video (or playlist) URL: ").strip()

    if not args.url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    try:
        download(args.url, args)
    except yt_dlp.utils.DownloadError as e:
        print(f"\nDownload failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)


if __name__ == "__main__":
    main()