import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import numpy as np2

# 1. 数据准备（蝴蝶图/对比条形图，百分比，从大到小排列）
categories = ['华南', '华北', '东北', '西北', '华东']
data_2022 = [9, 13, 18, 31, 36]
data_2021 = [5, 12, 19, 26, 42]

color_2022 = '#0070C0'
color_2021 = '#E74E69'
bg_color = '#1A1E43'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×456 @ 144dpi（按原图716:392比例）
fig, ax = plt.subplots(figsize=(832 / 144, 456 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制蝴蝶条（从大到小：华东在上，华南在下）
y = np.arange(5)
bar_h = 0.45
center = 50
gap = 19  # 蓝红条之间的间隙

# 反转顺序：y=4对应华东（最上），y=0对应华南（最下）
left_blue = [center - gap/2 - d for d in data_2022]

ax.barh(y, data_2022, height=bar_h, left=left_blue, color=color_2022,
        edgecolor='none', zorder=2)
ax.barh(y, data_2021, height=bar_h, left=center + gap/2, color=color_2021,
        edgecolor='none', zorder=2)

ax.set_xlim(-2, 104)
ax.set_ylim(-0.5, 4.5)

# 5. 百分比数据标签（固定x坐标，垂直对齐）
label_left_x = center - gap/2 - max(data_2022) - 1.2
label_right_x = center + gap/2 + max(data_2021) + 1.0
for i in range(5):
    ax.text(label_left_x, i, f'{data_2022[i]}%',
            fontsize=7, color='#FFFFFF', ha='right', va='center', zorder=3)
    ax.text(label_right_x, i, f'{data_2021[i]}%',
            fontsize=7, color='#FFFFFF', ha='left', va='center', zorder=3)

# 6. 区域名标签（中心轴间隙中）
for i, cat in enumerate(categories):
    ax.text(center, i, cat, fontsize=7, color='#FFFFFF',
            ha='center', va='center', zorder=3)

# 7. 标题与副标题
fig.text(55 / 832, 1 - 30 / 456, '2022年第一季度销售目标完成情况',
         fontsize=14, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(55 / 832, 1 - 67 / 456, '华东区域完成率最高达到36%，但是相比去年的42%有所下降',
         fontsize=10, color='#FFFFFF', va='top', ha='left')

# 8. 底部注释
fig.text(51 / 832, 1 - 437 / 456, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 9. 隐藏坐标轴
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

# 10. 精确设置绘图区域（1%≈5.5px）
plt.subplots_adjust(left=0.146, right=0.847,
                    top=0.639, bottom=0.228)

# 11. 保存
plt.savefig('蝴蝶图2.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()

# 12. PIL后处理：添加垂直条纹图案（每3像素深浅交替）
img = Image.open('蝴蝶图2.png').convert('RGB')
arr = np2.array(img)
h, w = arr.shape[:2]

blue_light = (0, 112, 192)
blue_dark = (0, 87, 153)
red_light = (231, 78, 105)
red_dark = (169, 78, 105)

for y_pix in range(h):
    for x_pix in range(w):
        r, g, b = int(arr[y_pix, x_pix, 0]), int(arr[y_pix, x_pix, 1]), int(arr[y_pix, x_pix, 2])
        is_blue = abs(r - 0) < 25 and abs(g - 112) < 25 and abs(b - 192) < 25
        is_red = abs(r - 231) < 25 and abs(g - 78) < 25 and abs(b - 105) < 25
        if is_blue:
            if x_pix % 3 == 1:
                arr[y_pix, x_pix] = blue_dark
            else:
                arr[y_pix, x_pix] = blue_light
        elif is_red:
            if x_pix % 3 == 2:
                arr[y_pix, x_pix] = red_dark
            else:
                arr[y_pix, x_pix] = red_light

Image.fromarray(arr).save('蝴蝶图2.png')
print("图片 '蝴蝶图2.png' 已成功生成！")
