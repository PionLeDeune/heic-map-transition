from flask import Flask, render_template, jsonify, request
import subprocess
import json
from pathlib import Path
import shutil
from PIL import Image
import sys

BASE = Path(__file__).parent
STATIC_IMAGES = BASE / "static" / "images"
STATIC_THUMBS = BASE / "static" / "thumbs"
DATA_FILE = BASE / "data.json"

app = Flask(__name__, template_folder=str(BASE / "templates"), static_folder=str(BASE / "static"))


def ensure_dirs():
    STATIC_IMAGES.mkdir(parents=True, exist_ok=True)
    STATIC_THUMBS.mkdir(parents=True, exist_ok=True)


def has_exiftool():
    return shutil.which("exiftool") is not None


def run_exiftool(files):
    cmd = ["exiftool", "-j", "-n", "-GPSLatitude", "-GPSLongitude", "-GPSAltitude", "-DateTimeOriginal"] + files
    out = subprocess.check_output(cmd)
    return json.loads(out)


def convert_with_pyheif(src: Path, dst: Path):
    try:
        import pyheif
    except Exception:
        return False
    try:
        heif = pyheif.read(str(src))
        img = Image.frombytes(heif.mode, heif.size, heif.data, "raw")
        img.save(dst, "JPEG", quality=85)
        return True
    except Exception:
        return False


def extract_preview_with_exiftool(src: Path, dst: Path):
    try:
        out = subprocess.check_output(["exiftool", "-b", "-PreviewImage", str(src)])
        if out:
            dst.write_bytes(out)
            return True
    except Exception:
        pass
    return False


def make_thumbnail(src: Path, dst: Path, size=(300, 300)):
    try:
        img = Image.open(src)
        img.thumbnail(size)
        img.save(dst, "JPEG", quality=80)
        return True
    except Exception:
        return False


def scan_folder(folder: Path):
    ensure_dirs()
    files = [str(p) for p in folder.rglob("*") if p.suffix.lower() in (".heic", ".heif", ".HEIC", ".HEIF")]
    if not files:
        return []
    if not has_exiftool():
        raise RuntimeError("exiftool 未安装或不在 PATH")

    items = run_exiftool(files)
    points = []
    for it in items:
        src = Path(it.get("SourceFile"))
        lat = it.get("GPSLatitude")
        lon = it.get("GPSLongitude")
        alt = it.get("GPSAltitude")
        dt = it.get("DateTimeOriginal")
        if lat is None or lon is None:
            continue

        name = src.stem
        img_dst = STATIC_IMAGES / f"{name}.jpg"
        thumb_dst = STATIC_THUMBS / f"{name}.jpg"

        converted = convert_with_pyheif(src, img_dst)
        if not converted:
            converted = extract_preview_with_exiftool(src, img_dst)

        if converted:
            make_thumbnail(img_dst, thumb_dst)
            thumb_url = f"/static/thumbs/{name}.jpg"
            img_url = f"/static/images/{name}.jpg"
        else:
            thumb_url = None
            img_url = None

        points.append({
            "file": str(src),
            "name": name,
            "img": img_url,
            "thumb": thumb_url,
            "lat": float(lat),
            "lon": float(lon),
            "alt": float(alt) if alt is not None else None,
            "datetime": dt,
        })

    DATA_FILE.write_text(json.dumps(points, ensure_ascii=False, indent=2), encoding="utf-8")
    return points


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    if DATA_FILE.exists():
        return DATA_FILE.read_text(encoding="utf-8"), 200, {"Content-Type": "application/json; charset=utf-8"}
    else:
        return jsonify([])


@app.route("/scan", methods=["POST"])
def scan():
    folder = request.form.get("folder") or request.args.get("folder")
    if not folder:
        return jsonify({"error": "请提供 folder 参数"}), 400
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        return jsonify({"error": "目录不存在"}), 400
    try:
        pts = scan_folder(p)
        return jsonify({"count": len(pts)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
