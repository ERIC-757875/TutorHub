import pandas as pd

#这是你要展示的初始数据
data = {
    'Name': ['张伟', '李娜', '王强', 'Emily'],
    'Subject': ['数学', '英语', '物理', '雅思'],
    'University': ['北京大学', '复旦大学', '清华大学', 'UC Berkeley'],
    'Gender': ['男', '女', '男', '女'],
    'Price': [200, 250, 300, 400],
    'Tags': ['奥数金牌', '专攻口语', '物理竞赛', '托福115'],
    'Description': ['拥有5年奥数辅导经验...', '曾在新东方任教...', '擅长力学分析...', '美本申请专家...']
}

# 变成表格
df = pd.DataFrame(data)

# 保存为Excel文件
df.to_excel('data.xlsx', index=False)

print("✅ 成功！data.xlsx 文件已生成！")