#utils.py
def get_heic_files(folder):
    """获取指定文件夹中所有 HEIC 文件的路径列表"""
    return [str(p) for p in folder.rglob("*") if p.suffix.lower() == ".heic"]

def format_gps_data(file, lat, lon, alt):
    """格式化 GPS 数据为可读字符串"""
    return f"File: {file}, Latitude: {lat}, Longitude: {lon}, Altitude: {alt if alt is not None else 'N/A'}"

def save_csv(data, csv_path):
    """将数据保存为 CSV 文件"""
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "lat", "lon", "alt"])
        for row in data:
            writer.writerow(row)

def create_map(points, html_path):
    """生成 HTML 地图并保存"""
    avg_lat = sum(p["lat"] for p in points) / len(points)
    avg_lon = sum(p["lon"] for p in points) / len(points)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    for p in points:
        popup = f"{Path(p['file']).name}<br>lat: {p['lat']}<br>lon: {p['lon']}<br>alt: {p['alt']}"
        folium.Marker([p["lat"], p["lon"]], popup=popup).add_to(m)

    m.save(str(html_path))