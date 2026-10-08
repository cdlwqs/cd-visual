import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 1. 数据
completion = 0.65
bg_color = '#1A1E43'
water_color = '#0070C0'
wave_color = '#0060B0'
border_color = '#0070C0'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 833×618 @ 144dpi（与原图深蓝背景区域一致）
fig, ax = plt.subplots(figsize=(833 / 144, 618 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 外圆边框
circle_border = mpatches.Circle((0, 0), 1.0, facecolor=bg_color, edgecolor=border_color,
                                linewidth=1.5, zorder=2)
ax.add_patch(circle_border)

# 5. 水填充（底部65%，带波浪效果）
water_level = 2 * completion - 1 - 0.05

# 生成波浪水面（模拟Excel波浪水球图动画帧）
wave_amplitude = 0.06
wave_frequency = 1.8

wave_x = np.linspace(-1, 1, 200)
wave_y = water_level - wave_amplitude * np.sin(wave_frequency * np.pi * wave_x)

# 构建水填充区域（波浪顶部 + 圆形底部）
fill_x = np.concatenate([wave_x, wave_x[::-1]])
fill_y = np.concatenate([wave_y, np.full(200, -1)])
fill_polygon = list(zip(fill_x, fill_y))
water = mpatches.Polygon(fill_polygon, facecolor=water_color, edgecolor='none', zorder=3)
clip_path = mpatches.Circle((0, 0), 0.91, transform=ax.transData)
water.set_clip_path(clip_path)
ax.add_patch(water)

# 6. 中心文字（fig坐标定位，与原图一致）
fig.text(0.5300, 0.4482, '65%', fontsize=35, color='#FFFFFF',
         ha='center', va='center', zorder=10)

# 7. 设置坐标轴
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')

# 8. 水球绘图区位置（与原图精确匹配）
ax.set_position([0.2515, 0.0720, 0.5343, 0.7201])

# 9. 标题和副标题
fig.text(0.067, 0.924, '本科及以上学历员占比',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.067, 0.84, '6月30日最新统计数据本科及以上员工占比65%',
         fontsize=14, color='#FFFFFF', va='top', ha='left')

# 10. 脚注
fig.text(0.067, 0.0485, '*注：数据来源于公司人力资源系统',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 11. 保存
plt.savefig(r'D:\数据可视化\第一章后15\波浪水球图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '波浪水球图.png' 已成功生成！")
