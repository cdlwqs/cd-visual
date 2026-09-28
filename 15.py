import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 1. 数据
completion = 0.65
bg_color = '#1A1E43'
water_color = '#0070C0'
border_outer = '#0070C0'
border_inner = '#0070C0'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 865×617 @ 144dpi（按原图深蓝背景区域精确测量）
fig, ax = plt.subplots(figsize=(865 / 144, 617 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制水球图
# 外圆（较粗深蓝边框）
circle_outer = mpatches.Circle((0, 0), 1.0, facecolor=bg_color, edgecolor=border_outer,
                               linewidth=2, zorder=2)
ax.add_patch(circle_outer)

# 内圆（较细亮蓝边框）
circle_inner = mpatches.Circle((0, 0), 0.92, facecolor=bg_color, edgecolor=border_inner,
                               linewidth=2, zorder=3)
ax.add_patch(circle_inner)

# 水填充（底部65%）
water_height = 2 * completion - 1
water = mpatches.Rectangle((-1, -1), 2, 1 + water_height,
                           facecolor=water_color, edgecolor='none', zorder=4)
clip_path = mpatches.Circle((0, 0), 0.92, transform=ax.transData)
water.set_clip_path(clip_path)
ax.add_patch(water)

# 5. 中心文字
ax.text(0, 0, '65%', fontsize=35, color='#FFFFFF', fontweight=400,
        ha='center', va='center', zorder=5)

# 6. 设置坐标轴
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')

# 7. 绘图区域（按原图测量：圆形中心x=0.481, y=0.543, 直径约366px）
ax.set_position([0.238, 0.12, 0.486, 0.681])

# 8. 标题和副标题（按原图像素位置精确设置）
fig.text(0.074, 0.945, '2022年上半年目标完成率',
         fontsize=20, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.072, 0.859, '截至6月30日销售目标总体完成率达到65%',
         fontsize=14, color="#FFFFFF", va='top', ha='left')

# 9. 脚注
fig.text(0.064, 0.076, '*注：数据来源于公司销售系统',
         fontsize=9, color='#FFFFFF', va='top', ha='left')

# 10. 保存
plt.savefig(r'D:\数据可视化\第一章前15\水球图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '水球图.png' 已成功生成！")
