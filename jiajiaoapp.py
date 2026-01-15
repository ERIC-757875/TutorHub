import streamlit as st
import pandas as pd
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="精英家教库", page_icon="🎓", layout="wide")

# --- 2. 加载数据 ---
@st.cache_data
def load_data():
    file_path = 'data.xlsx'
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        return pd.DataFrame()

# --- 3. 主程序 ---
def main():
    st.title("🎓 大连理工大学学生家教库")
    st.caption("优秀师资 · 网页由理工本科在读学生果果制作") # 这里加了一句提示
    
    # 读取数据
    df = load_data()

    if df.empty:
        st.warning("⚠️ 暂无数据，请运行 generate_new_data.py 生成新表格")
        return

    # --- 搜索/筛选区域 ---
    with st.expander("🔍 筛选老师 (点击展开)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            subject_search = st.text_input("搜索科目", placeholder="例如：数学 / 全科")
        with c2:
            gender_filter = st.multiselect("性别", options=df['Gender'].unique(), default=df['Gender'].unique())
        with c3:
            uni_filter = st.multiselect("学校", options=df['University'].unique(), default=df['University'].unique())

    # --- 筛选逻辑 ---
    filtered_df = df[
        (df['Gender'].isin(gender_filter)) & 
        (df['University'].isin(uni_filter))
    ]
    if subject_search:
        filtered_df = filtered_df[filtered_df['Subjects'].str.contains(subject_search, na=False)]

    st.caption(f"当前展示: {len(filtered_df)} 位老师")
    st.divider()

    # --- 老师卡片展示 ---
    cols = st.columns(3)
    
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            with st.container(border=True):
                # === A. 头部：姓名 + 身份标签 ===
                # 不再显示价格，而是把名字加大，或者加个“实名认证”的标
                c_top1, c_top2 = st.columns([3, 1])
                with c_top1:
                    gender_icon = "♂️" if row['Gender'] == '男' else "♀️"
                    st.markdown(f"### {row['Name']} {gender_icon}")
                with c_top2:
                    # 原来的价格位置，现在放学校Logo或者文字，显得更学术
                    st.caption(f"{row['University']}") 
                
                # === B. 基础信息 ===
                st.markdown(f"**{row['Major']}** · {row['Grade']}")
                st.text(f"籍贯: {row['Hometown']} | {row['Age']}岁")
                
                st.divider()

                # === C. 可教科目 ===
                st.markdown("**📘 可教科目**")
                # 用蓝色背景块突出科目
                st.info(f"{row['Subjects']}")

                # === D. 优势与经验 ===
                with st.expander("✨ 个人优势"):
                    st.write(row['Advantage'])
                
                with st.expander("📖 家教经验"):
                    st.write(row['Experience'])
                
                # === E. 底部引导 (手机端优化版) ===
                # 使用回调逻辑：点击按钮后，显示微信号
                if st.button("💬 咨询详细情况 & 预约", key=f"btn_{idx}"):
                    st.success("👋 家长您好！请添加管理员微信：ahjdcg666")
                    st.caption("添加时请备注：咨询家教")

# 运行
if __name__ == "__main__":
    main()