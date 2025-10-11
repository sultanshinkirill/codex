from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from moviepy.editor import CompositeVideoClip, VideoFileClip
from moviepy.video.fx import crop, resize
from moviepy.video.fx import all as vfx

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "processed"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

TARGET_SPECS = {
    "square": {"label": "Square 1:1", "width": 1080, "height": 1080},
    "widescreen": {"label": "Widescreen 16:9", "width": 1920, "height": 1080},
}


def ensure_even(value: int) -> int:
    """MoviePy/FFmpeg prefer even dimensions."""
    return value if value % 2 == 0 else value - 1


def scale_and_crop(clip: VideoFileClip, target_width: int, target_height: int) -> VideoFileClip:
    """Scale the clip so it covers the target box, then crop the overflow."""
    scale_factor = max(target_width / clip.w, target_height / clip.h)
    resized = clip.fx(resize.resize, scale_factor)

    x_center = resized.w / 2
    y_center = resized.h / 2

    x1 = max(0, x_center - target_width / 2)
    y1 = max(0, y_center - target_height / 2)
    x2 = min(resized.w, x1 + target_width)
    y2 = min(resized.h, y1 + target_height)

    x1 = max(0, x2 - target_width)
    y1 = max(0, y2 - target_height)

    return resized.fx(crop.crop, x1=x1, y1=y1, x2=x2, y2=y2).set_audio(clip.audio)


def blur_background_composite(clip: VideoFileClip, target_width: int, target_height: int) -> VideoFileClip:
    """Create a blurred background while keeping the original video centered."""
    bg_scale = max(target_width / clip.w, target_height / clip.h)
    background = (
        clip.fx(resize.resize, bg_scale)
        .fx(vfx.gaussian_blur, sigma=25)
        .fx(
            crop.crop,
            x_center=clip.w * bg_scale / 2,
            y_center=clip.h * bg_scale / 2,
            width=target_width,
            height=target_height,
        )
    )

    fg_scale = min(target_width / clip.w, target_height / clip.h)
    foreground = clip.fx(resize.resize, fg_scale)

    composite = CompositeVideoClip(
        [background, foreground.set_position("center")],
        size=(target_width, target_height),
    )
    return composite.set_audio(clip.audio)


def process_video(input_path: Path, mode: str, output_dir: Path) -> list[Path]:
    outputs: list[Path] = []
    with VideoFileClip(str(input_path)) as clip:
        for key, spec in TARGET_SPECS.items():
            width = ensure_even(spec["width"])
            height = ensure_even(spec["height"])
            output_path = output_dir / f"{input_path.stem}_{key}.mp4"

            if mode == "blur":
                processed_clip = blur_background_composite(clip, width, height)
            else:
                processed_clip = scale_and_crop(clip, width, height)

            processed_clip.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                remove_temp=True,
                threads=2,
                verbose=False,
                logger=None,
            )

            processed_clip.close()
            outputs.append(output_path)

    return outputs


@app.route("/")
def index():
    return render_template("index.html", specs=TARGET_SPECS)


@app.post("/process")
def process():
    if "videos" not in request.files:
        return jsonify({"error": "No videos uploaded."}), 400

    files = request.files.getlist("videos")
    mode = request.form.get("mode", "blur")
    mode = mode if mode in {"blur", "scale"} else "blur"

    request_id = uuid.uuid4().hex
    session_upload_dir = UPLOAD_DIR / request_id
    session_output_dir = OUTPUT_DIR / request_id
    session_upload_dir.mkdir(parents=True, exist_ok=True)
    session_output_dir.mkdir(parents=True, exist_ok=True)

    processed_files: list[Path] = []

    try:
        for file_storage in files:
            if not file_storage.filename:
                continue
            input_path = session_upload_dir / file_storage.filename
            file_storage.save(input_path)
            processed_files.extend(process_video(input_path, mode, session_output_dir))
    except Exception as exc:  # pragma: no cover - logging/cleanup path
        shutil.rmtree(session_upload_dir, ignore_errors=True)
        shutil.rmtree(session_output_dir, ignore_errors=True)
        return jsonify({"error": f"Failed to process videos: {exc}"}), 500

    if not processed_files:
        shutil.rmtree(session_upload_dir, ignore_errors=True)
        shutil.rmtree(session_output_dir, ignore_errors=True)
        return jsonify({"error": "No valid videos were uploaded."}), 400

    archive_stem = OUTPUT_DIR / request_id
    shutil.make_archive(str(archive_stem), "zip", session_output_dir)

    shutil.rmtree(session_upload_dir, ignore_errors=True)
    shutil.rmtree(session_output_dir, ignore_errors=True)

    return jsonify(
        {
            "downloadUrl": url_for("download", request_id=request_id, _external=False),
            "fileCount": len(processed_files),
        }
    )


@app.get("/download/<request_id>")
def download(request_id: str):
    archive = OUTPUT_DIR / f"{request_id}.zip"
    if not archive.exists():
        return redirect(url_for("index"))
    return send_file(archive, as_attachment=True, download_name=f"resized_{request_id}.zip")


if __name__ == "__main__":
    app.run(debug=True)
