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
    st.title("🎓 大连理工大学精英家教")
    st.caption("理工学霸 · 严格筛选 · 价格面议")
    st.caption("由理工本科在读学生果果整理制作")

    # 读取数据
    df = load_data()

    if df.empty:
        st.warning("⚠️ 暂无数据，请检查 data.xlsx 是否上传成功")
        return

    # --- 搜索/筛选区域 ---
    with st.expander("🔍 点击筛选老师 (科目/性别/学校)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            # 搜索框：支持搜科目、年级等
            search_term = st.text_input("搜索关键词", placeholder="例如：数学 / 高三 / 物理")
        with c2:
            gender_filter = st.multiselect("性别", options=df['Gender'].unique(), default=df['Gender'].unique())
        with c3:
            # 年级筛选
            grade_filter = st.multiselect("年级", options=df['Grade'].unique(), default=df['Grade'].unique())

    # --- 筛选逻辑 ---
    filtered_df = df[
        (df['Gender'].isin(gender_filter)) & 
        (df['Grade'].isin(grade_filter))
    ]
    
    # 关键词模糊搜索 (搜科目、优势、姓名)
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Subjects'].str.contains(search_term, na=False) |
            filtered_df['Advantage'].str.contains(search_term, na=False) |
            filtered_df['Name'].str.contains(search_term, na=False)
        ]

    st.markdown(f"##### 当前展示: {len(filtered_df)} 位老师")
    st.divider()

    # --- 老师卡片展示 ---
    cols = st.columns(3)
    
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            with st.container(border=True):
                # === A. 头部：姓名 + 性别 + 籍贯 ===
                c_top1, c_top2 = st.columns([3, 2])
                with c_top1:
                    gender_icon = "♂️" if row['Gender'] == '男' else "♀️"
                    st.markdown(f"### {row['Name']} {gender_icon}")
                with c_top2:
                    st.caption(f"📍 {row['Hometown']}") 
                
                # === B. 核心身份 (加粗显示) ===
                st.markdown(f"**{row['University']}**")
                st.text(f"{row['Major']} | {row['Grade']}")
                
                st.divider()

                # === C. 可教科目 (蓝色高亮) ===
                st.info(f"📘 {row['Subjects']}")

                # === D. 个人优势 (折叠) ===
                with st.expander("✨ 个人优势 (点击查看)"):
                    st.write(row['Advantage'])
                
                # === E. 家教经验 (折叠) ===
                with st.expander("📖 家教经验 (点击查看)"):
                    st.write(row['Experience'])
                
                # === F. 底部按钮 ===
                if st.button("💬 预约这位老师", key=f"btn_{idx}"):
                    st.success("👋 家长您好！请添加管理员微信：ahjdcg666")
                    st.caption(f"备注：预约 {row['Name']} 老师")

if __name__ == "__main__":
    main()