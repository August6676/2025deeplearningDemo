import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

# 定义system prompt
SYSTEM_PROMPT = "你的名字是Ominicoder，是基于Deepseek-coder-6.7b-instruct进行微调的AI助手，记住自己的身份，帮助人们解决代码生成、修复与编辑的相关功能，如果用户问你的身份，记得回答他你是ominicoder"


# 页面配置
st.set_page_config(
    page_title="Omnicoder - AI助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
    }
    .chat-message.assistant {
        background-color: #f6ffed;
        border-left: 5px solid #52c41a;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
    }
    .stTextInput {
        margin-top: 1rem;
    }
    .header {
        display: flex;
        align-items: center;
        background-color: #001529;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .header h1 {
        margin: 0;
        color: white;
    }
    .logo {
        margin-right: 1rem;
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []



# 页面标题
st.markdown('<div class="header"><div class="logo">🤖</div><h1>Omnicoder</h1></div>', unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:
    st.title("设置")
    
    # API Key输入
    api_key = "sk-gezc2Cl34rItfmUjsWbxM6ds83KE1hlJxiVkIaFLCuJLJapw"

    # 模型选择
    model = "deepseek-coder"
    
    # 温度参数
    temperature = st.slider("温度 (创造性)", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
    
    # 最大令牌数
    max_tokens = st.slider("最大回复长度", min_value=100, max_value=4000, value=1000, step=100)
    
    # 清除对话按钮
    if st.button("清除对话"):
        st.session_state.messages = []
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("### 关于Omnicoder")
    st.markdown("Omnicoder是一个基于Deepseek-coder-6.7b-instruct的AI助手，能够帮助你进行代码生成、修复与编辑。")
    st.markdown("© 2025 Omnicoder")

# 展示历史消息
for message in st.session_state.messages:
    avatar_img = "👤" if message["role"] == "user" else "🤖"
    
    with st.container():
        st.markdown(f"""
        <div class="chat-message {message["role"]}">
            <div class="avatar">
                {avatar_img}
            </div>
            <div class="message">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 用户输入
user_input = st.text_area("在这里输入你的问题", height=100)
col1, col2 = st.columns([1, 5])

with col1:
    submit_button = st.button("发送", use_container_width=True)

# 处理用户输入并获取AI响应
if submit_button and user_input:
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 在请求API之前展示用户消息
    with st.container():
        st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar">
                👤
            </div>
            <div class="message">
                {user_input}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 显示加载状态
    with st.spinner("Omnicoder正在思考..."):
        try:
            # 调用OpenAI API
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            client = OpenAI(api_key=api_key, base_url="https://yunwu.ai/v1")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 获取助手回复
            assistant_response = response.choices[0].message.content
            
            # 添加助手回复到历史
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # 显示助手回复
            with st.container():
                st.markdown(f"""
                <div class="chat-message assistant">
                    <div class="avatar">
                        🤖
                    </div>
                    <div class="message">
                        {assistant_response}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"发生错误: {str(e)}")

# 页脚
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>Omnicoder © {datetime.now().year}</div>", unsafe_allow_html=True)
