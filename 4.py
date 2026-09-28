import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle

# 1. 数据准备（来自 Excel "4 标注柱形图" 工作表）
categories = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
values = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
bar_colors = [
    '#7BBDD5',  # 口红 - 默认色
    '#49A098',  # 面膜
    '#E66B4C',  # 隔离
    '#FFC000',  # 防晒
    '#0097E0',  # 精华
    '#0070C0',  # 面霜
    '#4A5BD1',  # 眼影
    '#464CAC',  # 气垫
]

# 2. 设置中文字体（与 Excel 文档一致：微软雅黑）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 创建画布，尺寸与 Excel 原图一致（832×616 @ 144dpi）
fig, ax = plt.subplots(figsize=(832 / 144, 616 / 144))
fig.patch.set_facecolor('#1A1E43')
ax.set_facecolor('#1A1E43')

# 4. 绘制柱形图参数
x = np.arange(len(categories))
bar_width = 0.489  # 40px / (654px / 8) ≈ 0.489，与 Excel gapWidth=100 一致

# 5. 绘制柱子（每个柱子不同颜色，来自 chart4.xml dPt spPr）
bars = ax.bar(x, values, width=bar_width, color=bar_colors, zorder=2)
ax.set_xlim(-0.5, len(categories) - 0.5)

# 6. 数据标签（矩形标注框 + 斜三角箭头，与柱子同色，白色数值位于柱子上方）
# 原图实测：标注框 45px×26px，箭头从框底1/4或3/4处斜向指向柱子顶部
# 箭头宽端9px，高度5-10px不等，每个柱子箭头倾斜方向不同
# 像素→数据单位换算：X轴 1px=1/81.76, Y轴 1px=1/0.03314=30.18
px_to_dx = 1 / 81.76
px_to_dy = 1 / 0.03314
box_w = 45 * px_to_dx       # 标注框宽
box_h = 26 * px_to_dy       # 标注框高
arrow_half_w = 4.5 * px_to_dx  # 箭头宽端半宽(9px/2)
# 每个柱子箭头参数(像素): (框中心相对柱中心偏移, 箭头底中心相对框中心偏移, 箭头尖相对柱中心偏移, 箭头高)
# 箭头高+2补偿matplotlib抗锯齿导致尖端像素丢失
arrow_params = [
    (3, -9, -3, 11),   # 口红 - 右斜
    (1,  9,  5, 11),   # 面膜 - 左斜
    (0, -9, -3, 12),   # 隔离 - 右斜
    (2,  9,  6, 7),    # 防晒 - 左斜
    (2, -8, -1, 8),    # 精华 - 右斜
    (3, -9,  1, 9),    # 面霜 - 右斜
    (3, -9,  0, 11),   # 眼影 - 右斜
    (5, -9,  2, 10),   # 气垫 - 右斜
]
for i, (bar, val) in enumerate(zip(bars, values)):
    bx = bar.get_x() + bar.get_width() / 2
    by = bar.get_height()
    box_off, arr_base_off, arr_tip_off, arr_h_px = arrow_params[i]
    box_cx = bx + box_off * px_to_dx          # 标注框中心x
    box_bottom = by + arr_h_px * px_to_dy     # 框底=柱顶+箭头高
    box_top = box_bottom + box_h              # 框顶
    # 矩形标注框（与柱子同色，不裁剪以允许超出绘图区）
    rect = Rectangle((box_cx - box_w / 2, box_bottom), box_w, box_h,
                     facecolor=bar_colors[i], edgecolor='none', zorder=5,
                     clip_on=False)
    ax.add_patch(rect)
    # 斜三角箭头（宽端在框底偏移处，尖端在柱顶偏移处）
    arr_base_cx = box_cx + arr_base_off * px_to_dx
    arr_tip_x = bx + arr_tip_off * px_to_dx
    arrow = Polygon([
        (arr_base_cx - arrow_half_w, box_bottom),
        (arr_base_cx + arrow_half_w, box_bottom),
        (arr_tip_x, by),
    ], closed=True, facecolor=bar_colors[i], edgecolor='none', zorder=5,
       clip_on=False)
    ax.add_patch(arrow)
    # 数值文本（白色 8pt，居中于矩形框）
    ax.text(box_cx, (box_bottom + box_top) / 2, str(val),
            fontsize=8, color='white', ha='center', va='center', zorder=6,
            clip_on=False)

# 7. 标题与副标题（来自 drawing8.xml 文本框 11）
fig.text(0.05, 0.95, '2021年商品销量情况', fontsize=18, fontweight='bold',
         color='white', va='top', ha='left')
fig.text(0.05, 0.88, '口红销量最好达9221，是眼影最低值2645近3.5倍',
         fontsize=12, color='white', va='top', ha='left')

# 8. 底部注释（来自 drawing8.xml 文本框 12）
fig.text(0.04, 0.03, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 9. X 轴设置（标签 8pt #F2F2F2，无刻度线）
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8, color='#F2F2F2')
ax.tick_params(axis='x', length=0, pad=5)

# 10. Y 轴设置（0-10000，间隔 2000，标签 9pt #F2F2F2，有网格线）
ax.set_ylim(0, 10000)
ax.set_yticks(np.arange(0, 10001, 2000))
ax.set_yticklabels(np.arange(0, 10001, 2000), fontsize=9, color='#F2F2F2')
ax.tick_params(axis='y', length=0)

# 11. 网格线（长虚线，浅色，与 Excel majorGridlines 一致）
ax.yaxis.grid(True, linestyle=(0, (8, 4)), color='#FFFFFF', alpha=0.12)
ax.set_axisbelow(True)

# 12. 隐藏所有边框
for spine in ax.spines.values():
    spine.set_visible(False)

# 13. 精确设置绘图区域位置（与 Excel XML manualLayout 一致）
plt.subplots_adjust(left=0.142, right=0.142 + 0.786, top=1 - 0.299, bottom=1 - 0.299 - 0.538)

# 14. 保存图片（dpi=144 与 Excel 导出尺寸一致：832×616）
plt.savefig('标注柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
print("图片 '标注柱形图.png' 已成功生成！")
