import matplotlib.pyplot as plt
import numpy as np

# 1. 数据准备
months = ['1月', '2月', '3月', '4月', '5月', '6月']
v2021 = [1686, 1345, 1934, 1658, 1865, 1936]
v2022 = [1385, 1846, 1654, 1936, 2564, 2236]

bg_color = '#1A1E43'
color_2021 = '#E74E69'
color_2022 = '#0070C0'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布
fig, ax = plt.subplots(figsize=(832 / 144, 622 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制两条折线
x = np.arange(len(months))
ax.plot(x, v2021, color=color_2021, linewidth=1.5, zorder=3)
ax.plot(x, v2022, color=color_2022, linewidth=1.5, zorder=3)

# 5. 圆形标记
ax.scatter(x, v2021, marker='o', s=25, facecolor=color_2021,
           edgecolor=bg_color, linewidth=0.75, zorder=4)
ax.scatter(x, v2022, marker='o', s=25, facecolor=color_2022,
           edgecolor=bg_color, linewidth=0.75, zorder=4)

# 6. 数据标签（上面的点标在上方，下面的点标在下方，与点保持距离）
offset = 200
for i, v in enumerate(v2021):
    if v > v2022[i]:
        ax.text(i, v + offset, str(v), fontsize=8, color='#FFFFFF', ha='center', va='center', zorder=5)
    else:
        ax.text(i, v - offset, str(v), fontsize=8, color='#FFFFFF', ha='center', va='center', zorder=5)

for i, v in enumerate(v2022):
    if v > v2021[i]:
        ax.text(i, v + offset, str(v), fontsize=8, color='#FFFFFF', ha='center', va='center', zorder=5)
    else:
        ax.text(i, v - offset, str(v), fontsize=8, color='#FFFFFF', ha='center', va='center', zorder=5)

# 7. X轴
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=9, color='#FFFFFF')
ax.tick_params(axis='x', length=0)
ax.set_xlim(-0.5, 5.5)

# 8. Y轴
ax.set_ylim(0, 3000)
ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
ax.set_yticklabels(['0', '500', '1000', '1500', '2000', '2500', '3000'], fontsize=8, color='#FFFFFF')
ax.tick_params(axis='y', length=0)

# 9. 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

# 10. 水平虚线网格
ax.grid(axis='y', linestyle=(0, (10, 5)), alpha=0.15, color='#FFFFFF', zorder=1)
ax.set_axisbelow(True)

# 11. 标题和副标题
fig.text(0.08, 0.94, '2022年上半年各月同比去年销量',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.08, 0.85, '上半年同比去年增长明显，5月份同比增长最多，增长近40%',
         fontsize=12, color='#FFFFFF', va='top', ha='left')

# 12. 图例（同一行，线-点-线样式）
legend_y = 0.69
# 2021年
fig.lines.append(plt.Line2D([0.64, 0.65], [legend_y, legend_y], color=color_2021, linewidth=1.5, transform=fig.transFigure))
fig.scatter = fig.add_artist(plt.Circle((0.66, legend_y), 0.003, color=color_2021, transform=fig.transFigure, zorder=5))
fig.lines.append(plt.Line2D([0.67, 0.68], [legend_y, legend_y], color=color_2021, linewidth=1.5, transform=fig.transFigure))
fig.text(0.69, legend_y, '2021年', fontsize=8, color='#FFFFFF', va='center', ha='left')
# 2022年
fig.lines.append(plt.Line2D([0.78, 0.79], [legend_y, legend_y], color=color_2022, linewidth=1.5, transform=fig.transFigure))
fig.add_artist(plt.Circle((0.80, legend_y), 0.003, color=color_2022, transform=fig.transFigure, zorder=5))
fig.lines.append(plt.Line2D([0.81, 0.82], [legend_y, legend_y], color=color_2022, linewidth=1.5, transform=fig.transFigure))
fig.text(0.83, legend_y, '2022年', fontsize=8, color='#FFFFFF', va='center', ha='left')

# 13. 脚注
fig.text(0.08, 0.03, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=9, color='#AAAAAA', va='bottom', ha='left')

# 14. 绘图区域
ax.set_position([0.130, 0.151, 0.814, 0.490])

# 15. 保存
plt.savefig(r'D:\数据可视化\第一章前15\对比折线图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '对比折线图.png' 已成功生成！")
