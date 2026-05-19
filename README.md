# HEIC GPS Scanner + Map Viewer

快速说明：此项目扫描指定文件夹内的 HEIC/HEIF 图片，使用 `exiftool` 提取 GPS 信息，生成缩略图并在浏览器中以地图+缩略图联动方式展示。

Inspired by Apple.inc

依赖:
- 系统：exiftool（需安装并加入 PATH）
- Python：见 `requirements.txt`

安装：
```powershell
pip install -r requirements.txt
# 在 Windows 上安装 exiftool：手动下载可执行文件并放入 PATH
python app.py
```

使用：打开 `http://localhost:5000`，在侧栏输入要扫描的文件夹路径并点击“扫描”。
# HEIC GPS Scanner

## 项目简介
HEIC GPS Scanner 是一个 Python 项目，旨在扫描指定文件夹中的 HEIC 文件，提取其 GPS 信息，并生成相应的 CSV 文件和 HTML 地图。

## 功能
- 扫描指定目录中的 HEIC 文件
- 提取每个文件的 GPS 信息（经度、纬度和海拔）
- 生成包含 GPS 信息的 CSV 文件
- 创建显示 GPS 位置的 HTML 地图

## 使用方法
1. 确保已安装 Python 3.x 和 `exiftool`。
2. 克隆或下载项目到本地。
3. 在项目根目录下安装依赖项：
   ```
   pip install -r requirements.txt
   ```
4. 运行主脚本：
   ```
   python src/scan_heic.py <要扫描的文件夹路径>
   ```
   如果未提供路径，将会提示输入。

## 目录结构（必看！）
```
heic-gps-scanner
├── src
│   ├── scan_heic.py       # 主脚本
│   ├── utils.py           # 辅助函数
│   └── __init__.py        # Python 包标记
├── tests
│   └── test_scan.py       # 单元测试
├── requirements.txt        # 依赖项
├── .gitignore              # 忽略文件
└── README.md               # 项目文档
```

Windows 系统运行说明（中文）

1. 准备环境
- 安装 Python 3.8+：从 https://www.python.org/ 下载并安装，安装时勾选“Add Python to PATH”。

2. 安装 exiftool（用于读取 HEIC 的 EXIF/GPS）
- 推荐方法（手动）：
   1. 访问 https://exiftool.org/ 下载 Windows 版本（zip）。
   2. 解压后将 `exiftool(-k).exe` 重命名为 `exiftool.exe`，放到一个目录，例如 `C:\Tools\exiftool\`。
   3. 将该目录添加到系统 PATH（控制面板 → 系统 → 高级系统设置 → 环境变量，编辑 PATH 并添加 `C:\Tools\exiftool\`），或使用 PowerShell：

```powershell
setx PATH "$env:PATH;C:\Tools\exiftool\"
```

- 备用方法（Chocolatey）：以管理员权限打开 PowerShell，然后运行：

```powershell
choco install exiftool
```

安装完成后，在 PowerShell 中运行 `exiftool -ver` 应能看到版本号。

3. 安装 Python 依赖
在项目根目录（包含 `app.py` 的目录）打开 PowerShell，然后运行：

```powershell
python -m pip install -r requirements.txt
```

如果遇到 `pyheif` 安装问题（Windows 上有时难编译），可以先只安装 `Flask` 和 `Pillow`：

```powershell
python -m pip install Flask Pillow
```

4. 运行程序
在项目根目录运行：

```powershell
python app.py
```

然后在浏览器打开：

```
http://localhost:5000
```

5. 使用说明
- 在页面右侧输入你要扫描的文件夹路径（例如 `C:\Users\你的用户名\Pictures`），点击“扫描”。程序会调用 `exiftool` 提取 GPS 数据，生成 `data.json` 以及 `static/images` 与 `static/thumbs`（如能成功转换为 JPEG）。

6. 常见问题
- 提示 `exiftool 未安装`：确认 `exiftool.exe` 已放入 PATH，并在终端输入 `exiftool -ver` 能看到版本号。
- 未生成缩略图或图片为空：尝试安装 ImageMagick（将 `magick` 命令加入 PATH）或确保 `pyheif` 与 `Pillow` 可用；部分 HEIC 文件只能由 `exiftool` 提取预览（脚本尝试了多种方式）。
- 权限或防火墙阻止端口：确保防火墙允许本地 5000 端口或修改 `app.py` 中端口号。

7. 示例（完整流程）

```powershell
# 进入项目目录
cd C:\Users\beryl\VSCode\fotomap\heic-gps-scanner

# 安装依赖
python -m pip install -r requirements.txt

# 启动服务
python app.py

# 在浏览器打开 http://localhost:5000，输入要扫描的文件夹并执行扫描
```


## 依赖项
- `exiftool`: 用于提取 HEIC 文件的元数据。
- `folium`: 用于生成 HTML 地图。
- `csv`: 用于处理 CSV 文件。

## 目录结构（必看！）
```
heic-gps-scanner
├── src
│   ├── scan_heic.py       # 主脚本
│   ├── utils.py           # 辅助函数
│   └── __init__.py        # Python 包标记
├── tests
│   └── test_scan.py       # 单元测试
├── requirements.txt        # 依赖项
├── .gitignore              # 忽略文件
└── README.md               # 项目文档
```

## 贡献
欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证
本项目采用 MIT 许可证。
