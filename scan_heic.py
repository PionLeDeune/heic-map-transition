#scan_heic.py
import subprocess
import json
import sys
import webbrowser
import csv
from pathlib import Path
import shutil
import folium

# 传入目录（命令行参数或交互输入）
if len(sys.argv) >= 2:
    folder = Path(sys.argv[1])
else:
    folder = Path(input("请输入要扫描的文件夹路径: ").strip())

if not folder.exists() or not folder.is_dir():
    print("目录不存在或不是文件夹:", folder)
    sys.exit(1)

if not shutil.which("exiftool"):
    print("需要先安装 exiftool（https://exiftool.org/）。")
    sys.exit(1)

# 找到所有 HEIC 文件（递归）
files = [str(p) for p in folder.rglob("*") if p.suffix.lower() == ".heic"]
if not files:
    print("未找到 .heic 文件")
    sys.exit(0)

# 用 exiftool 一次性获取 GPS 信息，-j 返回 JSON，-n 返回数值形式
cmd = ["exiftool", "-j", "-n", "-GPSLatitude", "-GPSLongitude", "-GPSAltitude"] + files
out = subprocess.check_output(cmd)
items = json.loads(out)

points = []
for it in items:
    src = it.get("SourceFile")
    lat = it.get("GPSLatitude")
    lon = it.get("GPSLongitude")
    alt = it.get("GPSAltitude")
    # 有些文件可能没有 GPS 信息，跳过
    if lat is None or lon is None:
        continue
    points.append({"file": src, "lat": float(lat), "lon": float(lon), "alt": float(alt) if alt is not None else None})

if not points:
    print("没有找到带 GPS 的图片")
    sys.exit(0)

# 分别按经度、纬度、海拔排序
by_lon = sorted(points, key=lambda p: p["lon"])
by_lat = sorted(points, key=lambda p: p["lat"])
by_alt = sorted(points, key=lambda p: (p["alt"] is None, p["alt"]))  # alt None 放后面

# 输出 CSV（同目录）
csv_path = folder / "heic_gps_list.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "lat", "lon", "alt"])
    for p in points:
        w.writerow([p["file"], p["lat"], p["lon"], p["alt"]])

# 生成 folium 地图，中心为平均坐标
avg_lat = sum(p["lat"] for p in points) / len(points)
avg_lon = sum(p["lon"] for p in points) / len(points)
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

for p in points:
    popup = f"{Path(p['file']).name}<br>lat: {p['lat']}<br>lon: {p['lon']}<br>alt: {p['alt']}"
    folium.Marker([p["lat"], p["lon"]], popup=popup).add_to(m)

html_path = folder / "heic_gps_map.html"
m.save(str(html_path))

print("总共找到 GPS 图片:", len(points))
print("CSV:", csv_path)
print("HTML 地图:", html_path)
# 打开浏览器查看
webbrowser.open(f"file://{html_path}")