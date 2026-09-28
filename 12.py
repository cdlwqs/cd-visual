import matplotlib.pyplot as plt
import numpy as np

# 1. 数据准备
months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
values = [0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704]

bg_color = '#1A1E43'
marker_border = "#FC5666"
line_color = "#FC546E"
label_color = '#FFFFFF'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×590 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 590 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制菱形标记和垂直线
x = np.arange(len(months))

# 垂直drop lines（从数据点到X轴）
for i in range(len(months)):
    ax.plot([x[i], x[i]], [0, values[i]], color=line_color, linewidth=0.75, zorder=2)

# 菱形标记（填充背景色，边框#E74E69）
ax.scatter(x, values, marker='D', s=40, facecolor=bg_color,
           edgecolor=marker_border, linewidth=0.75, zorder=3)

# 5. 数据标签（百分比，在标记上方）
for i in range(len(months)):
    ax.text(x[i], values[i] + 0.06, f'{values[i]*100:.2f}%',
            fontsize=9, color='#FFFFFF', ha='center', va='bottom',
            zorder=5)

# 6. X轴
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=9, color=label_color)
ax.tick_params(axis='x', length=0)
ax.set_xlim(-0.5, 7.5)

# 7. Y轴（隐藏）
ax.set_ylim(0, 0.85)
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 8. X轴轴线（半透明）
ax.spines['bottom'].set_color('#D9D9D9')
ax.spines['bottom'].set_alpha(0.6)
ax.spines['bottom'].set_linewidth(0.5)

# 9. 标题和副标题
fig.text(0.07, 0.94, '2022年1-8月公司计划完成率',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.07, 0.85, '公司整体完成率55%，4月和8月超过70%，2月和6月较低未过半',
         fontsize=12, color='#FFFFFF', va='top', ha='left')

# 10. 脚注
fig.text(0.07, 0.03, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         fontsize=9, color='#D9D9D9', va='bottom', ha='left')

# 11. 精确设置绘图区域
# XML: x=0.081, y=0.277, w=0.865, h=0.547
ax.set_position([0.081, 0.18, 0.865, 0.6])

# 12. 保存
plt.savefig(r'D:\数据可视化\第一章前15\菱形走势图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '菱形走势图.png' 已成功生成！")
