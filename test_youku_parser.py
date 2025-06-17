#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
优酷解析器测试脚本
用于测试优酷专线解析器的功能
"""

from youku_enhanced_parser import YoukuEnhancedParser
import json

def test_youku_urls():
    """测试优酷链接解析"""
    
    # 初始化解析器
    parser = YoukuEnhancedParser()
    
    # 测试的优酷链接
    test_urls = [
        "https://v.youku.com/video?vid=XNjQ4MzA5ODkwOA==&s=bdfb0949ae4c4ac39168&scm=20140719.apircmd.298496.video_XNjQ4MzA5ODkwOA==&spm=a2hkt.13141534.1_6.d_1_13",
        "https://v.youku.com/video?vid=XNjQ4MDE0MTc0OA==&s=06efbfbd08efbfbdefbf&scm=20140719.apircmd.298496.video_XNjQ4MDE0MTc0OA==&spm=a2hkt.13141534.1_6.d_1_4"
    ]
    
    print("=" * 80)
    print("优酷专线解析器测试")
    print("=" * 80)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n【测试链接 {i}】")
        print(f"链接: {url}")
        print("-" * 60)
        
        # 检测是否为优酷链接
        if parser.is_youku_url(url):
            print("✓ 检测到优酷链接")
            
            # 提取视频ID
            vid = parser.extract_video_id(url)
            if vid:
                print(f"✓ 视频ID: {vid}")
            else:
                print("✗ 无法提取视频ID")
            
            # 解析视频
            result = parser.parse_youku_video(url)
            
            if result['success']:
                print("✓ 解析成功!")
                print(f"  标题: {result.get('title', '未知')}")
                print(f"  时长: {result.get('duration', '未知')}")
                print(f"  视频ID: {result.get('vid', '未知')}")
                print(f"  推荐解析线路: {result.get('recommended_api', '未设置')}")
                print(f"  最佳解析链接: {result.get('best_parse_url', '未设置')}")
                
                # 显示所有可用线路
                if result.get('parse_urls'):
                    print(f"  可用解析线路数量: {len(result['parse_urls'])}")
                    print("  解析线路列表:")
                    for j, parse_info in enumerate(result['parse_urls'][:3], 1):  # 只显示前3个
                        print(f"    {j}. {parse_info['name']}")
                        print(f"       URL: {parse_info['url']}")
                
            else:
                print("✗ 解析失败!")
                print(f"  错误信息: {result.get('error', '未知错误')}")
        else:
            print("✗ 不是优酷链接")
    
    print("\n" + "=" * 80)
    print("解析接口测试")
    print("=" * 80)
    
    # 测试所有解析接口
    test_url = test_urls[0]  # 使用第一个链接测试
    print(f"测试链接: {test_url[:50]}...")
    
    api_results = parser.test_all_apis(test_url)
    
    print(f"\n总共测试了 {len(api_results)} 个解析接口:")
    print("-" * 60)
    
    for result in api_results:
        status = "✓ 可用" if result.get('available', False) else "✗ 不可用"
        print(f"{result['name']}: {status}")
        if result.get('response_time'):
            print(f"  响应时间: {result['response_time']:.2f}秒")
        if result.get('error'):
            print(f"  错误: {result['error']}")
        print()
    
    print("=" * 80)
    print("优酷专线解析器信息")
    print("=" * 80)
    
    api_info = parser.get_api_info()
    print(f"支持的解析线路数量: {len(api_info)}")
    
    for info in api_info:
        print(f"线路: {info['name']}")
        print(f"优先级: {info['priority']}")
        print(f"类型: {info['type']}")
        print("-" * 40)

if __name__ == "__main__":
    test_youku_urls() 