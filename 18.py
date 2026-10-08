import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 1. 数据
bg_color = '#1A1E43'
# 从内到外: 人力部, 行政部, 财务部, 工程部, 采购部, 销售部
departments = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']
values = [130, 226, 238, 293, 326, 451]
total = 832
colors = ['#7030A0', '#0070C0', '#37A2DA', '#11A7AD', '#F5C353', '#E74E69']

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×622 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 622 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制跑道图
# 6个同心环弧, 都从90°(12点钟)开始, 顺时针延伸
# 环半径(外径=1.0, 从内到外, 基于像素测量 center=(378,359) R=203)
ring_specs = [
    (0.465, 0.530),  # 人力部(紫)
    (0.550, 0.615),  # 行政部(蓝)
    (0.635, 0.700),  # 财务部(浅蓝)
    (0.720, 0.785),  # 工程部(青)
    (0.805, 0.870),  # 采购部(黄)
    (0.890, 0.955),  # 销售部(红)
]

for i in range(6):
    r_inner, r_outer = ring_specs[i]
    arc_angle = values[i] / total * 360
    theta1 = 90 - arc_angle  # 顺时针
    theta2 = 90
    wedge = mpatches.Wedge((0, 0), r_outer, theta1, theta2,
                           width=r_outer - r_inner, facecolor=colors[i],
                           edgecolor='none', zorder=3)
    ax.add_patch(wedge)

# 5. 设置坐标轴
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_position([0.185, 0.064, 0.537, 0.718])

# 6. 数据标签 (部门名称 + 人数, 在左上方区域)
label_x = 0.399
label_ys = [0.724, 0.696, 0.669, 0.641, 0.613, 0.585]
label_texts = ['销售部 451', '采购部 326', '工程部 293', '财务部 238', '行政部 226', '人力部 130']
for ly, lt in zip(label_ys, label_texts):
    fig.text(label_x, ly, lt, fontsize=6, color='#F2F2F2', ha='center', va='center')

# 7. 标题和副标题
fig.text(0.069, 0.895, '2022年上半年各部门人数',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='center', ha='left')
fig.text(0.067, 0.82, '公司总人数1664，销售部人数最多451，占比27%',
         fontsize=14, color='#FFFFFF', va='center', ha='left')

# 8. 脚注
fig.text(0.048, 0.053, '*注：数据来源于公司人力资源系统，统计日期截止2022.06.30',
         fontsize=8, color='#D9D9D9', va='center', ha='left')

# 9. 保存
plt.savefig(r'D:\数据可视化\第一章后15\跑道图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '跑道图.png' 已成功生成！")
