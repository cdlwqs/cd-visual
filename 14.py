import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 1. 数据
completion = 0.85
bg_color = '#1A1E43'
color_start = '#7030A0'
color_end = '#E74E69'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布
fig = plt.figure(figsize=(832 / 144, 617 / 144))
fig.patch.set_facecolor(bg_color)

# 4. 用极坐标绘制渐变圆环
ax = fig.add_axes([0.297, 0.12, 0.422, 0.68], polar=True)
ax.set_facecolor(bg_color)

# 渐变色
cmap = LinearSegmentedColormap.from_list('grad', [color_start, color_end])

# 绘制85%部分（渐变）
n = 360
theta = np.linspace(0, 2 * np.pi * completion, n, endpoint=False)
width = 2 * np.pi * completion / n
colors = cmap(np.linspace(0, 1, n))
bars = ax.bar(theta, 1, width=width, bottom=0.9, color=colors,
              edgecolor='none', align='edge', zorder=2)

# 绘制15%部分（透明灰色）
theta2_start = 2 * np.pi * completion
theta2 = np.linspace(theta2_start, 2 * np.pi, int(n * (1-completion)), endpoint=False)
width2 = 2 * np.pi * (1 - completion) / int(n * (1-completion))
ax.bar(theta2, 1, width=width2, bottom=0.9, color='#FFFFFF', alpha=0.05,
       edgecolor='none', align='edge', zorder=2)

# 设置起始角度（Excel 300° = matplotlib -30° or 330°）
ax.set_theta_offset(np.radians(90))  # 12点方向
ax.set_theta_direction(-1)  # 顺时针
ax.set_theta_offset(np.radians(90) - np.radians(300))  # 300°起始

# 隐藏所有装饰
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['polar'].set_visible(False)
ax.grid(False)

# 5. 中心文字（用普通坐标）
ax_text = fig.add_axes([0.297, 0.12, 0.422, 0.68])
ax_text.set_facecolor('none')
ax_text.axis('off')
ax_text.set_xlim(-1, 1)
ax_text.set_ylim(-1, 1)
ax_text.text(0, 0.1, '85%', fontsize=30, color='#FFFFFF', fontweight=500,
             ha='center', va='center', zorder=5)
ax_text.text(0, -0.25, '目标完成率', fontsize=10, color='#FFFFFF',
             ha='center', va='center', zorder=5)

# 6. 标题和副标题
fig.text(0.08, 0.94, '2022年上半年目标完成率',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.08, 0.85, '截至6月30日销售目标总体完成率达到85%',
         fontsize=13, color='#FFFFFF', va='top', ha='left')

# 7. 脚注
fig.text(0.08, 0.03, '*注：数据来源于公司销售系统',
         fontsize=9, color='#AAAAAA', va='bottom', ha='left')

# 8. 保存
plt.savefig(r'D:\数据可视化\第一章前15\单值圆环图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '单值圆环图.png' 已成功生成！")
