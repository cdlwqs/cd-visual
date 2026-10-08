import matplotlib.pyplot as plt
import numpy as np

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 594
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
yoy = [12, 25, 16, 21, 18, 25]

x = np.arange(len(regions))
bar_color = '#E74E69'
circle_color = '#0070C0'

ax.bar(x, sales, width=0.35, color=bar_color, edgecolor='none', zorder=3)

ax.plot([-0.4, len(regions) - 0.6], [0, 0], color='#B0B0B0', linewidth=1.0, zorder=2)

circle_y = [max(sales) + max(sales) * 0.32] * len(regions)
circle_s = [500 * (y / 25) ** 1.5 for y in yoy]
ax.scatter(x, circle_y, s=circle_s, color=circle_color, zorder=4)

for i in range(len(regions)):
    ax.text(i, sales[i] + max(sales) * 0.04, str(sales[i]), ha='center', va='bottom',
            color='#FFFFFF', fontsize=8, zorder=5)
    ax.text(i, circle_y[i], f'{yoy[i]}%', ha='center', va='center',
            color='#FFFFFF', fontsize=8, zorder=5)

ax.set_ylim(0, max(sales) * 1.45)
ax.set_xticks(x)
ax.set_xticklabels(regions, color='#FFFFFF', fontsize=8)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0)
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.06, 0.95, '各区域上半年销量以同比', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '东北区域销量持续保持第一，华东和华南同比去年增长最多',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=9, color='#D9D9D9', va='top', ha='left')

plt.subplots_adjust(left=0.08, right=0.92, top=0.75, bottom=0.15)
plt.savefig(r'D:\数据可视化\第一章后15\柱形圆.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '柱形圆.png' 已成功生成！")
