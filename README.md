# Vibe Resizer

A tiny Flask app that batch-converts vertical 9:16 clips into square (1:1) and widescreen (16:9) exports.
Choose between a blurred background letterbox or a fill-and-crop look.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This project depends on FFmpeg. MoviePy will attempt to download a static build on first use, but
for best results install FFmpeg locally and make sure it is available on your `$PATH`.

## Running the app

```bash
flask --app app run --debug
```

### Trying it in your browser

1. Wait for Flask to print `Running on http://127.0.0.1:5000` in the terminal.
2. Open that address in your browser on the same machine.
3. Drag one or more 9:16 clips into the upload dropzone.
4. Pick either **Blurred background** or **Fill and crop** for each export size.
5. Click **Start resizing** and let the progress bar finish. When the job completes
   your browser will download a ZIP containing both the 1:1 and 16:9 renders.

> Tip: if you need to test from another device on your network, start the server with
> `flask --app app run --host 0.0.0.0 --port 5000` and browse to `http://<your-ip>:5000`.

## Pricing

This utility is completely free to run locally. There are no usage caps or per-render fees—process
as many clips as your machine can handle.
