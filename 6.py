import matplotlib.pyplot as plt
import numpy as np

# 1. 数据准备（蝴蝶图/对比条形图，stacked bar横向）
categories = ['华东', '西北', '东北', '华北', '华南']
padding = [2238, 2132, 2027, 1922, 1215]
sales_2022 = [1215, 1321, 1426, 1531, 2238]
gap = [1215, 1215, 1215, 1215, 1215]
sales_2021 = [1003, 1265, 1531, 1436, 2066]

color_2022 = '#0070C0'
color_2021 = '#E74E69'
bg_color = '#1A1E43'
x_max = 6734

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×588 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 588 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制蝴蝶条
y = np.arange(5)
bar_h = 0.4
left_blue = np.array(padding, dtype=float)
left_red = np.array(padding) + np.array(sales_2022) + np.array(gap)

ax.barh(y, sales_2022, height=bar_h, left=left_blue, color=color_2022, edgecolor='none', zorder=2)
ax.barh(y, sales_2021, height=bar_h, left=left_red, color=color_2021, edgecolor='none', zorder=2)

ax.set_xlim(0, x_max)
ax.set_ylim(-0.5, 4.5)

# 5. 数据标签
# 蓝色条内左侧(inBase), 红色条内右侧(inEnd)
# 实测距边缘13px, 1数据单位=0.0979px, 13px≈132.8数据单位
label_offset = 132.8
for i in range(5):
    ax.text(left_blue[i] + label_offset, i, str(sales_2022[i]),
            fontsize=9, color='#F2F2F2', ha='left', va='center', zorder=3)
    ax.text(left_red[i] + sales_2021[i] - label_offset, i, str(sales_2021[i]),
            fontsize=9, color='#F2F2F2', ha='right', va='center', zorder=3)

# 6. 类别标签（中心间隙）
for i, cat in enumerate(categories):
    center_x = padding[i] + sales_2022[i] + gap[i] / 2
    ax.text(center_x, i, cat, fontsize=8, color='#FFFFFF',
            ha='center', va='center', zorder=3)

# 7. 年份标签（第一行上方）
fig.text(307.5 / 832, 1 - 164.5 / 588, '2022', fontsize=9, color='#0070C0',
         ha='center', va='center')
fig.text(516.5 / 832, 1 - 164.5 / 588, '2021', fontsize=9, color='#E74E69',
         ha='center', va='center')

# 8. 标题与副标题
fig.text(55 / 832, 1 - 45 / 588, '2022年上半年各区域对比去年销量',
         fontsize=18, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(55 / 832, 1 - 97 / 588, '2022年整体销量高于2021年，只有东北区域较2021有所下降',
         fontsize=11, color='#FFFFFF', va='top', ha='left')

# 9. 底部注释
fig.text(51 / 832, 1 - 563 / 588, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 10. 隐藏坐标轴
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

# 11. 精确设置绘图区域
plt.subplots_adjust(left=0.0373, right=0.8293,
                    top=0.7154, bottom=0.1180)

# 12. 保存
plt.savefig('蝴蝶图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '蝴蝶图.png' 已成功生成！")
