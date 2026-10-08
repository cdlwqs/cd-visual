import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Ellipse

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 844, 593
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

regions = ['华南', '华北', '东北', '西北', '华东']
completion = [0.86, 0.74, 0.62, 0.51, 0.35]
blue_ends = [0.870, 0.751, 0.635, 0.528, 0.373]
bar_color = '#0070C0'
gray_color = '#717389'

y = np.arange(len(regions))
bar_h = 0.397

ax.set_xlim(0, 1)
ax.set_ylim(-0.2, 4.2)
ax.invert_yaxis()

plt.subplots_adjust(left=0.145, right=0.724, top=0.708, bottom=0.170)

ry = bar_h / 2
rx = 0.0295

for i in range(len(regions)):
    ax.add_patch(Rectangle((rx, y[i] - ry), 1.0 - 2 * rx, bar_h, facecolor=gray_color, edgecolor='none', zorder=2))
    ax.add_patch(Ellipse((rx, y[i]), 2 * rx, 2 * ry, facecolor=gray_color, edgecolor='none', zorder=2))
    ax.add_patch(Ellipse((1.0 - rx, y[i]), 2 * rx, 2 * ry, facecolor=gray_color, edgecolor='none', zorder=2))

for i in range(len(regions)):
    c = blue_ends[i]
    ax.add_patch(Rectangle((rx, y[i] - ry), c - rx, bar_h, facecolor=bar_color, edgecolor='none', zorder=3))
    ax.add_patch(Ellipse((rx, y[i]), 2 * rx, 2 * ry, facecolor=bar_color, edgecolor='none', zorder=3))

ax.scatter(blue_ends, y, s=200, facecolor=bar_color, edgecolor='white', linewidth=1.0, zorder=4)

for i in range(len(regions)):
    ax.text(blue_ends[i] - 0.05, y[i], f'{int(completion[i] * 100)}%', ha='right', va='center',
            color='#FFFFFF', fontsize=8, zorder=5)

ax.set_yticks(y)
ax.set_yticklabels(regions, color='#FFFFFF', fontsize=9)
ax.tick_params(axis='y', length=0, pad=4)
ax.tick_params(axis='x', length=0)
ax.set_xticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.06, 0.95, '2022年上半年产品销量目标达成率情况', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '华南完成率最高达到86%，华东最低35%',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=9, color='#D9D9D9', va='top', ha='left')

plt.savefig(r'D:\数据可视化\第一章后15\滑珠图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '滑珠图.png' 已成功生成！")
