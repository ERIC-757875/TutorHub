import streamlit as st
import pandas as pd
import os

# 1. 页面配置
st.set_page_config(page_title="精英家教库", page_icon="🎓", layout="wide")

# 2. 模拟数据 (如果没找到Excel，就用这个)
def create_dummy_data():
    data = {
        'Name': ['张伟', '李娜', '王强', 'Emily'],
        'Subject': ['数学', '英语', '物理', '雅思'],
        'University': ['北京大学', '复旦大学', '清华大学', 'UC Berkeley'],
        'Gender': ['男', '女', '男', '女'],
        'Price': [200, 250, 300, 400],
        'Tags': ['奥数金牌', '专攻口语', '物理竞赛', '托福115'],
        'Description': ['拥有5年奥数辅导经验...', '曾在新东方任教...', '擅长力学分析...', '美本申请专家...']
    }
    return pd.DataFrame(data)

# 3. 加载数据函数
def load_data():
    file_path = 'data.xlsx'
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        st.warning("⚠️ 还没找到 data.xlsx 文件，目前显示的是测试数据。")
        return create_dummy_data()

# 4. 登录锁
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("🔒 内部家教系统")
    password = st.text_input("请输入访问密码", type="password")
    if st.button("登录"):
        if password == "888888":  # ===> 密码在这里修改 <===
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("密码错误")

def main_page():
    st.sidebar.title("🔍 筛选老师")
    df = load_data()
    
    # 侧边栏筛选
    subject = st.sidebar.multiselect("选择科目", options=df['Subject'].unique(), default=df['Subject'].unique())
    gender = st.sidebar.multiselect("选择性别", options=df['Gender'].unique(), default=df['Gender'].unique())
    
    # 过滤数据
    filtered_df = df[(df['Subject'].isin(subject)) & (df['Gender'].isin(gender))]

    st.title("🎓 精英家教展示")
    st.markdown(f"当前展示 **{len(filtered_df)}** 位老师")
    st.divider()

    # 展示卡片
    cols = st.columns(3)
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            with st.container(border=True):
                st.subheader(f"{row['Name']} 老师")
                st.caption(f"🏫 {row['University']} | {row['Subject']}")
                st.write(f"🏷️ `{row['Tags']}`")
                st.write(f"💰 **¥{row['Price']}/小时**")
                with st.expander("查看详情"):
                    st.write(row['Description'])
                    st.info("预约请联系管理员微信：Boss_User")

# 5. 程序入口
if not st.session_state.logged_in:
    login_page()
else:
    main_page()