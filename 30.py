import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Ellipse

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 831, 593
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

regions = ['华南', '华北', '东北', '西北', '华东']
c2022 = [0.86, 0.74, 0.62, 0.51, 0.35]
c2021 = [0.92, 0.69, 0.53, 0.39, 0.45]
blue_ends = [0.8827, 0.7721, 0.6633, 0.5629, 0.4167]
gray_ends = [0.9269, 0.7156, 0.5697, 0.4422, 0.4966]

bar_color = '#0070C0'
gray_color = '#717389'
gray_ball_color = '#A6A6A6'

y = np.arange(len(regions))
bar_h = 0.162
blue_start = 0.0884

ax.set_xlim(0, 1)
ax.set_ylim(-0.2, 4.2)
ax.invert_yaxis()

plt.subplots_adjust(left=0.0866, right=0.7942, top=0.6927, bottom=0.1437)

ry = bar_h / 2
rx = 0.0102

for i in range(len(regions)):
    ax.add_patch(Rectangle((blue_start, y[i] - ry), 1.0 - blue_start, bar_h, facecolor=gray_color, edgecolor='none', zorder=2))

for i in range(len(regions)):
    c = blue_ends[i]
    ax.add_patch(Rectangle((blue_start, y[i] - ry), c - blue_start, bar_h, facecolor=bar_color, edgecolor='none', zorder=3))

ax.scatter(blue_ends, y, s=80, facecolor=bar_color, edgecolor='white', linewidth=1.0, zorder=4)
ax.scatter(gray_ends, y, s=80, facecolor=gray_ball_color, edgecolor='white', linewidth=1.0, zorder=4)

for i in range(len(regions)):
    ax.text(blue_ends[i], y[i] - 0.25, f'{int(c2022[i] * 100)}%', ha='center', va='center', color='#FFFFFF', fontsize=6, zorder=5)

for i in range(len(regions)):
    ax.text(0.002, y[i], regions[i], ha='left', va='center', color='#FFFFFF', fontsize=8, zorder=5)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.0686, 0.9275, '2022年上半年销量目标达成率同比去年情况', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.0710, 0.8533, '华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.0806, 0.0674, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=8, color='#D9D9D9', va='top', ha='left')

ax_legend = fig.add_axes([0, 0, 1, 1], facecolor='none')
ax_legend.set_xlim(0, 1)
ax_legend.set_ylim(0, 1)
ax_legend.axis('off')
ax_legend.scatter([0.0915], [0.7383], s=80, facecolor=bar_color, edgecolor='white', linewidth=1.0, zorder=5)
ax_legend.scatter([0.2479], [0.7383], s=80, facecolor=gray_ball_color, edgecolor='white', linewidth=1.0, zorder=5)
fig.text(0.1191, 0.7383, '2022完成率', color='#FFFFFF', fontsize=7, va='center', ha='left')
fig.text(0.2684, 0.7383, '2021完率', color='#FFFFFF', fontsize=7, va='center', ha='left')

plt.savefig(r'D:\数据可视化\第一章后15\对比滑珠图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '对比滑珠图.png' 已成功生成！")
