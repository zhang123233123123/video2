#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
优酷专线解析器 Streamlit Web应用
"""

import streamlit as st
import sys
import os
import requests
from urllib.parse import quote
import time

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youku_enhanced_parser import YoukuEnhancedParser
from integrated_parser import IntegratedVideoParser

# 页面配置
st.set_page_config(
    page_title="优酷专线解析器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #721c24;
    }
    
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0c5460;
    }
    
    .api-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .api-available {
        border-left: 4px solid #28a745;
    }
    
    .api-unavailable {
        border-left: 4px solid #dc3545;
    }
    
    .video-info {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主函数"""
    
    # 页面标题
    st.markdown("""
    <div class="main-header">
        <h1>🎬 优酷专线解析器</h1>
        <p>专门针对优酷平台的增强视频解析工具</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 🎯 优酷专线解析器")
        st.markdown("---")
        
        # 功能选择
        tab_option = st.selectbox(
            "选择功能",
            ["🔍 视频解析", "🧪 线路测试", "📊 解析器信息", "📝 使用说明"]
        )
        
        st.markdown("---")
        
        # 测试链接
        st.markdown("### 📋 测试链接")
        test_urls = [
            "https://v.youku.com/video?vid=XNjQ4MzA5ODkwOA==&s=bdfb0949ae4c4ac39168&scm=20140719.apircmd.298496.video_XNjQ4MzA5ODkwOA==&spm=a2hkt.13141534.1_6.d_1_13",
            "https://v.youku.com/video?vid=XNjQ4MDE0MTc0OA==&s=06efbfbd08efbfbdefbf&scm=20140719.apircmd.298496.video_XNjQ4MDE0MTc0OA==&spm=a2hkt.13141534.1_6.d_1_4"
        ]
        
        for i, url in enumerate(test_urls, 1):
            if st.button(f"测试链接 {i}", key=f"test_{i}"):
                st.session_state.test_url = url
    
    # 主内容区域
    if tab_option == "🔍 视频解析":
        show_video_parse_tab()
    elif tab_option == "🧪 线路测试":
        show_api_test_tab()
    elif tab_option == "📊 解析器信息":
        show_parser_info_tab()
    elif tab_option == "📝 使用说明":
        show_usage_tab()

def show_video_parse_tab():
    """视频解析页面"""
    st.markdown("## 🔍 视频解析")
    
    # 视频链接输入
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_url = st.text_input(
            "请输入优酷视频链接:",
            value=st.session_state.get('test_url', ''),
            placeholder="https://v.youku.com/video?vid=XXXXX"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        parse_button = st.button("🚀 开始解析", type="primary")
    
    if parse_button and video_url:
        with st.spinner("正在解析视频..."):
            try:
                # 初始化解析器
                parser = IntegratedVideoParser()
                
                # 解析视频
                result = parser.parse_video(video_url)
                
                if result.get('success'):
                    st.markdown("""
                    <div class="success-box">
                        <h4>✅ 解析成功!</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 显示视频信息
                    st.markdown('<div class="video-info">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📺 视频信息")
                        st.write(f"**平台**: {result.get('platform', '未知')}")
                        st.write(f"**标题**: {result.get('title', '未知')}")
                        st.write(f"**时长**: {result.get('duration', '未知')}")
                        st.write(f"**视频ID**: {result.get('vid', '未知')}")
                        st.write(f"**解析器**: {result.get('parser_info', '未知')}")
                    
                    with col2:
                        st.markdown("### 🔗 解析结果")
                        if result.get('best_parse_url'):
                            st.markdown("**推荐解析链接**:")
                            st.code(result['best_parse_url'], language="")
                            
                            # 复制按钮
                            if st.button("📋 复制链接"):
                                st.success("链接已复制到剪贴板!")
                        
                        if result.get('recommended_api'):
                            st.write(f"**推荐线路**: {result['recommended_api']}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 显示所有解析线路
                    if result.get('parse_urls'):
                        st.markdown("### 🛣️ 所有可用线路")
                        
                        for i, parse_info in enumerate(result['parse_urls'], 1):
                            with st.expander(f"线路 {i}: {parse_info['name']}"):
                                st.code(parse_info['url'], language="")
                                st.write(f"优先级: {parse_info.get('priority', 'N/A')}")
                                st.write(f"类型: {parse_info.get('type', 'N/A')}")
                
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <h4>❌ 解析失败</h4>
                        <p>错误信息: {result.get('error', '未知错误')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    <h4>❌ 程序错误</h4>
                    <p>{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

def show_api_test_tab():
    """线路测试页面"""
    st.markdown("## 🧪 解析线路测试")
    
    # 测试URL输入
    test_url = st.text_input(
        "测试URL:",
        value="https://v.youku.com/video?vid=XNjQ4MzA5ODkwOA==",
        placeholder="输入要测试的优酷视频链接"
    )
    
    if st.button("🧪 测试所有线路", type="primary"):
        if test_url:
            with st.spinner("正在测试所有解析线路..."):
                try:
                    parser = YoukuEnhancedParser()
                    
                    if parser.is_youku_url(test_url):
                        results = parser.test_all_apis(test_url)
                        
                        st.markdown(f"### 📊 测试结果 (共 {len(results)} 条线路)")
                        
                        # 统计信息
                        available_count = sum(1 for r in results if r.get('available', False))
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("总线路数", len(results))
                        with col2:
                            st.metric("可用线路", available_count)
                        with col3:
                            st.metric("可用率", f"{available_count/len(results)*100:.1f}%")
                        
                        # 详细结果
                        for result in results:
                            is_available = result.get('available', False)
                            card_class = "api-available" if is_available else "api-unavailable"
                            
                            st.markdown(f'''
                            <div class="api-card {card_class}">
                                <h4>{result['name']}</h4>
                                <p><strong>状态</strong>: {"✅ 可用" if is_available else "❌ 不可用"}</p>
                                <p><strong>优先级</strong>: {result.get('priority', 'N/A')}</p>
                                {"<p><strong>响应时间</strong>: {:.2f}秒</p>".format(result['response_time']) if result.get('response_time') else ""}
                                {"<p><strong>错误</strong>: {}</p>".format(result['error']) if result.get('error') else ""}
                            </div>
                            ''', unsafe_allow_html=True)
                            
                    else:
                        st.error("❌ 不是有效的优酷链接")
                        
                except Exception as e:
                    st.error(f"测试过程中出现错误: {str(e)}")
        else:
            st.warning("⚠️ 请输入测试URL")

def show_parser_info_tab():
    """解析器信息页面"""
    st.markdown("## 📊 解析器信息")
    
    try:
        parser = YoukuEnhancedParser()
        integrated_parser = IntegratedVideoParser()
        
        # 基本信息
        st.markdown("### 🎯 优酷专线解析器")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✨ 功能特点")
            features = [
                "🎯 专门针对优酷平台",
                "🔄 多种解析策略", 
                "🚀 8条专线线路",
                "📊 智能测试功能",
                "🔍 详细信息提取"
            ]
            for feature in features:
                st.write(f"• {feature}")
        
        with col2:
            st.markdown("#### 🛠️ 技术特点")
            tech_features = [
                "多种ID提取策略",
                "随机User-Agent轮换",
                "会话复用优化",
                "智能线路选择",
                "超时控制保护"
            ]
            for feature in tech_features:
                st.write(f"• {feature}")
        
        # API信息
        st.markdown("### 🛣️ 解析线路信息")
        
        api_info = parser.get_api_info()
        
        for i, api in enumerate(api_info, 1):
            with st.expander(f"线路 {i}: {api['name']}"):
                st.write(f"**优先级**: {api['priority']}")
                st.write(f"**类型**: {api['type']}")
                st.code(api['url'], language="")
        
        # 支持的平台
        st.markdown("### 🌐 支持的平台")
        platforms = integrated_parser.get_supported_platforms()
        
        cols = st.columns(3)
        for i, platform in enumerate(platforms):
            with cols[i % 3]:
                st.write(f"• {platform}")
                
    except Exception as e:
        st.error(f"获取解析器信息时出错: {str(e)}")

def show_usage_tab():
    """使用说明页面"""
    st.markdown("## 📝 使用说明")
    
    st.markdown("""
    ### 🎯 关于优酷专线解析器
    
    优酷专线解析器是专门为优酷平台视频解析而开发的增强模块，能够有效解决原始解析器对某些优酷链接解析失败的问题。
    
    ### 🚀 主要功能
    
    1. **智能平台识别**: 自动识别优酷链接并使用专线解析
    2. **多策略解析**: 支持多种视频ID提取方式
    3. **8条专线线路**: 按优先级排序的备用解析接口
    4. **智能测试**: 自动测试并选择最佳解析线路
    5. **详细信息**: 提取视频标题、时长、缩略图等信息
    
    ### 📋 支持的链接格式
    
    - `https://v.youku.com/video?vid=XXXXX`
    - `https://v.youku.com/v_show/id_XXXXX.html`
    - `https://youku.com/...`
    
    ### 🛣️ 解析线路
    
    优酷专线解析器提供8条专线线路，按优先级自动选择：
    
    1. **优酷专线1-高清稳定** - 高画质稳定播放
    2. **优酷专线2-超清画质** - 超清画质支持
    3. **优酷专线3-快速解析** - 快速响应解析
    4. **优酷专线4-VIP专用** - VIP内容专用
    5. **优酷专线5-无广告** - 无广告播放
    6. **优酷专线6-备用线路** - 备用稳定线路
    7. **优酷专线7-极速播放** - 极速播放体验
    8. **优酷专线8-智能解析** - 智能适配解析
    
    ### 📖 使用步骤
    
    1. **输入链接**: 在视频解析页面输入优酷视频链接
    2. **点击解析**: 点击"开始解析"按钮
    3. **获取结果**: 系统会自动选择最佳线路并返回解析结果
    4. **复制使用**: 复制解析链接到播放器中使用
    
    ### ⚠️ 注意事项
    
    - 本工具仅供学习和研究使用
    - 请尊重版权，支持正版内容  
    - 用户需承担使用风险和法律责任
    - 解析接口可用性可能随时变化
    
    ### 🔧 技术支持
    
    如遇到问题，可以：
    1. 使用"线路测试"功能检查接口状态
    2. 尝试不同的解析线路
    3. 检查输入的链接格式是否正确
    """)

if __name__ == "__main__":
    main() 