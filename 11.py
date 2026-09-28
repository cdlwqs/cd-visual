import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import pchip_interpolate

# 1. 数据准备
months = ['5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
values = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]

bg_color = '#1A1E43'
line_color = '#E66B4C'
yaxis_color = '#E66B4C'
legend_2021 = '#66CBDD'
legend_2022 = '#F5C353'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 832×616 @ 144dpi
fig, ax = plt.subplots(figsize=(832 / 144, 616 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 平滑曲线插值（PCHIP保形插值，避免端点过冲）
x = np.arange(len(months)) + 0.5
x_smooth = np.linspace(x.min(), x.max(), 200)
y_smooth = pchip_interpolate(x, values, x_smooth)

# 5. 绘制平滑折线
ax.plot(x_smooth, y_smooth, color=line_color, linewidth=1, zorder=3)

# 6. 数据标签（仅1月，index=8，数据点x=8.5）+ 垂直虚线
from matplotlib.lines import Line2D
vline_x = 8.572
vline_y_top = 0.959
vline_y_bot = 0.0
dash_px = 7
gap_px = 4
plot_h_px = 293
dash_axes = dash_px / plot_h_px
gap_axes = gap_px / plot_h_px
period_axes = dash_axes + gap_axes
yy = vline_y_top
while yy > vline_y_bot:
    yy2 = max(yy - dash_axes, vline_y_bot)
    line = Line2D([vline_x, vline_x], [yy2, yy],
                  color='#E66B4C', linewidth=0.8,
                  zorder=2, transform=ax.get_xaxis_transform())
    ax.add_line(line)
    yy -= period_axes
ax.text(8.572, 3950, '3782', fontsize=7, color='#FFFFFF', fontweight='bold',
        ha='center', va='bottom', zorder=5)

# 7. X轴：12个刻度线(0-11)形成11个等宽线段，标签在段中间
ax.set_xticks(np.arange(12))
ax.set_xticklabels([])
ax.set_xticks(np.arange(len(months)) + 0.5, minor=True)
ax.set_xticklabels(months, fontsize=9, color='#F2F2F2', minor=True)
ax.tick_params(axis='x', length=4, color='#D9D9D9')
ax.tick_params(axis='x', which='minor', length=0)
ax.set_xlim(0, 11)

# 8. Y轴
ax.set_ylim(0, 4000)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(['0', '1,000', '2,000', '3,000', '4,000'], fontsize=8, color=yaxis_color)
ax.tick_params(axis='y', length=0, colors=yaxis_color)
ax.spines['left'].set_visible(False)

# 9. X轴轴线
ax.spines['bottom'].set_color('#D9D9D9')
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 10. 无网格线（原图无网格线）

# 11. 标题和副标题
fig.text(0.054, 0.9542, '化妆品品类月度销量走势',
         fontsize=18, fontweight='bold', color='#FFFFFF', va='top', ha='left')
fig.text(0.054, 0.8700, '2022年销量迅速增加，1月最高，销量达到3782',
         fontsize=13, color='#E0E0E8', va='top', ha='left')

# 12. 图例条（2021青色 + 2022橙色）- 圆角矩形，文字在内部
from matplotlib.patches import FancyBboxPatch
legend_y = 0.1136
legend_h = 0.0503
fig.patches.append(FancyBboxPatch((0.0938, legend_y), 0.6394, legend_h,
                                  boxstyle="round,pad=0,rounding_size=0.006",
                                  facecolor=legend_2021, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.patches.append(FancyBboxPatch((0.7428, legend_y), 0.2344, legend_h,
                                  boxstyle="round,pad=0,rounding_size=0.006",
                                  facecolor=legend_2022, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(0.0938 + 0.6394/2, legend_y + legend_h/2, '2021',
         fontsize=10, color='#FFFFFF', ha='center', va='center', zorder=6)
fig.text(0.7428 + 0.2344/2, legend_y + legend_h/2, '2022',
         fontsize=10, color='#FFFFFF', ha='center', va='center', zorder=6)

# 13. 脚注
fig.text(0.05, 0.03, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=9, color='#AAAAAA', va='bottom', ha='left')

# 14. 精确设置绘图区域（基于原图像素测量）
ax.set_position([0.1215, 0.239, 0.8438, 0.476])

# 15. 保存
plt.savefig(r'D:\数据可视化\第一章前15\平滑折线图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '平滑折线图.png' 已成功生成！")
