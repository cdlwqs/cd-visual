import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

# 1. 数据准备（来自 Excel "3 渐变圆角柱形图" 工作表）
categories = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
values = [653, 523, 648, 856, 714, 785]

# 2. 设置中文字体（与 Excel 文档一致：微软雅黑）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 创建画布，尺寸与 Excel 原图一致（864×617 @ 144dpi）
fig, ax = plt.subplots(figsize=(864 / 144, 617 / 144))
fig.patch.set_facecolor('#1A1E43')
ax.set_facecolor('#1A1E43')

# 4. 渐变色 stops（与 Excel blipFill 图片像素采样一致）
gradient_stops = [
    (0.00, (0, 243, 254)),    # #00F3FE
    (0.25, (0, 228, 243)),    # #00E4F3
    (0.50, (0, 184, 215)),    # #00B8D7
    (0.75, (0, 120, 182)),    # #0078B6
    (1.00, (0, 78, 167)),     # #004EA7
]

def make_gradient_rgba(bar_height_px, bar_width_px=18, radius_px=4, supersample=3):
    w = bar_width_px * supersample
    h = max(bar_height_px, 1) * supersample
    r = radius_px * supersample
    rgba = np.ones((h, w, 4), dtype=np.float32)
    for y in range(h):
        frac = y / (h - 1) if h > 1 else 0
        for j in range(len(gradient_stops) - 1):
            f1, c1 = gradient_stops[j]
            f2, c2 = gradient_stops[j + 1]
            if f1 <= frac <= f2:
                t = (frac - f1) / (f2 - f1)
                rgba[y, :, 0] = (c1[0] + t * (c2[0] - c1[0])) / 255
                rgba[y, :, 1] = (c1[1] + t * (c2[1] - c1[1])) / 255
                rgba[y, :, 2] = (c1[2] + t * (c2[2] - c1[2])) / 255
                break
    for x in range(w):
        for y in range(r):
            if x < r:
                dx = r - x
                dy = r - y
                dist = np.sqrt(dx * dx + dy * dy)
                if dist > r:
                    rgba[y, x, 3] = 0.0
                elif dist > r - supersample:
                    rgba[y, x, 3] = max(0.0, (r - dist) / supersample)
            elif x > w - r - 1:
                dx = x - (w - r - 1)
                dy = r - y
                dist = np.sqrt(dx * dx + dy * dy)
                if dist > r:
                    rgba[y, x, 3] = 0.0
                elif dist > r - supersample:
                    rgba[y, x, 3] = max(0.0, (r - dist) / supersample)
    return rgba

# 5. 绘制柱形图参数
x = np.arange(len(categories))
bar_width = 0.167

# 6. 为每个柱子绘制渐变填充 + 圆角顶部
plot_height_px = 331
y_max = 1200
for i, val in enumerate(values):
    bar_x = i - bar_width / 2
    bar_h_px = int(round(val / y_max * plot_height_px))
    gradient_rgba = make_gradient_rgba(bar_h_px, bar_width_px=18, radius_px=4)
    ax.imshow(gradient_rgba, aspect='auto',
              extent=[bar_x, bar_x + bar_width, 0, val],
              zorder=2, interpolation='bilinear')

# 7. 数据标签圆角矩形 + 蓝色圆点 + 连接线 + 数值文本（来自 drawing6.xml userShapes）
label_boxes = [
    (0.18076, 0.45536, 0.254, 0.50604),
    (0.31587, 0.52416, 0.38911, 0.57484),
    (0.44638, 0.46765, 0.51962, 0.51833),
    (0.58150, 0.37920, 0.65473, 0.42987),
    (0.71444, 0.44195, 0.78768, 0.49263),
    (0.84161, 0.41237, 0.91485, 0.46304),
]
connectors = [
    (0.19945, 0.48280, 0.53808),
    (0.33058, 0.55733, 0.61261),
    (0.46293, 0.49713, 0.54177),
    (0.59589, 0.40704, 0.45168),
    (0.73009, 0.46847, 0.51310),
    (0.85968, 0.43898, 0.48362),
]

for i, val in enumerate(values):
    x1, y1, x2, y2 = label_boxes[i]
    fig_x = x1
    fig_y = 1 - y2
    fig_w = x2 - x1
    fig_h = y2 - y1

    # 圆角矩形（#0070C0 20% 透明度）
    box = FancyBboxPatch(
        (fig_x + 0.004, fig_y + 0.004), fig_w - 0.008, fig_h - 0.008,
        boxstyle="round,pad=0.004,rounding_size=0.01",
        transform=fig.transFigure, facecolor='#0070C0', alpha=0.2,
        edgecolor='none', zorder=5
    )
    fig.patches.append(box)

    # 蓝色圆点（在数值左侧，#5B9BD5，半径约6px）
    dot_cx = fig_x + 0.016  # 距框左边约14px
    dot_cy = fig_y + fig_h / 2  # 垂直居中
    dot_radius = 0.007  # 约6px
    dot = Circle((dot_cx, dot_cy), dot_radius,
                 transform=fig.transFigure, facecolor='#5B9BD5',
                 edgecolor='none', zorder=6)
    fig.patches.append(dot)

    # 数值文本（#F2F2F2 9pt，在圆点右侧）
    text_cx = fig_x + fig_w / 2 + 0.01  # 略偏右，为圆点让出空间
    fig.text(text_cx, fig_y + fig_h / 2, str(val),
             fontsize=9, color='#F2F2F2', ha='center', va='center', zorder=6)

    # 连接线（从标签框底部到柱子顶部）
    cx_conn, y_top, y_bot = connectors[i]
    line = Line2D([cx_conn, cx_conn], [1 - y_bot, 1 - y_top],
                  color='#5B9BD5', linewidth=0.8, zorder=4,
                  transform=fig.transFigure)
    fig.add_artist(line)

# 8. 标题与副标题（来自 drawing6.xml 文本框 11）
fig.text(0.05, 0.95, '3月商品销量对比', fontsize=20, fontweight='bold',
         color='white', va='top', ha='left')
fig.text(0.05, 0.856, '防晒销量最多，3月销量856；面膜最少，3月销量523',
         fontsize=14, color='white', va='top', ha='left')

# 9. 底部注释（来自 drawing6.xml 文本框 12）
fig.text(0.04, 0.03, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 10. X 轴设置（标签 9pt #F2F2F2，无刻度线）
ax.set_xlim(-0.5, len(categories) - 0.5)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9, color='#F2F2F2')
ax.tick_params(axis='x', length=0, pad=5)

# 11. Y 轴设置（0-1200，间隔 200，标签 9pt #F2F2F2，有网格线）
ax.set_ylim(0, 1200)
ax.set_yticks(np.arange(0, 1201, 200))
ax.set_yticklabels(np.arange(0, 1201, 200), fontsize=9, color='#F2F2F2')
ax.tick_params(axis='y', length=0)

# 12. 网格线（长虚线，浅色，与 Excel majorGridlines 一致）
ax.yaxis.grid(True, linestyle=(0, (8, 4)), color='#FFFFFF', alpha=0.12)
ax.set_axisbelow(True)

# 13. 隐藏所有边框
for spine in ax.spines.values():
    spine.set_visible(False)

# 14. 精确设置绘图区域位置（与 Excel XML manualLayout 一致）
plt.subplots_adjust(left=0.135, right=0.135 + 0.789, top=1 - 0.292, bottom=1 - 0.292 - 0.536)

# 15. 保存图片（dpi=144 与 Excel 导出尺寸一致：864×617）
plt.savefig('渐变圆角柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
print("图片 '渐变圆角柱形图.png' 已成功生成！")
