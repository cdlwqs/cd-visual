import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# 1. 数据准备
categories = ['口红', '面膜', '隔离', '防晒', '精华']
data_2021 = [3568, 4135, 4436, 4106, 4936]
data_2022 = [2569, 3241, 2965, 3209, 3541]
diff = [999, 894, 1471, 897, 1395]

color_2021 = '#0070C0'
color_2022 = '#82ADD7'
bg_color = '#1A1E43'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×645 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 645 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制分组柱形图
x = np.arange(5)
w1 = 0.225
w2 = 0.225
offset1 = -0.146
offset2 = 0.136

bars1 = ax.bar(x + offset1, data_2021, width=w1, color=color_2021, edgecolor='none', zorder=2)
bars2 = ax.bar(x + offset2, data_2022, width=w2, color=color_2022, edgecolor='none', zorder=2)

# 5. 数据标签
for i in range(5):
    ax.text(x[i] + offset1, data_2021[i] + 308, f'{data_2021[i]}',
            fontsize=7.3, color='#F2F2F2', ha='center', va='center', zorder=3)
    ax.text(x[i] + offset2, data_2022[i] - 393, f'{data_2022[i]}',
            fontsize=7.3, color='#F2F2F2', ha='center', va='center', zorder=3)

# 6. 变化量箭头标记（白色向下三角→白色竖线，位于浅蓝柱正上方）
for i in range(5):
    y1 = data_2021[i]
    y2 = data_2022[i]
    xc = x[i] + offset2  # 浅蓝柱中心
    xd = x[i] + offset1  # 深蓝柱中心

    # 深蓝色细线（从深蓝柱中心引出到浅蓝柱中心，位于深蓝柱顶）
    ax.plot([xd, xc], [y1, y1], color=color_2021, linewidth=0.5, zorder=4)

    # 白色向下三角（顶部2px宽，底部10px宽，高10px）
    tri_top_y = y1 - 34       # 三角顶部（深蓝柱顶下方2px）
    tri_bot_y = y1 - 205      # 三角底部（顶部下方10px）
    tri_top_hw = 0.004        # 顶部半宽~0.5px（渲染后2px）
    tri_bot_hw = 0.040        # 底部半宽~5.7px（渲染后10px）
    triangle = Polygon([
        (xc - tri_top_hw, tri_top_y),
        (xc + tri_top_hw, tri_top_y),
        (xc + tri_bot_hw, tri_bot_y),
        (xc - tri_bot_hw, tri_bot_y),
    ], closed=True, facecolor='#F2F2F2', edgecolor='none', zorder=4)
    ax.add_patch(triangle)

    # 白色竖线（从三角底部到浅蓝柱顶，2px宽）
    ax.plot([xc, xc], [tri_bot_y, y2], color='#F2F2F2', linewidth=1.0, zorder=4)

    # 变化量数值标签（竖线右侧，竖线中点下方5px）
    ax.text(xc + 0.14, (tri_bot_y + y2) / 2 - 102, f'{diff[i]}',
            fontsize=7.1, color='#FFFFFF', ha='center', va='center',
            zorder=5)

# 7. 类别轴标签
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8.25, color='#F2F2F2')
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(0, 6000)

# 8. 隐藏y轴，保留底部灰色细线
ax.set_yticks([])
ax.tick_params(length=0)
for spine_name, spine in ax.spines.items():
    if spine_name == 'bottom':
        spine.set_visible(True)
        spine.set_color('#717389')
        spine.set_linewidth(0.5)
    else:
        spine.set_visible(False)

# 9. 图例（色块在左，文字在右）
legend_y = 0.7085
fig.text(0.0902, legend_y, '2021销量', fontsize=9, color='#FFFFFF', va='center', ha='left')
fig.patches.append(plt.Rectangle((0.0769, legend_y - 0.0077), 0.0108, 0.0155,
                                  facecolor=color_2021, edgecolor='none', transform=fig.transFigure))
fig.text(0.2176, legend_y, '2022销量', fontsize=9, color='#FFFFFF', va='center', ha='left')
fig.patches.append(plt.Rectangle((0.2043, legend_y - 0.0077), 0.0108, 0.0155,
                                  facecolor=color_2022, edgecolor='none', transform=fig.transFigure))

# 10. 标题与副标题
fig.text(0.041, 1 - 0.043, '2022年商品对比去年销售情况',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.041, 1 - 0.12, '商品整体比去年销量有所下降，其中隔离下降最多，下降33%',
         fontsize=12, color='#FFFFFF', va='top', ha='left')

# 11. 底部注释
fig.text(0.028, 1 - 0.95, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
         fontsize=8, color='#D9D9D9', va='top', ha='left')

# 12. 精确设置绘图区域
ax.set_position([0.0637, 0.1638, 0.8554, 0.5448])

# 13. 保存
plt.savefig('对比柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '对比柱形图.png' 已成功生成！")
