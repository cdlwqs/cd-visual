import matplotlib.pyplot as plt
import numpy as np

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 594
fig, ax1 = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax1.set_facecolor(bg_color)

years = ['2017', '2018', '2019', '2020', '2021', '2022']
sales = [1603, 2106, 2406, 3265, 3721, 3921]
growth = [27, 31, 14, 36, 14, 5]

x = np.arange(len(years))
bar_color = '#0070C0'
line_color = '#E74E5C'

# 柱形图 (销售量)
bars = ax1.bar(x, sales, width=0.29, color=bar_color, zorder=2)
ax1.set_ylim(0, max(sales) * 1.6)
ax1.set_xticks(x)
ax1.set_xticklabels(years, color='#FFFFFF', fontsize=8)
ax1.tick_params(axis='x', length=0, pad=8)
ax1.tick_params(axis='y', length=0)
ax1.set_yticks([])
for spine in ax1.spines.values():
    spine.set_visible(False)

# 柱形数值标签 (白色, 柱顶上方)
for i, v in enumerate(sales):
    ax1.text(i, v + max(sales) * 0.04, str(v), ha='center', va='bottom',
             color='#FFFFFF', fontsize=8, zorder=6)

# 折线图 (同比, 双Y轴)
ax2 = ax1.twinx()
ax2.plot(x, growth, color=line_color, linewidth=1.5, marker='o', markersize=4, zorder=4)
ax2.set_ylim(-3.8 * max(growth), 1.2 * max(growth))
ax2.set_yticks([])
ax2.tick_params(axis='y', length=0)
for spine in ax2.spines.values():
    spine.set_visible(False)

# 折线数值标签 (白色, 点上方)
for i, v in enumerate(growth):
    ax2.text(i, v + max(growth) * 0.15, f'{v}%', ha='center', va='bottom',
             color='#FFFFFF', fontsize=8, zorder=5)

# 图例 (右上角)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor=bar_color, label='销售量'),
    Line2D([0], [0], color=line_color, marker='o', markersize=4, label='同比'),
]
leg = ax1.legend(handles=legend_elements, frameon=False, labelcolor='#FFFFFF',
                 fontsize=8, ncol=2, bbox_to_anchor=(1, 1.15))

# 标题/副标题/注释
fig.text(0.06, 0.95, '近六年销售量及增长率', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '平台销量近6年持续增长，但近两年增长率有所放缓',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统', fontsize=9, color='#D9D9D9', va='top', ha='left')

plt.subplots_adjust(left=0.08, right=0.92, top=0.72, bottom=0.15)
plt.savefig(r'D:\数据可视化\第一章后15\柱形折线图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '柱形折线图.png' 已成功生成！")
