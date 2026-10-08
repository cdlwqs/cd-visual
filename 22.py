import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Annulus, Rectangle, Circle
from matplotlib.lines import Line2D
import numpy as np

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 580
fig = plt.figure(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
ax.set_facecolor(bg_color)

# 仪表盘参数 (放大, 置于白色绘图区中心略偏上)
cx, cy = 416, 240  # 圆心(axes坐标, y向上, 居中略偏上)
R_out, R_in = 200, 180  # 外圈蓝色环 (宽20)
r_out, r_in = 180, 160  # 内圈彩色环 (宽20, 和蓝环一样宽)
inner_out, inner_in = 160, 140  # 深蓝色内环 (宽20)

# 白色矩形绘图区 (大小=外圆直径, 正好框住外圆)
plot_x, plot_y, plot_w, plot_h = cx - R_out, cy - R_out, 2 * R_out, 2 * R_out
ax.add_patch(Rectangle((plot_x, plot_y), plot_w, plot_h,
                       facecolor='#FFFFFF', edgecolor='none', zorder=1))

# 外圈蓝色环 (完整360°, 调细)
ax.add_patch(Annulus((cx, cy), R_out, width=R_out - R_in,
                     facecolor='#0070C0', edgecolor='none', zorder=2))

# 深蓝色底环 (完整360°, 从彩色环外径到内环内径, 补充彩色没填充之处)
ax.add_patch(Annulus((cx, cy), r_out, width=r_out - inner_in,
                     facecolor='#1A1E43', edgecolor='none', zorder=3))

# 内圈彩色分段 (饱和度降低, 覆盖在深蓝底环上)
# 50-80 青色: mpl 144°~225° (饱和度再降 #0A6A78→#1A7088)
ax.add_patch(Wedge((cx, cy), r_out, 144, 225, width=r_out - r_in,
                   facecolor="#1E706C", edgecolor='none', zorder=4))
# 80-120 黄色: mpl 36°~144°
ax.add_patch(Wedge((cx, cy), r_out, 36, 144, width=r_out - r_in,
                   facecolor="#F3BF3CF9", edgecolor='none', zorder=4))
# 120-150 红色: mpl -45°~36° (饱和度再降 #D85070→#D86080)
ax.add_patch(Wedge((cx, cy), r_out, -45, 36, width=r_out - r_in,
                   facecolor="#DC2A4E", edgecolor='none', zorder=4))

# 每个环外围深蓝色细线 (三个圆轮廓)
for ring_r in [R_out, r_out, inner_out]:
    ax.add_patch(Circle((cx, cy), ring_r, facecolor='none', edgecolor='#1A1E43',
                        linewidth=0.8, zorder=5))

# 刻度角度定义
ticks = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
tick_angs = [225 - (v - 50) * 2.7 for v in ticks]  # mpl角度

# 刻度分割线 (径向细黑线, 从外环外边延长至最内环数字处)
for ang in tick_angs:
    rad = np.radians(ang)
    x1 = cx + 150 * np.cos(rad); y1 = cy + 150 * np.sin(rad)
    x2 = cx + R_out * np.cos(rad); y2 = cy + R_out * np.sin(rad)
    ax.add_line(Line2D([x1, x2], [y1, y2], color='#000000', linewidth=0.8, zorder=6))

# 指针 (指向76, mpl 154.8°, 长度110, 浅灰色)
ptr_ang = 154.8
ptr_len = 140
px = cx + ptr_len * np.cos(np.radians(ptr_ang))
py = cy + ptr_len * np.sin(np.radians(ptr_ang))
ax.add_line(Line2D([cx, px], [cy, py], color="#E0DCDC", linewidth=1.3, zorder=5))

# 刻度数字 50-150 (半径125, 最内环上, 白色)
for v, ang in zip(ticks, tick_angs):
    rad = np.radians(ang)
    tx = cx + 150 * np.cos(rad)
    ty = cy + 150 * np.sin(rad)
    ax.text(tx, ty, str(v), fontsize=9, color='#FFFFFF', ha='center', va='center', zorder=7)

# 标题 (顶部居中, 白色绘图区上方深蓝背景上, y=595确保不被白色区遮挡)
ax.text(W / 2, 525, '2022年6月29公司整体运营指数良好', fontsize=18, fontweight='bold',
        color='#FFFFFF', ha='center', va='center', zorder=7)

plt.savefig(r'D:\数据可视化\第一章后15\仪表盘图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '仪表盘图.png' 已成功生成！")
