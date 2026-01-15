import streamlit as st
import pandas as pd
import os

# 1. 页面配置 (设置宽屏模式)
st.set_page_config(page_title="精英家教库", page_icon="🎓", layout="wide")

# 2. 加载数据函数 (带缓存，加载更快)
@st.cache_data
def load_data():
    file_path = 'data.xlsx'
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        # 如果没找到文件，建立空表防止报错
        return pd.DataFrame()

# 3. 主程序
def main():
    st.title("🎓 精英家教展示")
    
    # 加载数据
    df = load_data()

    # 如果表格是空的（或者没找到文件）
    if df.empty:
        st.warning("⚠️ 暂时没有老师数据，请在后台上传 data.xlsx")
        return

    # --- 核心修改：筛选栏移到主页面 (手机更友好) ---
    with st.expander("🔍 点这里筛选老师 (科目/性别)", expanded=False):
        # 创建两列，左边选科目，右边选性别
        c1, c2 = st.columns(2)
        with c1:
            subject_list = df['Subject'].unique().tolist()
            selected_subject = st.multiselect("选择科目", options=subject_list, default=subject_list)
        with c2:
            gender_list = df['Gender'].unique().tolist()
            selected_gender = st.multiselect("选择性别", options=gender_list, default=gender_list)

    # 根据筛选结果过滤数据
    filtered_df = df[
        (df['Subject'].isin(selected_subject)) & 
        (df['Gender'].isin(selected_gender))
    ]

    # 展示统计数字
    st.caption(f"当前展示: {len(filtered_df)} 位老师")
    st.divider()

    # --- 展示老师卡片 ---
    # 手机端会自动把3列变成1列，完美适配
    cols = st.columns(3)
    
    for idx, row in filtered_df.iterrows():
        # 这里的 % 3 是为了让卡片在电脑上横向排列，手机上会自动竖排
        with cols[idx % 3]:
            with st.container(border=True):
                # 第一行：名字 + 价格 (用列以此对齐)
                col_top1, col_top2 = st.columns([2, 1])
                with col_top1:
                    st.subheader(f"{row['Name']}")
                with col_top2:
                    st.markdown(f"#### ¥{row['Price']}")
                
                # 第二行：学校 | 科目
                st.text(f"🏫 {row['University']} | {row['Subject']}")
                
                # 第三行：标签 (比如 '奥数金牌')
                st.info(f"🏷️ {row['Tags']}")
                
                # 第四行：折叠的详细介绍
                with st.expander("查看详细介绍"):
                    st.write(row['Description'])
                    # 醒目的预约按钮
                    st.success("📲 预约请联系管理员微信：Boss_User")

# 运行主程序 (不需要再输入密码了)
if __name__ == "__main__":
    main()