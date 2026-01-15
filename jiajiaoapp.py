import streamlit as st
import pandas as pd
import os

# --- 1. 页面基础设置 ---
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
    st.title("🎓 精英家教严选")
    
    # 读取数据
    df = load_data()

    if df.empty:
        st.warning("⚠️ 暂无数据，请运行 generate_new_data.py 生成新表格")
        return

    # --- 筛选区域 (顶部展开式) ---
    with st.expander("🔍 筛选老师 (点击展开)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            subject_search = st.text_input("搜索科目 (例如: 数学)", placeholder="输入科目关键词...")
        with c2:
            gender_filter = st.multiselect("性别", options=df['Gender'].unique(), default=df['Gender'].unique())
        with c3:
            # 获取所有学校并去重
            uni_filter = st.multiselect("学校", options=df['University'].unique(), default=df['University'].unique())

    # --- 执行筛选逻辑 ---
    # 1. 筛选性别和学校
    filtered_df = df[
        (df['Gender'].isin(gender_filter)) & 
        (df['University'].isin(uni_filter))
    ]
    # 2. 搜索科目 (模糊搜索)
    if subject_search:
        filtered_df = filtered_df[filtered_df['Subjects'].str.contains(subject_search, na=False)]

    st.caption(f"当前展示: {len(filtered_df)} 位老师")
    st.divider()

    # --- 简历卡片展示区 ---
    # 手机端自动单列，电脑端三列
    cols = st.columns(3)
    
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            # 每个老师一个边框卡片
            with st.container(border=True):
                # === A. 头部信息：姓名+价格 ===
                c_top1, c_top2 = st.columns([3, 2])
                with c_top1:
                    # 姓名 + 性别图标
                    gender_icon = "♂️" if row['Gender'] == '男' else "♀️"
                    st.markdown(f"### {row['Name']} {gender_icon}")
                with c_top2:
                    st.markdown(f"#### <span style='color:red'>¥{row['Price']}/h</span>", unsafe_allow_html=True)
                
                # === B. 基础背景 (学校 | 专业 | 年级) ===
                # 用灰色小字显示，显得很整洁
                st.markdown(f"**{row['University']}** · {row['Major']}") 
                st.caption(f"{row['Grade']} | 籍贯: {row['Hometown']} | {row['Age']}岁")
                
                st.divider() # 分割线

                # === C. 可教科目 ===
                st.markdown("**📘 可教科目**")
                st.info(f"{row['Subjects']}")

                # === D. 优势与经验 (折叠显示，节省空间) ===
                with st.expander("✨ 查看个人优势"):
                    st.markdown(row['Advantage'])
                
                with st.expander("📖 查看家教经验"):
                    st.markdown(row['Experience'])
                
                # === E. 底部按钮 ===
                st.button("📞 联系老师", key=f"btn_{idx}", help="请联系管理员微信预约")

if __name__ == "__main__":
    main()