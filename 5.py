import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# 1. 数据准备（来自 Excel "5 层叠柱形图" 工作表，实际为分组柱形图 clustered）
categories = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
sales = [3121, 4086, 4321, 4601, 4936, 4231]      # 销售额
profit = [1020, 1421, 1502, 1623, 1781, 1432]      # 利润额
color_sales = '#0070C0'    # 蓝色
color_profit = '#E74E69'   # 红色

# 2. 设置中文字体（微软雅黑）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 创建画布（832×588 @ 144dpi）
fig, ax = plt.subplots(figsize=(832 / 144, 588 / 144))
fig.patch.set_facecolor('#1A1E43')
ax.set_facecolor('#1A1E43')

# 4. 分组柱形图参数（gapWidth=219, overlap=30, 柱宽29px）
# 绘图区宽=0.8088*832=672.9px, 每组占112.15px, 柱宽29px
x = np.arange(len(categories))
bar_width = 29 / 112.15       # 0.259 数据单位
offset = 10 / 112.15          # 组内中心距20px, 半距10px

# 5. 绘制柱子
bars1 = ax.bar(x - offset, sales, width=bar_width, color=color_sales, zorder=2)
bars2 = ax.bar(x + offset, profit, width=bar_width, color=color_profit, zorder=2)
ax.set_xlim(-0.5, len(categories) - 0.5)
ax.set_ylim(0, 6000)

# 6. 数据标签（柱顶外 outEnd, 7pt, #F2F2F2）
# 原图实测：标签高11px, 生成图9pt=14px, 修正=9×11/14≈7pt
# 标签中心距柱顶20px, 1px=17.57数据单位
label_dy = 20 * 17.57  # ~351 数据单位
for bar, val in zip(bars1, sales):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + label_dy,
            str(val), fontsize=7, color='#F2F2F2', ha='center', va='center', zorder=6)
for bar, val in zip(bars2, profit):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + label_dy,
            str(val), fontsize=7, color='#F2F2F2', ha='center', va='center', zorder=6)

# 7. 标题与副标题（精确位置：原图标题顶y=51x=49, 副标题顶y=114x=49）
fig.text(49 / 832, 1 - 51 / 588, '2021年至今季度销售额(万)和利润额(万)',
         fontsize=20, fontweight='bold', color='white', va='top', ha='left')
fig.text(49 / 832, 1 - 97 / 588, '2022年第二季度销售额首次出现下降，降幅达到15%',
         fontsize=12, color='white', va='top', ha='left')

# 8. 底部注释（原图注释底y=564 x=40）
fig.text(40 / 832, 1 - 564 / 588, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 9. 图例文字（由PIL后处理绘制）

# 10. X 轴设置（9pt, 无刻度线）
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8, color='#F2F2F2')
ax.tick_params(axis='x', length=0, pad=5)

# 11. Y 轴设置（无刻度标签, 无网格线）
ax.set_yticks([])
ax.tick_params(axis='y', length=0)

# 12. 边框：显示底部横线（原图柱底有横线 #454866），隐藏其余
for spine_name, spine in ax.spines.items():
    if spine_name == 'bottom':
        spine.set_visible(True)
        spine.set_color('#454866')
        spine.set_linewidth(1)
    else:
        spine.set_visible(False)

# 13. 精确设置绘图区域位置（manualLayout: x=0.0882, y=0.2643, w=0.8088, h=0.5806）
plt.subplots_adjust(left=0.0882, right=0.0882 + 0.8088,
                    top=1 - 0.2643, bottom=1 - 0.2643 - 0.5806)

# 14. 保存图片
plt.savefig('层叠柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()

# 15. PIL后处理：绘制图例方框和文字
from PIL import Image, ImageDraw, ImageFont
img = Image.open('层叠柱形图.png').convert('RGB')
draw = ImageDraw.Draw(img)
bg_color = (26, 30, 67)
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 16)
text_color = (242, 242, 242)
# 蓝色方框 x[670-746] y[302-328]
draw.rectangle([670, 302, 746, 328], fill=bg_color)
draw.line([(670, 302), (746, 302)], fill=(0, 112, 192), width=1)
draw.line([(670, 328), (746, 328)], fill=(0, 112, 192), width=1)
draw.line([(670, 302), (670, 328)], fill=(0, 112, 192), width=1)
draw.line([(746, 302), (746, 328)], fill=(0, 112, 192), width=1)
draw.text((684, 307), '销售额', font=font, fill=text_color)
# 红色方框 x[670-745] y[346-372]
draw.rectangle([670, 346, 745, 372], fill=bg_color)
draw.line([(670, 346), (745, 346)], fill=(231, 78, 105), width=1)
draw.line([(670, 372), (745, 372)], fill=(231, 78, 105), width=1)
draw.line([(670, 346), (670, 372)], fill=(231, 78, 105), width=1)
draw.line([(745, 346), (745, 372)], fill=(231, 78, 105), width=1)
draw.text((683, 351), '利润额', font=font, fill=text_color)
img.save('层叠柱形图.png')
print("图片 '层叠柱形图.png' 已成功生成！")
