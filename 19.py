import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 1. 数据
bg_color = '#1A1E43'
# 顺时针从12点钟: 销售, 采购, 工程, 财务, 行政, 人力
values = [0.292, 0.227, 0.175, 0.136, 0.103, 0.067]
colors = ['#E74E69', '#F5C353', '#11A7AD', '#0070C0', '#37A2DA', '#7030A0']

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×622 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 622 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制饼图
# firstSliceAng=0: 从90°(12点钟)开始, 顺时针
R = 1.0
cumulative = 0
sector_info = []
for i, (val, color) in enumerate(zip(values, colors)):
    arc_angle = val * 360
    theta2 = 90 - cumulative  # 起始角
    theta1 = theta2 - arc_angle  # 终止角(顺时针)
    
    wedge = mpatches.Wedge((0, 0), R, theta1, theta2,
                           facecolor=color, edgecolor='none', zorder=3)
    ax.add_patch(wedge)
    
    # 扇区中点角度(数学坐标)
    mid_angle = (theta1 + theta2) / 2
    sector_info.append({
        'mid_angle': mid_angle,
        'theta1': theta1,
        'theta2': theta2,
        'color': color,
        'val': val,
    })
    cumulative += arc_angle

# 5. 引导线 (从扇区边缘向外延伸)
for idx, info in enumerate(sector_info):
    mid = info['mid_angle']
    color = info['color']
    theta1 = info['theta1']
    theta2 = info['theta2']
    
    if idx == 5:  # 紫色: 横线, 起点在紫色区域内, 无圆点
        start_y = 0.63  # 再上去一点, 仍在浅蓝色区域上方
        # 紫色扇区114.1°方向上y=0.60对应的点
        r_at = start_y / np.sin(np.radians(114.1))
        start_x = r_at * np.cos(np.radians(114.1))
        end_x = (start_x + (-1.40)) / 2  # 缩短一半
        end_y = start_y
        ax.plot([start_x, end_x], [start_y, end_y],
                color=color, linewidth=1.5, zorder=4)
    elif idx == 4:  # 浅蓝色: 横线, 从最下面上去一点, 无圆点
        guide_angle = 148  # 在浅蓝色扇区内(114.1°~151.2°), 靠近最下面上去一点
        start_x = R * np.cos(np.radians(guide_angle))
        start_y = R * np.sin(np.radians(guide_angle))
        end_x = -1.20  # 缩短一点
        end_y = start_y
        ax.plot([start_x, end_x], [start_y, end_y],
                color=color, linewidth=1.5, zorder=4)
    elif idx == 3:  # 深蓝色: 横线, 从偏下引出, 无圆点
        guide_angle = -165  # 偏下位置
        start_x = R * np.cos(np.radians(guide_angle))
        start_y = R * np.sin(np.radians(guide_angle))
        end_x = -1.60  # 增加一点
        end_y = start_y
        ax.plot([start_x, end_x], [start_y, end_y],
                color=color, linewidth=1.5, zorder=4)
    else:  # 其他扇区: 折线 + 圆点
        start_x = R * np.cos(np.radians(mid))
        start_y = R * np.sin(np.radians(mid))
        
        if np.cos(np.radians(mid)) > 0:
            ext_r = 1.12
        else:
            ext_r = 1.08
        ext_x = ext_r * np.cos(np.radians(mid))
        ext_y = ext_r * np.sin(np.radians(mid))
        
        if np.cos(np.radians(mid)) > 0:
            end_x = 1.45
        else:
            end_x = -1.40
        end_y = ext_y

        if idx == 0:  # 红色线整体向右移
            shift = 0.1
            start_x += shift
            ext_x += shift
            end_x += shift

        ax.plot([start_x, ext_x], [start_y, ext_y],
                color=color, linewidth=1.5, zorder=4)
        ax.plot([ext_x, end_x], [ext_y, end_y],
                color=color, linewidth=1.5, zorder=4)
        if np.cos(np.radians(mid)) > 0:
            if idx == 0 or idx == 1:  # 红色和黄色: 圆点在起点
                ax.plot(start_x, start_y, 'o', color=color, markersize=3, zorder=5)
            else:
                ax.plot(ext_x, ext_y, 'o', color=color, markersize=3, zorder=5)

# 6. 设置坐标轴
ax.set_xlim(-1.5, 1.6)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_position([0.107, -0.112, 0.782, 1.047])

# 7. 标题和副标题
fig.text(0.066, 0.921, '2021年各部门人数分布',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='center', ha='left')
fig.text(0.064, 0.841, '公司总人数1664，销售部人数最多451，占比29.2%',
         fontsize=14, color='#FFFFFF', va='center', ha='left')

# 8. 脚注
fig.text(0.065, 0.051, '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01',
         fontsize=8, color='#D9D9D9', va='center', ha='left')

# 9. 保存
plt.savefig(r'D:\数据可视化\第一章后15\南丁格尔圆饼图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '南丁格尔圆饼图.png' 已成功生成！")
