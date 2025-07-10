#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG图标转换器
将SVG文件转换为前端开发所需的各种尺寸的ICO和PNG文件
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
import cairosvg
from io import BytesIO

class SVGIconConverter:
    def __init__(self):
        self.input_dir = Path("input")
        self.output_dir = Path("output")
        
        # 前端开发常用的图标尺寸
        self.png_sizes = [16, 32, 48, 64, 96, 128, 192, 256, 512]
        
        # ICO文件包含的尺寸 (常用于favicon)
        self.ico_sizes = [16, 32, 48]
        
        # 特殊用途的图标
        self.special_icons = {
            'apple-touch-icon.png': 180,
            'android-chrome-192x192.png': 192,
            'android-chrome-512x512.png': 512,
            'mstile-150x150.png': 150,
        }
        
    def ensure_directories(self):
        """确保输入输出目录存在"""
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def svg_to_png(self, svg_path, size):
        """将SVG转换为指定尺寸的PNG - 优化版本"""
        try:
            # 使用更高的DPI和更好的渲染选项
            dpi = max(72, size * 2)  # 动态调整DPI，小图标使用更高DPI
            
            # 使用cairosvg将SVG转换为PNG字节流，使用优化参数
            png_data = cairosvg.svg2png(
                url=str(svg_path),
                output_width=size,
                output_height=size,
                dpi=dpi,
                background_color=None,  # 保持透明背景
            )
            
            # 使用PIL加载PNG数据
            image = Image.open(BytesIO(png_data))
            
            # 确保是RGBA模式以保持透明度
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # 对小尺寸图标进行锐化处理
            if size <= 32:
                from PIL import ImageFilter
                # 轻微锐化，保持细节
                image = image.filter(ImageFilter.UnsharpMask(radius=0.5, percent=150, threshold=0))
            
            # 确保图像尺寸准确
            if image.size != (size, size):
                # 使用高质量重采样
                image = image.resize((size, size), Image.Resampling.LANCZOS)
                
            return image
            
        except Exception as e:
            print(f"转换SVG失败 {svg_path} -> {size}px: {e}")
            return None
    
    def create_ico(self, images):
        """创建包含多个尺寸的ICO文件"""
        if not images:
            return None
            
        # 按尺寸排序
        sorted_images = sorted(images, key=lambda x: x.size[0])
        
        # 创建ICO文件
        ico_buffer = BytesIO()
        try:
            # 使用第一个图像作为基础，添加所有尺寸
            sorted_images[0].save(
                ico_buffer,
                format='ICO',
                sizes=[(img.size[0], img.size[1]) for img in sorted_images],
                # 添加质量选项
                optimize=True
            )
            ico_buffer.seek(0)
            return ico_buffer.getvalue()
        except Exception as e:
            print(f"创建ICO文件失败: {e}")
            return None
    
    def save_png_optimized(self, image, path):
        """优化PNG保存，保持最佳质量"""
        try:
            # 使用优化选项保存PNG
            image.save(
                path, 
                "PNG", 
                optimize=True,
                compress_level=6,  # 平衡文件大小和质量
                pnginfo=None  # 不保存元数据，减小文件大小
            )
            return True
        except Exception as e:
            print(f"保存PNG失败 {path}: {e}")
            return False
    
    def process_svg_file(self, svg_path):
        """处理单个SVG文件"""
        filename_base = svg_path.stem
        print(f"\n处理文件: {svg_path.name}")
        
        # 创建子目录
        output_subdir = self.output_dir / filename_base
        output_subdir.mkdir(exist_ok=True)
        
        # 生成标准PNG尺寸
        print("生成PNG文件...")
        for size in self.png_sizes:
            image = self.svg_to_png(svg_path, size)
            if image:
                png_path = output_subdir / f"{filename_base}-{size}x{size}.png"
                if self.save_png_optimized(image, png_path):
                    print(f"  ✓ {png_path.name}")
                else:
                    print(f"  ❌ {png_path.name}")
        
        # 生成特殊用途图标
        print("生成特殊用途图标...")
        for special_name, size in self.special_icons.items():
            image = self.svg_to_png(svg_path, size)
            if image:
                special_path = output_subdir / special_name
                if self.save_png_optimized(image, special_path):
                    print(f"  ✓ {special_name}")
                else:
                    print(f"  ❌ {special_name}")
        
        # 生成ICO文件
        print("生成ICO文件...")
        ico_images = []
        for size in self.ico_sizes:
            image = self.svg_to_png(svg_path, size)
            if image:
                ico_images.append(image)
        
        if ico_images:
            ico_data = self.create_ico(ico_images)
            if ico_data:
                ico_path = output_subdir / "favicon.ico"
                try:
                    with open(ico_path, 'wb') as f:
                        f.write(ico_data)
                    print(f"  ✓ favicon.ico")
                except Exception as e:
                    print(f"  ❌ favicon.ico: {e}")
        
        # 生成单独的favicon.png (32x32)
        favicon_png = self.svg_to_png(svg_path, 32)
        if favicon_png:
            favicon_png_path = output_subdir / "favicon.png"
            if self.save_png_optimized(favicon_png, favicon_png_path):
                print(f"  ✓ favicon.png")
            else:
                print(f"  ❌ favicon.png")
    
    def convert_all(self):
        """转换所有SVG文件"""
        self.ensure_directories()
        
        # 查找所有SVG文件
        svg_files = list(self.input_dir.glob("*.svg"))
        
        if not svg_files:
            print("❌ 在input目录中没有找到SVG文件")
            print(f"请将SVG文件放入: {self.input_dir.absolute()}")
            return
        
        print(f"找到 {len(svg_files)} 个SVG文件")
        print("=" * 50)
        
        for svg_file in svg_files:
            try:
                self.process_svg_file(svg_file)
            except Exception as e:
                print(f"❌ 处理文件 {svg_file.name} 时出错: {e}")
        
        print("\n" + "=" * 50)
        print("✅ 转换完成！")
        print(f"输出目录: {self.output_dir.absolute()}")
        
        # 显示输出文件说明
        self.show_output_guide()
        
        # 显示质量优化说明
        self.show_quality_tips()
    
    def show_output_guide(self):
        """显示输出文件使用说明"""
        print("\n📋 文件用途说明:")
        print("├── favicon.ico          - 网站图标 (推荐)")
        print("├── favicon.png          - 备用网站图标 (32x32)")
        print("├── apple-touch-icon.png - iOS Safari书签图标")
        print("├── android-chrome-*.png - Android Chrome图标")
        print("├── mstile-150x150.png   - Windows磁贴图标")
        print("└── *-{size}x{size}.png  - 各种尺寸的通用图标")
        
        print("\n🚀 前端使用示例:")
        print("""
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">
""")
    
    def show_quality_tips(self):
        """显示质量优化提示"""
        print("\n💡 质量优化提示:")
        print("• 已自动应用高质量渲染和抗锯齿")
        print("• 小尺寸图标已进行锐化处理")
        print("• 保持了原始透明度和颜色")
        print("• 如果效果仍不理想，请检查原始SVG文件质量")
        print("• 建议原始SVG使用简洁的矢量图形，避免过于复杂的效果")

def main():
    print("🎨 SVG图标转换器 - 高质量版本")
    print("将SVG转换为前端开发所需的各种格式和尺寸")
    print("=" * 50)
    
    converter = SVGIconConverter()
    converter.convert_all()

if __name__ == "__main__":
    main() 