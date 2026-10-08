import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
import numpy as np

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 622
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

def px2fig(px, py):
    return (px / W, 1 - py / H)

# 数据: 6个部门
# 扇区按逆时针排列: 财务部, 人力部, 行政部, 工程部, 采购部, 销售部
sectors = [
    {'label': '人力部', 'pct': '5.0%',  'value': 0.050, 'color': '#7030A0'},
    {'label': '行政部', 'pct': '10.3%', 'value': 0.103, 'color': '#0070C0'},
    {'label': '财务部', 'pct': '13.6%', 'value': 0.136, 'color': '#37A2DA'},
    {'label': '工程部', 'pct': '17.5%', 'value': 0.175, 'color': '#11A7AD'},
    {'label': '采购部', 'pct': '22.7%', 'value': 0.227, 'color': '#F5C353'},
    {'label': '销售部', 'pct': '29.2%', 'value': 0.292, 'color': '#E74E69'},
]

total = sum(s['value'] for s in sectors)
angles = [s['value'] / total * 360 for s in sectors]

# 中心位置和半径
cx_px, cy_px = 405, 365  # 图像坐标中心
max_radius_px = 240      # 最大半径(像素)
max_val = max(s['value'] for s in sectors)

# 绘制扇区 (matplotlib逆时针, 从90°开始)
# 在图像中表现为顺时针
cum_angle = 90.0
for i, s in enumerate(sectors):
    theta1 = cum_angle
    theta2 = cum_angle + angles[i]
    r_px = s['value'] / max_val * max_radius_px

    # 生成扇区多边形顶点
    verts = [(cx_px, cy_px)]  # 从中心开始
    n_arc = max(20, int(angles[i] / 3))  # 弧上的点数
    for j in range(n_arc + 1):
        t = np.radians(theta1 + (theta2 - theta1) * j / n_arc)
        x = cx_px + r_px * np.cos(t)
        y = cy_px - r_px * np.sin(t)  # 图像y向下
        verts.append((x, y))

    # 转fig坐标
    fig_verts = [px2fig(v[0], v[1]) for v in verts]
    poly = Polygon(fig_verts, closed=True, facecolor=s['color'], edgecolor='none',
                   transform=fig.transFigure, zorder=3)
    fig.add_artist(poly)
    cum_angle = theta2

# 引导线
guides = [
    ((628, 253), (660, 216), (763, 213), '#E74E69'),
    ((571, 492), (608, 528), (716, 528), '#F5C353'),
    ((287, 498), (255, 533), (134, 536), '#11A7AD'),
    ((265, 355), (234, 391), (114, 393), '#0070C0'),
    ((342, 289), (299, 252), (159, 252), '#37A2DA'),
    ((253, 220), (373, 222), (398, 256), '#7030A0'),
]
for (s, c, e, color) in guides:
    sf = px2fig(*s); cf = px2fig(*c); ef = px2fig(*e)
    fig.add_artist(Line2D([sf[0], cf[0]], [sf[1], cf[1]], color=color, linewidth=1.0, transform=fig.transFigure, zorder=4))
    fig.add_artist(Line2D([cf[0], ef[0]], [cf[1], ef[1]], color=color, linewidth=1.0, transform=fig.transFigure, zorder=4))
    # 紫色圆点在末端, 其余在起点
    dot = ef if color == '#7030A0' else sf
    fig.add_artist(Line2D([dot[0]], [dot[1]], marker='o', markersize=3, color=color, linestyle='None', transform=fig.transFigure, zorder=5))

# 标题/副标题/脚注
fig.text(0.06, 0.968, '2021年各部门人数分布', fontsize=18, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.884, '公司总人数1664，销售部人数最多451，占比29.2%', fontsize=12, color='#FFFFFF', va='top', ha='left')
fig.text(0.06, 0.068, '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01', fontsize=6.5, color='#D9D9D9', va='top', ha='left')

plt.savefig(r'D:\数据可视化\第一章后15\南丁格尔PPT.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '南丁格尔PPT.png' 已成功生成！")
