import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

bg_color = '#1A1E43'
values = [0.375, 0.29167, 0.20833, 0.125]
labels = ['[20,30)', '[30,40)', '[40,50)', '>=50']
percents = ['37.5%', '29.2%', '20.8%', '12.5%']
colors = ['#512DCB', '#6073F3', '#66CBDD', '#F5C353']

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 867, 620
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 南丁格尔玫瑰图: 中心正圆空洞, 各扇区从内径向外延伸层数与数据成正比
# 像素测量: 中心(432,372), 内径108px, 层宽14px, scale=168px/data_unit
r_in = 108 / 168       # 内径(正圆空洞半径)
layer_w = 14 / 168     # 每层宽度
layers_per_sector = [5, 4, 3, 2]  # 紫5/蓝4/青3/黄2 层

# 预算每个扇区的角度(Excel从12点顺时针, firstSliceAng=0)
sector_thetas = []
cumulative = 0
for val in values:
    arc_angle = val * 360
    theta2 = 90 - cumulative
    theta1 = theta2 - arc_angle
    sector_thetas.append((theta1, theta2))
    cumulative += arc_angle

for i, (theta1, theta2) in enumerate(sector_thetas):
    n = layers_per_sector[i]
    r_out = r_in + n * layer_w
    wedge = mpatches.Wedge((0, 0), r_out, theta1, theta2,
                           width=r_out - r_in, facecolor=colors[i], edgecolor='none', zorder=3)
    ax.add_patch(wedge)
    # 跑道线: 各层边界处画暗色细弧(约主色88%亮度)
    track_color = tuple(int(c * 0.88) for c in [int(colors[i][j:j+2], 16) for j in (1, 3, 5)])
    track_color = f'#{track_color[0]:02X}{track_color[1]:02X}{track_color[2]:02X}'
    for k in range(1, n):
        r_boundary = r_in + k * layer_w
        track = mpatches.Wedge((0, 0), r_boundary + 0.4/168, theta1, theta2,
                               width=0.8/168, facecolor=track_color, edgecolor='none', zorder=4)
        ax.add_patch(track)

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
# 中心映射到像素(432,372): left=432/867-0.465/2, bottom=1-372/620-0.650/2
ax.set_position([0.2658, 0.075, 0.465, 0.650])

# 引导线 (fig坐标, 原图像素换算)
# 每条引导线: [(px,py), (px,py), ...] 点序列 + [color, color, ...] 每段颜色
def px2fig(px, py):
    return (px / W, 1 - py / H)

gray = '#A6A6A6'
guides = [
    # 紫色: 灰对角 + 紫折线(水平→斜下)
    ([(591, 306), (676, 195)], [gray]),
    ([(798, 218), (670, 218), (635, 261)], ['#512DCB']),
    # 蓝色: 灰折线(水平→斜下) + 蓝折线(斜上→水平)
    ([(627, 536), (582, 537), (425, 548)], [gray]),
    ([(552, 528), (580, 568), (720, 569)], ['#6073F3']),
    # 青色: 灰对角 + 青折线(斜下→水平)
    ([(205, 344), (261, 350)], [gray]),
    ([(252, 340), (226, 376), (95, 377)], ['#66CBDD']),
    # 黄色: 灰对角 + 黄折线(水平→斜下)
    ([(286, 157), (354, 204)], [gray]),
    ([(170, 188), (308, 189), (330, 221)], ['#F5C353']),
]
# 彩色线靠近圆环一端的圆点
dots = [
    (636, 256, '#512DCB'),
    (553, 530, '#6073F3'),
    (254, 339, '#66CBDD'),
    (331, 223, '#F5C353'),
]
for dpx, dpy, dcol in dots:
    dfx, dfy = px2fig(dpx, dpy)
    dot = mpatches.Ellipse((dfx, dfy), 7/W, 7/H, facecolor=dcol, edgecolor='none',
                           transform=fig.transFigure, zorder=5)
    fig.add_artist(dot)
for pts, seg_colors in guides:
    figs = [px2fig(p[0], p[1]) for p in pts]
    for i in range(len(figs) - 1):
        col = seg_colors[i] if i < len(seg_colors) else seg_colors[-1]
        line = Line2D([figs[i][0], figs[i+1][0]], [figs[i][1], figs[i+1][1]],
                      color=col, linewidth=1.5, transform=fig.transFigure, zorder=6)
        fig.add_artist(line)

# 标签: (px_lab, py_lab, px_pct, py_pct, lab, pct, pct_color, ha)
label_info = [
    (694, 180, 697, 202, '[20,30)', '37.5%', '#512DCB', 'left'),
    (636, 521, 640, 543, '[30,40)', '29.2%', '#6073F3', 'left'),
    (188, 329, 185, 350, '[40,50)', '20.8%', '#66CBDD', 'right'),
    (273, 142, 273, 163, '>=50', '12.5%', '#FFFFFF', 'right'),
]
for (pxl, pyl, pxp, pyp, lab, pct, pct_color, ha) in label_info:
    fxl, fyl = px2fig(pxl, pyl)
    fxp, fyp = px2fig(pxp, pyp)
    fig.text(fxl, fyl, lab, fontsize=7, color='#FFFFFF', va='top', ha=ha, zorder=6)
    fig.text(fxp, fyp, pct, fontsize=7, color=pct_color, va='top', ha=ha, fontweight='bold', zorder=6)

fig.text(0.060, 0.968, '2022年上半各年龄段人数分布',
         fontsize=18, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.884, '公司平均年龄32.5，20-30员工比例最高占比37.5%',
         fontsize=12, color='#FFFFFF', va='top', ha='left')
fig.text(0.0611, 0.068, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         fontsize=6.5, color='#D9D9D9', va='top', ha='left')

plt.savefig(r'D:\数据可视化\第一章后15\南丁格尔圆环图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '南丁格尔圆环图.png' 已成功生成！")
