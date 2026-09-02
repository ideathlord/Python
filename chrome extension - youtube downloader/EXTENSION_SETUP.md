# YouTube Downloader — Chrome Extension + Local Server

This adds a browser popup with a Download button, backed by a local Python
server running yt-dlp (the extension itself can't run Python/ffmpeg — browser
extensions are sandboxed).

> For personal use only. This can't be published to the Chrome Web Store —
> Google removes YouTube-downloader extensions as a Terms of Service
> violation. Running it locally in Developer Mode is fine.

## 1. Set up the local server

```bash
pip install yt-dlp flask
python server.py
```

Leave this terminal window open — it needs to keep running in the background
whenever you want to use the extension. It listens on
`http://127.0.0.1:5005` and saves files to `~/Downloads/yt-downloads`.

## 2. Load the extension in Chrome

1. Open `chrome://extensions`
2. Turn on **Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the `extension` folder
5. Pin the extension to your toolbar (puzzle-piece icon → pin)

## 3. Use it

1. Go to any YouTube video
2. Click the extension icon
3. Pick a quality (1080p/720p/480p) or check "Audio only (mp3)"
4. Click **Download**
5. Watch the progress percentage update in the popup — when it says "Done",
   check `~/Downloads/yt-downloads`

## Troubleshooting

- **"Local server not running"** — make sure `python server.py` is running
  in a terminal. The extension talks to it over `localhost`, so it must be
  active on the same machine.
- **"Not a YouTube video page"** — the button only activates on
  `youtube.com/watch` or `youtu.be` URLs.
- **Download errors** — same causes/fixes as the standalone script; see
  `TROUBLESHOOTING.md`. Keep `yt-dlp` updated with `pip install -U yt-dlp`.
- **Changing the download folder** — edit `DOWNLOAD_DIR` near the top of
  `server.py`.

## How it fits together

```
[Chrome popup] --fetch--> [server.py on 127.0.0.1:5005] --yt-dlp--> [file on disk]
```

The extension only ever sends a video URL to your own local server and polls
for progress — it never talks to YouTube directly. All the actual
downloading logic is the same yt-dlp code from `yt_downloader.py`.
