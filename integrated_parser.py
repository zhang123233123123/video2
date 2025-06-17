#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
集成视频解析器
集成优酷专线解析器到现有系统中
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_parser import EnhancedVIPParser
from youku_enhanced_parser import YoukuEnhancedParser
from typing import Dict, Any, Optional

class IntegratedVideoParser:
    """集成视频解析器"""
    
    def __init__(self):
        # 初始化原有的解析器
        self.original_parser = EnhancedVIPParser()
        
        # 初始化优酷专线解析器
        self.youku_parser = YoukuEnhancedParser()
    
    def parse_video(self, url: str) -> Dict[str, Any]:
        """解析视频 - 优酷使用专线，其他平台使用原方法"""
        
        # 检测是否为优酷链接
        if self.youku_parser.is_youku_url(url):
            print("🎯 检测到优酷链接，使用优酷专线解析...")
            result = self.youku_parser.parse_youku_video(url)
            
            # 标记使用的解析方法
            result['parser_type'] = 'youku_enhanced'
            result['parser_info'] = '优酷专线解析器'
            
            return result
        else:
            print("🔍 使用原始解析器解析...")
            result = self.original_parser.parse_video(url)
            
            # 标记使用的解析方法
            result['parser_type'] = 'original'
            result['parser_info'] = '原始解析器'
            
            return result
    
    def get_supported_platforms(self) -> list:
        """获取支持的平台"""
        platforms = self.original_parser.get_supported_platforms()
        platforms.append("优酷(专线)")
        return platforms
    
    def get_youku_api_info(self) -> list:
        """获取优酷专线API信息"""
        return self.youku_parser.get_api_info()
    
    def get_original_api_info(self) -> list:
        """获取原始解析API信息"""
        return self.original_parser.get_parse_apis_info()
    
    def test_youku_apis(self, url: str) -> list:
        """测试优酷专线APIs"""
        if self.youku_parser.is_youku_url(url):
            return self.youku_parser.test_all_apis(url)
        return []

def test_integrated_parser():
    """测试集成解析器"""
    parser = IntegratedVideoParser()
    
    # 测试链接
    test_urls = [
        # 优酷链接
        "https://v.youku.com/video?vid=XNjQ4MzA5ODkwOA==&s=bdfb0949ae4c4ac39168&scm=20140719.apircmd.298496.video_XNjQ4MzA5ODkwOA==&spm=a2hkt.13141534.1_6.d_1_13",
        "https://v.youku.com/video?vid=XNjQ4MDE0MTc0OA==&s=06efbfbd08efbfbdefbf&scm=20140719.apircmd.298496.video_XNjQ4MDE0MTc0OA==&spm=a2hkt.13141534.1_6.d_1_4",
        # 其他平台链接（示例）
        "https://v.qq.com/x/cover/m4101qychtr.html"
    ]
    
    print("=" * 80)
    print("集成视频解析器测试")
    print("=" * 80)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n【测试链接 {i}】")
        print(f"URL: {url}")
        print("-" * 60)
        
        result = parser.parse_video(url)
        
        print(f"解析器类型: {result.get('parser_type', '未知')}")
        print(f"解析器信息: {result.get('parser_info', '未知')}")
        
        if result.get('success'):
            print("✓ 解析成功")
            print(f"  平台: {result.get('platform', '未知')}")
            print(f"  标题: {result.get('title', '未知')}")
            print(f"  视频ID: {result.get('vid', '未知')}")
            
            if result.get('best_parse_url'):
                print(f"  最佳解析链接: {result['best_parse_url'][:80]}...")
            
            if result.get('parse_urls'):
                print(f"  可用解析线路: {len(result['parse_urls'])}")
        else:
            print("✗ 解析失败")
            print(f"  错误: {result.get('error', '未知错误')}")
    
    print("\n" + "=" * 80)
    print("支持的平台")
    print("=" * 80)
    
    platforms = parser.get_supported_platforms()
    for platform in platforms:
        print(f"• {platform}")
    
    print("\n" + "=" * 80)
    print("优酷专线API信息")
    print("=" * 80)
    
    youku_apis = parser.get_youku_api_info()
    for api in youku_apis:
        print(f"线路: {api['name']}")
        print(f"优先级: {api['priority']}")
        print(f"类型: {api['type']}")
        print("-" * 40)

if __name__ == "__main__":
    test_integrated_parser() 