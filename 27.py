import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 594
fig, ax1 = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax1.set_facecolor(bg_color)

regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales_2022 = [2354, 1902, 3524, 2698, 2896, 2563]
sales_2021 = [2021, 1563, 3213, 2531, 2631, 2361]
yoy = [16, 22, 10, 7, 10, 9]

x = np.arange(len(regions))
bar_w = 0.24
offset = 0.15
color_2022 = '#0070C0'
color_2021 = '#E74E69'
line_color = '#FFC000'

bars1 = ax1.bar(x - offset, sales_2022, width=bar_w, color=color_2022, edgecolor='none', zorder=3)
bars2 = ax1.bar(x + offset, sales_2021, width=bar_w, color=color_2021, edgecolor='none', zorder=3)

ax1.plot([-0.4, len(regions) - 0.6], [0, 0], color='#B0B0B0', linewidth=1.0, zorder=2)

ax1.set_ylim(0, max(sales_2022) * 1.4)
ax1.set_xticks(x)
ax1.set_xticklabels(regions, color='#FFFFFF', fontsize=8)
ax1.tick_params(axis='x', length=0, pad=8)
ax1.tick_params(axis='y', length=0)
ax1.set_yticks([])
for spine in ax1.spines.values():
    spine.set_visible(False)

for i, v in enumerate(sales_2022):
    ax1.text(i - offset, v + max(sales_2022) * 0.02, str(v), ha='center', va='bottom',
             color='#FFFFFF', fontsize=7, zorder=5)
for i, v in enumerate(sales_2021):
    ax1.text(i + offset, v + max(sales_2022) * 0.02, str(v), ha='center', va='bottom',
             color='#FFFFFF', fontsize=7, zorder=5)

ax2 = ax1.twinx()
ax2.plot(x, yoy, color=line_color, linewidth=1.5, marker='o', markersize=4, zorder=4)
ax2.set_ylim(-4.0 * max(yoy), 1.2 * max(yoy))
ax2.set_yticks([])
ax2.tick_params(axis='y', length=0)
for spine in ax2.spines.values():
    spine.set_visible(False)

for i, v in enumerate(yoy):
    ax2.text(i, v + max(yoy) * 0.10, f'{v}%', ha='center', va='bottom',
             color='#FFFFFF', fontsize=7, zorder=5)

legend_elements = [
    Patch(facecolor=color_2022, label='2022'),
    Patch(facecolor=color_2021, label='2021'),
]

fig.text(0.06, 0.95, '上半年各月商品销量同比去年情况', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '2022年相比于2021年销量都有提升，半年整体提升17%',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=9, color='#D9D9D9', va='top', ha='left')

plt.subplots_adjust(left=0.08, right=0.92, top=0.75, bottom=0.15)
plt.savefig(r'D:\数据可视化\第一章后15\簇状柱形折线图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()

from PIL import Image, ImageDraw, ImageFont
img = Image.open(r'D:\数据可视化\第一章后15\簇状柱形折线图.png')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 14)
box_w, box_h = 60, 26
gap = 15
bx = 707 - box_w // 2
by1 = 400
by2 = by1 + box_h + gap
for by, fc, ec, txt in [(by1, color_2022, color_2022, '2022'), (by2, color_2021, color_2021, '2021')]:
    draw.rectangle((bx, by, bx + box_w, by + box_h), fill='#1A1E43')
    draw.line([(bx, by), (bx + box_w, by), (bx + box_w, by + box_h), (bx, by + box_h), (bx, by)], fill=ec, width=2)
    tw = draw.textlength(txt, font=font)
    draw.text((bx + (box_w - tw) / 2, by + 4), txt, fill='#FFFFFF', font=font)
img.save(r'D:\数据可视化\第一章后15\簇状柱形折线图.png')
print("图片 '簇状柱形折线图.png' 已成功生成！")
