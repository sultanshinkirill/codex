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

Open http://127.0.0.1:5000/ and drop in your vertical clips. Once the processing finishes you'll get
one ZIP containing both the 1:1 and 16:9 renders for every upload.

## Pricing

This utility is completely free to run locally. There are no usage caps or per-render fees—process
as many clips as your machine can handle.
