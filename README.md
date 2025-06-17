# 优酷专线解析器

## 概述

优酷专线解析器是专门为优酷平台视频解析而开发的增强模块，提供多种解析策略和备用线路，以提高优酷视频的解析成功率。

## 功能特点

- 🎯 **专门针对优酷平台**：专门优化的解析算法
- 🔄 **多种解析策略**：支持多种视频ID提取方式
- 🚀 **8条专线线路**：按优先级排序的解析接口
- 📊 **智能测试**：自动测试最佳解析线路
- 🔍 **详细信息提取**：提取标题、时长、缩略图等信息

## 支持的链接格式

- `https://v.youku.com/video?vid=XXXXX`
- `https://v.youku.com/v_show/id_XXXXX.html`
- `https://youku.com/...`

## 解析线路

### 优酷专线线路（按优先级排序）

1. **优酷专线1-高清稳定** - `https://jx.618g.com/`
2. **优酷专线2-超清画质** - `https://jx.jsonplayer.com/`
3. **优酷专线3-快速解析** - `https://api.bb3.buzz/`
4. **优酷专线4-VIP专用** - `https://www.1717yun.com/`
5. **优酷专线5-无广告** - `https://vip.gaotian.love/`
6. **优酷专线6-备用线路** - `https://okjx.cc/`
7. **优酷专线7-极速播放** - `https://jx.bozrc.com/`
8. **优酷专线8-智能解析** - `https://jx.xmflv.com/`

## 使用方法

### 1. 基本使用

```python
from youku_enhanced_parser import YoukuEnhancedParser

# 初始化解析器
parser = YoukuEnhancedParser()

# 解析优酷视频
url = "https://v.youku.com/video?vid=XNjQ4MzA5ODkwOA=="
result = parser.parse_youku_video(url)

if result['success']:
    print(f"标题: {result['title']}")
    print(f"最佳解析链接: {result['best_parse_url']}")
else:
    print(f"解析失败: {result['error']}")
```

### 2. 集成使用

```python
from integrated_parser import IntegratedVideoParser

# 初始化集成解析器
parser = IntegratedVideoParser()

# 自动识别平台并解析
result = parser.parse_video(url)

# 优酷链接会自动使用专线解析
# 其他平台使用原始解析器
```

### 3. 测试所有线路

```python
# 测试所有解析接口
api_results = parser.test_all_apis(url)

for result in api_results:
    print(f"{result['name']}: {'可用' if result['available'] else '不可用'}")
```

## 测试脚本

### 运行优酷专线测试

```bash
cd youku_parser
python test_youku_parser.py
```

### 运行集成解析器测试

```bash
cd youku_parser  
python integrated_parser.py
```

## 解析结果格式

```python
{
    'success': True,                    # 解析是否成功
    'platform': '优酷',                # 平台名称
    'title': '视频标题',               # 视频标题
    'duration': '00:45:30',            # 视频时长
    'thumbnail': 'http://...',         # 缩略图URL
    'vid': 'XNjQ4MzA5ODkwOA==',       # 视频ID
    'parse_urls': [...],               # 所有解析链接
    'best_parse_url': 'http://...',    # 推荐的最佳解析链接
    'recommended_api': '优酷专线1',     # 推荐的解析线路
    'vip_content': True,               # 是否为VIP内容
    'parse_method': 'enhanced'         # 解析方法
}
```

## 技术特点

### 多种ID提取策略

- URL参数解析：`vid=XXXXX`
- 页面内容提取：从HTML中提取videoId
- 正则匹配：支持多种链接格式
- 智能识别：自动适配不同的链接格式

### 请求优化

- 随机User-Agent轮换
- 优化的请求头设置
- 会话复用提高效率
- 超时控制防止阻塞

### 智能测试

- 按优先级测试接口
- 响应时间统计
- 内容检测验证
- 自动选择最佳线路

## 解决的问题

1. **原始解析器对某些优酷链接解析失败**
   - 通过多种ID提取策略提高成功率
   
2. **不同格式的优酷链接支持不完整**
   - 支持多种链接格式的识别和解析
   
3. **解析线路单一**
   - 提供8条专线备用线路
   
4. **缺乏针对性优化**
   - 专门针对优酷平台的优化策略

## 注意事项

- 本工具仅供学习和研究使用
- 请尊重版权，支持正版内容
- 用户需承担使用风险和法律责任
- 解析接口可用性可能随时变化

## 目录结构

```
youku_parser/
├── __init__.py                 # 模块初始化
├── youku_enhanced_parser.py    # 优酷增强解析器
├── integrated_parser.py        # 集成解析器
├── test_youku_parser.py       # 优酷解析器测试
└── README.md                  # 说明文档
```

## 更新日志

### v1.0.0
- 初始版本发布
- 支持8条优酷专线线路
- 多种ID提取策略
- 智能线路测试功能
- 集成到现有系统 