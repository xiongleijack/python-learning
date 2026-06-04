"""
文档问答 Web 页（阶段 B3）

运行：
  cd projects/doc-agent
  streamlit run app/streamlit_app.py
"""

import streamlit as st

st.set_page_config(page_title="Doc Agent", layout="wide")
st.title("项目文档问答")
st.caption("先实现 src/ 下 index 与 ask，再接入此页面。")

if prompt := st.chat_input("问一个关于项目的问题"):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        st.write("TODO: 调用 retrieve.ask_claude")

if st.button("重建索引"):
    st.info("TODO: 调用 cli.cmd_index")
