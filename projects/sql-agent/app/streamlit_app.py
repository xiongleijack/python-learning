"""
SQL Agent Review 工作台（阶段 C5）

运行：
  cd projects/sql-agent
  streamlit run app/streamlit_app.py
"""

import streamlit as st

st.set_page_config(page_title="SQL Agent", layout="wide")
st.title("SQL Agent — Review 工作台")

request = st.text_area("需求描述", placeholder="例如：统计 bond 表最近 7 天记录数")

if st.button("生成 SQL"):
    st.session_state["pending"] = True
    st.info("TODO: 调用 agent.run_agent(request)")

if st.session_state.get("pending"):
    st.subheader("生成的 SQL")
    sql = st.text_area("SQL（可编辑）", value="-- TODO", height=150)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("批准 · 只读执行"):
            st.warning("TODO: validator + tools.run_readonly_query")
    with col2:
        if st.button("创建 PR"):
            st.warning("TODO: git_ops.create_pr")
    with col3:
        if st.button("拒绝"):
            st.session_state.pop("pending", None)
            st.rerun()
