# SVG图标转换器

🎨 一键将SVG转换为前端开发所需的各种尺寸的ICO和PNG文件，无需任何配置，开箱即用！

## ✨ 特性

- 🚀 **一键转换**: 无需任何配置，将SVG文件放入input目录即可
- 📱 **前端优化**: 根据前端开发最佳实践生成标准尺寸和文件名
- 🎯 **全面覆盖**: 生成favicon.ico、各种PNG尺寸、移动端图标等
- 💼 **即开即用**: 生成的文件无需重命名，直接复制到项目使用

## 🎯 生成的文件

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `favicon.ico` | 16,32,48px | 网站图标(推荐) |
| `favicon.png` | 32x32 | 备用网站图标 |
| `apple-touch-icon.png` | 180x180 | iOS Safari书签图标 |
| `android-chrome-192x192.png` | 192x192 | Android Chrome图标 |
| `android-chrome-512x512.png` | 512x512 | Android Chrome图标 |
| `mstile-150x150.png` | 150x150 | Windows磁贴图标 |
| `{name}-{size}x{size}.png` | 16-512px | 各种尺寸通用图标 |

## 🚀 使用方法

### 1. 放入SVG文件
将你的SVG文件放入 `input/` 目录

### 2. 一键运行

**Windows用户:**
```bash
双击运行 run.bat
```

**Linux/Mac用户:**
```bash
chmod +x run.sh
./run.sh
```

**或直接使用Python:**
```bash
pip install -r requirements.txt
python convert.py
```

### 3. 获取生成的文件
转换完成后，在 `output/` 目录下会为每个SVG文件创建一个子文件夹，包含所有生成的图标文件。

## 📋 前端使用示例

将生成的文件复制到项目根目录，然后在HTML中添加：

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">
<meta name="msapplication-TileImage" content="/mstile-150x150.png">
```

## 🛠️ 依赖要求

- Python 3.7+
- Pillow (图像处理)
- cairosvg (SVG转换)

## 📁 目录结构

```
svg-icon-converter/
├── input/          # 放入SVG文件
├── output/         # 生成的图标文件
├── convert.py      # 主转换脚本
├── run.bat         # Windows一键运行
├── run.sh          # Linux/Mac一键运行
└── requirements.txt # Python依赖
```

## 🎉 开始使用

1. 将SVG文件放入 `input/` 目录
2. 双击运行对应系统的脚本文件
3. 在 `output/` 目录获取生成的图标
4. 复制需要的文件到你的前端项目

就是这么简单！🎯
