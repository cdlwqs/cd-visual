import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 1. 数据
bg_color = '#1A1E43'
categories = ['>=50', '[40,50)', '[30,40)', '[20,30)']
values = [0.125, 0.208, 0.292, 0.375]
colors = ['#37A2DA', '#11A7AD', '#F5C353', '#E74E69']
percent_labels = ['12.5%', '20.8%', '29.2%', '37.5%']

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 834×594 @ 144dpi
fig, ax = plt.subplots(figsize=(834 / 144, 594 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制玉玦图
# 弧角度 = 值 × 720° (每系列2个数据点和为0.5, 弧占 value/0.5 × 360°)
# 所有弧从12点钟(90°)开始, 顺时针延伸 — 对齐面竖直
# 环半径(外径=1.0): 蓝[0.384,0.529], 青[0.541,0.686], 黄[0.698,0.843], 红[0.855,1.000]
ring_specs = [
    (0.384, 0.529),
    (0.541, 0.686),
    (0.698, 0.843),
    (0.855, 1.000),
]

for i, (val, color) in enumerate(zip(values, colors)):
    r_inner, r_outer = ring_specs[i]
    arc_angle = val * 720
    theta1 = 90 - arc_angle
    theta2 = 90
    wedge = mpatches.Wedge((0, 0), r_outer, theta1, theta2,
                           width=r_outer - r_inner, facecolor=color,
                           edgecolor='none', zorder=3)
    ax.add_patch(wedge)

# 4.5 黄色引导线
# 第一条: 蓝色弧中点(45°, r=0.4565) → 12.5%标签附近
blue_mid_x = 0.4565 * np.cos(np.radians(45))
blue_mid_y = 0.4565 * np.sin(np.radians(45))
ax.plot([blue_mid_x, 0.42], [blue_mid_y, -0.05],
        color='#F5C353', linewidth=0.8, alpha=0.7, zorder=4)

# 第二条: 青色弧中点(15°, r=0.6135) → 弧尽头偏下 → 横线 → 20.8%标签
cyan_mid_x = 0.6135 * np.cos(np.radians(15))
cyan_mid_y = 0.6135 * np.sin(np.radians(15))
cyan_end_x = 0.6135 * np.cos(np.radians(-60))
cyan_turn_x = 0.65 * np.cos(np.radians(-60))
cyan_turn_y = 0.65 * np.sin(np.radians(-60))
ax.plot([cyan_mid_x, cyan_turn_x], [cyan_mid_y, cyan_turn_y],
        color='#F5C353', linewidth=0.8, alpha=0.7, zorder=4)
ax.plot([cyan_turn_x, 0.269], [cyan_turn_y, cyan_turn_y],
        color='#F5C353', linewidth=0.8, alpha=0.7, zorder=4)

# 5. 设置坐标轴
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.set_aspect('equal')
ax.axis('off')
ax.set_position([0.270, 0.100, 0.468, 0.657])

# 6. 数据标签 (fig坐标, 从原图像素精确测量+修正渲染偏移)
fig.text(0.593, 0.396, '12.5%', fontsize=9, color='#F2F2F2', ha='center', va='center')
fig.text(0.532, 0.256, '20.8%', fontsize=9, color='#F2F2F2', ha='center', va='center')
fig.text(0.403, 0.256, '29.2%', fontsize=9, color='#F2F2F2', ha='center', va='center')
fig.text(0.300, 0.464, '37.5%', fontsize=9, color='#F2F2F2', ha='center', va='center')

# 7. 类别标签 (统一x坐标, 整体上移)
fig.text(0.458, 0.719, '[20,30)', fontsize=9, color='#F2F2F2', ha='center', va='center')
fig.text(0.458, 0.668, '[30,40)', fontsize=9, color='#F2F2F2', ha='center', va='center')
fig.text(0.458, 0.618, '[40,50)', fontsize=9, color='#F2F2F2', ha='center', va='center')
fig.text(0.458, 0.570, '>=50', fontsize=9, color='#F2F2F2', ha='center', va='center')

# 8. 标题和副标题
fig.text(0.04, 0.95, '2022年上半年年龄分布',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.04, 0.86, '公司平均年龄32.5，23-30员工比例最高',
         fontsize=14, color='#FFFFFF', va='top', ha='left')

# 9. 脚注
fig.text(0.04, 0.03, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 10. 保存
plt.savefig(r'D:\数据可视化\第一章后15\玉玦图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '玉玦图.png' 已成功生成！")
