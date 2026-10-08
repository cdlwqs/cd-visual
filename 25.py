import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

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
pass_val = 600
good_val = 800
excel_val = 1000

x = np.arange(len(products))
pass_color = '#82ADD7'
good_color = '#00B0F0'
excel_color = '#0070C0'
actual_color = '#0E5DFF'
target_color = '#FFC000'

ax.bar(x, pass_val, width=0.3, color=pass_color, zorder=2)
ax.bar(x, good_val - pass_val, bottom=pass_val, width=0.3, color=good_color, zorder=2)
ax.bar(x, excel_val - good_val, bottom=good_val, width=0.3, color=excel_color, zorder=2)

ax.plot([-0.4, len(products) - 0.6], [0, 0], color='#B0B0B0', linewidth=1.0, zorder=3)

ax.bar(x, actual, width=0.18, color=actual_color, edgecolor='none', zorder=4)

for i, t in enumerate(target):
    ax.plot([i - 0.075, i + 0.075], [t, t], color=target_color, linewidth=3, zorder=5)

ax.set_ylim(0, 1200)
ax.set_xticks(x)
ax.set_xticklabels(products, color='#FFFFFF', fontsize=7)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0, pad=1.5)
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.set_yticklabels(['0', '200', '400', '600', '800', '1000', '1200'], color='#FFFFFF', fontsize=7)
for spine in ax.spines.values():
    spine.set_visible(False)

legend_elements = [
    Patch(facecolor=pass_color, label='及格'),
    Patch(facecolor=good_color, label='良好'),
    Patch(facecolor=excel_color, label='优秀'),
    Patch(facecolor=actual_color, label='实际'),
    Line2D([0], [0], color=target_color, linewidth=3, label='目标'),
]
ax.legend(handles=legend_elements, frameon=False, labelcolor='#FFFFFF',
          fontsize=7, ncol=5, bbox_to_anchor=(0.06, 1.05), loc='upper left',
          handlelength=1.0, handleheight=1.0)

fig.text(0.06, 0.95, '2022年上半年各商品销量完成情况', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=9, color='#D9D9D9', va='top', ha='left')

plt.subplots_adjust(left=0.10, right=0.94, top=0.72, bottom=0.18)
plt.savefig(r'D:\数据可视化\第一章后15\子弹图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '子弹图.png' 已成功生成！")
