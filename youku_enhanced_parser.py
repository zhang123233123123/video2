#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
优酷视频增强解析器
专门针对优酷平台的视频解析，包含多种解析策略和备用线路
"""

import requests
import re
import json
import random
import time
import base64
from urllib.parse import urlparse, parse_qs, unquote, quote
from typing import Optional, Dict, Any, List

class YoukuEnhancedParser:
    """优酷增强解析器"""
    
    def __init__(self):
        # 多个用户代理，随机轮换
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # 优酷专用解析接口
        self.youku_parse_apis = [
            {
                'name': '优酷专线1-高清稳定',
                'url': 'https://jx.618g.com/?url={}',
                'type': 'iframe',
                'priority': 1
            },
            {
                'name': '优酷专线2-超清画质',
                'url': 'https://jx.jsonplayer.com/player/?url={}',
                'type': 'iframe',
                'priority': 2
            },
            {
                'name': '优酷专线3-快速解析',
                'url': 'https://api.bb3.buzz/jiexi/?url={}',
                'type': 'iframe',
                'priority': 3
            },
            {
                'name': '优酷专线4-VIP专用',
                'url': 'https://www.1717yun.com/jx/ty.php?url={}',
                'type': 'iframe',
                'priority': 4
            },
            {
                'name': '优酷专线5-无广告',
                'url': 'https://vip.gaotian.love/api/?key=8CNrwNGWumgOHNK5r3H7jsDJb1XhPp&url={}',
                'type': 'iframe',
                'priority': 5
            },
            {
                'name': '优酷专线6-备用线路',
                'url': 'https://okjx.cc/?url={}',
                'type': 'iframe',
                'priority': 6
            },
            {
                'name': '优酷专线7-极速播放',
                'url': 'https://jx.bozrc.com:4433/player/?url={}',
                'type': 'iframe',
                'priority': 7
            },
            {
                'name': '优酷专线8-智能解析',
                'url': 'https://jx.xmflv.com/?url={}',
                'type': 'iframe',
                'priority': 8
            }
        ]
        
        # 请求会话
        self.session = requests.Session()
        
        # 优酷链接正则模式
        self.youku_patterns = [
            r'v\.youku\.com/v_show/id_([^.]+)\.html',
            r'v\.youku\.com/video\?vid=([^&]+)',
            r'youku\.com.*vid[=:]([^&\s]+)',
            r'youku\.com.*videoId[=:]([^&\s]+)',
            r'youku\.com/.*?/id_([^.]+)\.html'
        ]
    
    def get_random_headers(self) -> Dict[str, str]:
        """获取随机请求头"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.youku.com/',
            'Origin': 'https://www.youku.com'
        }
    
    def is_youku_url(self, url: str) -> bool:
        """检测是否为优酷链接"""
        return any(re.search(pattern, url) for pattern in ['youku\.com', 'v\.youku\.com'])
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """提取优酷视频ID"""
        # 尝试多种ID提取方式
        for pattern in self.youku_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # 如果直接匹配失败，尝试从页面内容提取
        try:
            headers = self.get_random_headers()
            response = self.session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                html = response.text
                
                # 多种ID提取模式
                id_patterns = [
                    r'"videoId"\s*:\s*"([^"]+)"',
                    r'"vid"\s*:\s*"([^"]+)"',
                    r'videoId["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                    r'data-id["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                    r'/id_([^.]+)\.html',
                    r'vid[=:]([^&\s]+)'
                ]
                
                for pattern in id_patterns:
                    match = re.search(pattern, html)
                    if match:
                        return match.group(1)
        except:
            pass
        
        return None
    
    def parse_youku_video(self, url: str) -> Dict[str, Any]:
        """解析优酷视频（增强版）"""
        try:
            # 基本信息初始化
            result = {
                'success': False,
                'platform': '优酷',
                'original_url': url,
                'title': '优酷视频',
                'duration': '未知',
                'thumbnail': '',
                'vid': '',
                'parse_urls': [],
                'best_parse_url': None,
                'vip_content': True,
                'parse_method': 'enhanced'
            }
            
            # 提取视频ID
            vid = self.extract_video_id(url)
            if vid:
                result['vid'] = vid
            
            # 获取页面信息
            page_info = self._get_page_info(url)
            if page_info:
                result.update(page_info)
            
            # 生成所有解析链接
            parse_urls = self._generate_parse_urls(url)
            result['parse_urls'] = parse_urls
            
            if parse_urls:
                result['best_parse_url'] = parse_urls[0]['url']
                result['success'] = True
            
            # 测试最佳解析链接
            if result['success']:
                best_api = self._test_best_parse_api(url)
                if best_api:
                    result['best_parse_url'] = best_api['url']
                    result['recommended_api'] = best_api['name']
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'优酷专线解析错误: {str(e)}',
                'platform': '优酷',
                'original_url': url
            }
    
    def _get_page_info(self, url: str) -> Optional[Dict[str, Any]]:
        """获取页面基本信息"""
        try:
            headers = self.get_random_headers()
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                info = {}
                
                # 提取标题
                title_patterns = [
                    r'<title>(.*?)</title>',
                    r'"title"\s*:\s*"([^"]+)"',
                    r'data-title["\']?\s*[:=]\s*["\']([^"\']+)["\']'
                ]
                
                for pattern in title_patterns:
                    match = re.search(pattern, html)
                    if match:
                        title = match.group(1).strip()
                        # 清理标题
                        title = re.sub(r'\s*-\s*优酷.*$', '', title)
                        title = re.sub(r'\s*-\s*视频.*$', '', title)
                        if title and len(title) > 2:
                            info['title'] = title
                            break
                
                # 提取缩略图
                thumb_patterns = [
                    r'"poster"\s*:\s*"([^"]+)"',
                    r'"img"\s*:\s*"([^"]+)"',
                    r'data-poster["\']?\s*[:=]\s*["\']([^"\']+)["\']'
                ]
                
                for pattern in thumb_patterns:
                    match = re.search(pattern, html)
                    if match:
                        thumbnail = match.group(1)
                        if thumbnail.startswith('http'):
                            info['thumbnail'] = thumbnail
                            break
                
                # 提取时长
                duration_patterns = [
                    r'"duration"\s*:\s*(\d+)',
                    r'data-duration["\']?\s*[:=]\s*["\']?(\d+)["\']?'
                ]
                
                for pattern in duration_patterns:
                    match = re.search(pattern, html)
                    if match:
                        duration_seconds = int(match.group(1))
                        info['duration'] = self._format_duration(duration_seconds)
                        break
                
                return info if info else None
                
        except Exception as e:
            print(f"获取页面信息失败: {e}")
            return None
    
    def _generate_parse_urls(self, original_url: str) -> List[Dict[str, str]]:
        """生成所有解析链接"""
        encoded_url = quote(original_url, safe=':/?#[]@!$&\'()*+,;=')
        
        parse_urls = []
        for api in sorted(self.youku_parse_apis, key=lambda x: x['priority']):
            parse_url = api['url'].format(encoded_url)
            parse_urls.append({
                'name': api['name'],
                'url': parse_url,
                'type': api['type'],
                'priority': api['priority']
            })
        
        return parse_urls
    
    def _test_best_parse_api(self, original_url: str) -> Optional[Dict[str, Any]]:
        """测试并返回最佳解析接口"""
        encoded_url = quote(original_url, safe=':/?#[]@!$&\'()*+,;=')
        
        # 按优先级测试接口
        for api in sorted(self.youku_parse_apis, key=lambda x: x['priority']):
            try:
                parse_url = api['url'].format(encoded_url)
                headers = self.get_random_headers()
                
                # 快速测试接口可用性
                response = self.session.head(parse_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    return {
                        'name': api['name'],
                        'url': parse_url,
                        'type': api['type'],
                        'priority': api['priority'],
                        'response_time': response.elapsed.total_seconds()
                    }
                    
            except Exception as e:
                continue
        
        return None
    
    def _format_duration(self, seconds: int) -> str:
        """格式化时长"""
        if seconds == 0:
            return "未知"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def test_all_apis(self, test_url: str) -> List[Dict[str, Any]]:
        """测试所有解析接口"""
        results = []
        encoded_url = quote(test_url, safe=':/?#[]@!$&\'()*+,;=')
        
        for api in self.youku_parse_apis:
            try:
                parse_url = api['url'].format(encoded_url)
                headers = self.get_random_headers()
                
                start_time = time.time()
                response = self.session.get(parse_url, headers=headers, timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    # 检测是否包含视频相关内容
                    content = response.text.lower()
                    has_video_content = any(keyword in content for keyword in [
                        'video', 'mp4', 'iframe', 'player', 'source'
                    ])
                    
                    results.append({
                        'name': api['name'],
                        'url': parse_url,
                        'available': has_video_content,
                        'response_time': response_time,
                        'status_code': response.status_code,
                        'priority': api['priority']
                    })
                else:
                    results.append({
                        'name': api['name'],
                        'url': parse_url,
                        'available': False,
                        'error': f'状态码: {response.status_code}',
                        'priority': api['priority']
                    })
                    
            except Exception as e:
                results.append({
                    'name': api['name'],
                    'url': api['url'].format(test_url),
                    'available': False,
                    'error': str(e),
                    'priority': api['priority']
                })
        
        return sorted(results, key=lambda x: x['priority'])
    
    def get_api_info(self) -> List[Dict[str, Any]]:
        """获取所有解析接口信息"""
        return [
            {
                'name': api['name'],
                'url': api['url'].replace('{}', '[视频链接]'),
                'type': api['type'],
                'priority': api['priority']
            }
            for api in sorted(self.youku_parse_apis, key=lambda x: x['priority'])
        ] 