import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 594
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

products = ['口 红', '面 膜', '隔 离', '防 晒', '精 华', '面 霜']
actual = [653, 523, 648, 856, 714, 785]
target = [700, 500, 600, 900, 600, 600]

x = np.arange(len(products))
bar_color = '#0070C0'
frame_color = '#B0B0B0'

bars = ax.bar(x, actual, width=0.168, color=bar_color, edgecolor='none', zorder=5)

for i, t in enumerate(target):
    ax.add_patch(Rectangle((i - 0.12, 0), 0.24, t, fill=False,
                           edgecolor=frame_color, linewidth=1.0, zorder=4))

ax.plot([-0.3, len(products) - 0.7], [0, 0], color='#0050A0', linewidth=1.0, zorder=2)

ax.set_ylim(0, max(target) * 1.1)
ax.set_xticks(x)
ax.set_xticklabels(products, color='#FFFFFF', fontsize=7)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0)
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

for i, v in enumerate(actual):
    ax.text(i, max(v, target[i]) + max(target) * 0.02, str(v), ha='center', va='bottom',
            color='#FFFFFF', fontsize=8, zorder=5)

legend_elements = [
    Patch(facecolor='none', edgecolor=frame_color, linewidth=1.0, label='目标销量'),
    Patch(facecolor=bar_color, label='实际销量'),
]
ax.legend(handles=legend_elements, frameon=False, labelcolor='#FFFFFF',
          fontsize=7, ncol=2, bbox_to_anchor=(0, 1.08), loc='upper left',
          handlelength=1.0, handleheight=1.0)

fig.text(0.06, 0.95, '2022年上半年各商品销量完成情况', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=9, color='#D9D9D9', va='top', ha='left')

plt.subplots_adjust(left=0.08, right=0.92, top=0.72, bottom=0.18)
plt.savefig(r'D:\数据可视化\第一章后15\目标柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '目标柱形图.png' 已成功生成！")
