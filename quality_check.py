#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG质量诊断工具
分析SVG文件并提供质量优化建议
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import re

class SVGQualityChecker:
    def __init__(self):
        self.input_dir = Path("input")
        
    def analyze_svg(self, svg_path):
        """分析SVG文件质量"""
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            analysis = {
                'file': svg_path.name,
                'size': svg_path.stat().st_size,
                'issues': [],
                'suggestions': []
            }
            
            # 检查SVG尺寸设置
            width = root.get('width')
            height = root.get('height')
            viewbox = root.get('viewBox')
            
            if not viewbox:
                analysis['issues'].append("❌ 缺少viewBox属性")
                analysis['suggestions'].append("添加viewBox属性以确保缩放质量")
            
            if width and ('px' in width or 'pt' in width):
                analysis['issues'].append("⚠️ 使用了绝对单位 (px/pt)")
                analysis['suggestions'].append("建议移除width/height或使用相对单位")
            
            # 检查复杂元素
            self._check_complex_elements(root, analysis)
            
            # 检查文本元素
            self._check_text_elements(root, analysis)
            
            # 检查样式和效果
            self._check_styles_and_effects(root, analysis)
            
            # 检查文件大小
            if analysis['size'] > 50000:  # 50KB
                analysis['issues'].append("⚠️ 文件较大 (>50KB)")
                analysis['suggestions'].append("考虑简化路径或移除不必要的元素")
            
            return analysis
            
        except Exception as e:
            return {
                'file': svg_path.name,
                'error': f"解析失败: {e}",
                'issues': ["❌ SVG文件格式错误"],
                'suggestions': ["检查SVG文件是否损坏或格式不正确"]
            }
    
    def _check_complex_elements(self, root, analysis):
        """检查复杂元素"""
        # 查找所有路径
        paths = root.findall('.//{http://www.w3.org/2000/svg}path')
        if len(paths) > 20:
            analysis['issues'].append(f"⚠️ 路径元素过多 ({len(paths)}个)")
            analysis['suggestions'].append("考虑合并路径或简化图形")
        
        # 检查复杂路径
        for path in paths:
            d = path.get('d', '')
            if len(d) > 1000:
                analysis['issues'].append("⚠️ 存在过于复杂的路径")
                analysis['suggestions'].append("简化复杂路径以提高渲染质量")
                break
        
        # 检查渐变和滤镜
        gradients = root.findall('.//{http://www.w3.org/2000/svg}linearGradient') + \
                   root.findall('.//{http://www.w3.org/2000/svg}radialGradient')
        if len(gradients) > 5:
            analysis['issues'].append(f"⚠️ 渐变过多 ({len(gradients)}个)")
            analysis['suggestions'].append("减少渐变数量可能提高小尺寸图标质量")
        
        filters = root.findall('.//{http://www.w3.org/2000/svg}filter')
        if filters:
            analysis['issues'].append(f"⚠️ 使用了滤镜效果 ({len(filters)}个)")
            analysis['suggestions'].append("滤镜在小尺寸下可能效果不佳，考虑简化")
    
    def _check_text_elements(self, root, analysis):
        """检查文本元素"""
        texts = root.findall('.//{http://www.w3.org/2000/svg}text')
        if texts:
            analysis['issues'].append(f"⚠️ 包含文本元素 ({len(texts)}个)")
            analysis['suggestions'].append("文本在小尺寸下可能不清晰，建议转换为路径")
            
            # 检查字体大小
            for text in texts:
                font_size = text.get('font-size', '')
                if font_size and font_size.replace('px', '').replace('pt', '').isdigit():
                    size = float(font_size.replace('px', '').replace('pt', ''))
                    if size < 12:
                        analysis['issues'].append("❌ 字体过小 (<12px)")
                        analysis['suggestions'].append("小字体在图标中可能无法识别")
    
    def _check_styles_and_effects(self, root, analysis):
        """检查样式和特效"""
        # 检查内联样式
        elements_with_style = root.findall(".//*[@style]")
        if elements_with_style:
            analysis['issues'].append("⚠️ 使用了内联样式")
            analysis['suggestions'].append("考虑将样式转换为属性以提高兼容性")
        
        # 检查透明度
        elements_with_opacity = root.findall(".//*[@opacity]")
        complex_opacity = [el for el in elements_with_opacity 
                          if el.get('opacity') and float(el.get('opacity', 1)) < 0.5]
        if complex_opacity:
            analysis['issues'].append("⚠️ 使用了低透明度元素")
            analysis['suggestions'].append("低透明度可能影响小图标的视觉效果")
        
        # 检查阴影效果
        svg_content = ET.tostring(root, encoding='unicode')
        if 'drop-shadow' in svg_content or 'blur' in svg_content:
            analysis['issues'].append("⚠️ 使用了阴影或模糊效果")
            analysis['suggestions'].append("阴影效果在小尺寸下可能消失")
    
    def check_all_files(self):
        """检查所有SVG文件"""
        svg_files = list(self.input_dir.glob("*.svg"))
        
        if not svg_files:
            print("❌ 在input目录中没有找到SVG文件")
            return
        
        print("🔍 SVG质量诊断报告")
        print("=" * 60)
        
        for svg_file in svg_files:
            analysis = self.analyze_svg(svg_file)
            self.print_analysis(analysis)
        
        self.print_general_tips()
    
    def print_analysis(self, analysis):
        """打印分析结果"""
        print(f"\n📁 文件: {analysis['file']}")
        print(f"💾 大小: {analysis.get('size', 0):,} 字节")
        
        if 'error' in analysis:
            print(f"❌ {analysis['error']}")
            return
        
        if not analysis['issues']:
            print("✅ 未发现明显问题")
        else:
            print("\n⚠️ 发现的问题:")
            for issue in analysis['issues']:
                print(f"  {issue}")
        
        if analysis['suggestions']:
            print("\n💡 优化建议:")
            for suggestion in analysis['suggestions']:
                print(f"  • {suggestion}")
        
        print("-" * 40)
    
    def print_general_tips(self):
        """打印通用优化提示"""
        print("\n🎯 通用优化建议:")
        print("""
1. 📐 使用viewBox而非固定尺寸
   ✓ 正确: <svg viewBox="0 0 100 100">
   ❌ 避免: <svg width="100px" height="100px">

2. 🎨 简化设计元素
   • 减少路径复杂度
   • 避免过多细节
   • 使用简洁的几何形状

3. 🚫 避免problematic元素
   • 避免小字体文本
   • 减少滤镜和特效
   • 限制渐变数量

4. 🎪 颜色和对比度
   • 使用高对比度颜色
   • 避免过于相近的颜色
   • 考虑深色模式兼容性

5. 📏 测试不同尺寸
   • 在16x16px下检查清晰度
   • 确保主要特征可识别
   • 验证细节是否保留
""")

def main():
    print("🔍 SVG质量诊断工具")
    print("分析SVG文件并提供优化建议")
    print("=" * 50)
    
    checker = SVGQualityChecker()
    checker.check_all_files()

if __name__ == "__main__":
    main() 