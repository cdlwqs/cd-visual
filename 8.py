import matplotlib.pyplot as plt
import numpy as np

# 1. 数据准备（XML顺序：y=0华北在最下，y=5华东在最上）
categories = ['华北', '华南', '东北', '西北', '西南', '华东']
sales =       [4321,   1946,   1536,   1872,   1369,   2109]
placeholder1 = [0,    2375,   2785,   2449,   2952,   2212]
placeholder2 = [1080.25] * 6
percentages = ['-13.6%', '-20.8%', '-9.3%', '-15.9%', '-17.9%', '-5.8%']

color_sales = '#09387E'
color_ph1 = '#82ADD7'
color_ph2 = '#9B3D4F'
bg_color = '#1A1E43'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×588 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 588 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制堆积水平条形图（y=0在最下=华北，y=5在最上=华东）
y = np.arange(6)

ax.barh(y, sales, height=0.767, color=color_sales, edgecolor='none', zorder=2)
ax.barh(y, placeholder1, height=0.767, left=sales, color=color_ph1, edgecolor='none', zorder=2)
left_ph2 = [s + p for s, p in zip(sales, placeholder1)]
ax.barh(y, placeholder2, height=0.767, left=left_ph2, color=color_ph2, edgecolor='none', zorder=2)

# 5. 数值标签（销量系列，inEnd位置，10pt，白色偏暗）
label_color = '#F2F2F2'
for i in range(6):
    ax.text(sales[i] - 80, i, f'{sales[i]}',
            fontsize=10, color=label_color, ha='right', va='center', zorder=3)

# 6. 百分比标签（占位2系列，居中，10pt）
for i in range(6):
    cx = left_ph2[i] + placeholder2[i] / 2
    ax.text(cx, i, percentages[i],
            fontsize=10, color='#FFFFFF', ha='center', va='center', zorder=3)

# 7. 类别标签（y轴，9pt，水平）
ax.set_yticks(y)
ax.set_yticklabels(categories, fontsize=9, color='#FFFFFF')

# 8. 坐标轴
ax.set_xlim(0, 5401.25)
ax.set_xticks([])
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

# 9. 标题与副标题
fig.text(0.047, 1 - 0.052, '2021年各区域销量及同比情况',
         fontsize=18, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.047, 1 - 0.129, '各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%',
         fontsize=11, color='#FFFFFF', va='top', ha='left')

# 10. 底部注释
fig.text(0.036, 1 - 0.93, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
         fontsize=8, color='#D9D9D9', va='top', ha='left')

# 11. 精确设置绘图区域
plt.subplots_adjust(left=0.127, right=0.861,
                    top=0.720, bottom=0.109)

# 12. 保存
plt.savefig('数值百分比.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '数值百分比.png' 已成功生成！")
