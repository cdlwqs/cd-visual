import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.ticker as mticker

# 1. 数据准备
projects = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
start_dates = [
    datetime(2022, 3, 1), datetime(2022, 3, 13), datetime(2022, 3, 22),
    datetime(2022, 4, 2), datetime(2022, 4, 16), datetime(2022, 5, 11), datetime(2022, 5, 26)
]
durations = [11, 8, 10, 13, 24, 14, 7]
completion = [0.51, 0.32, 0.21, 0.85, 0.36, 0.68, 0.68]
progress_days = [5.61, 2.56, 2.1, 11.05, 8.64, 9.52, 4.76]

color_bar = '#0070C0'
color_progress = '#00A3E6'
bg_color = '#1A1E43'

# 2. 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 画布 922×588 @ 144dpi
fig, ax = plt.subplots(figsize=(922 / 144, 588 / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制甘特图（Y轴反转，第一个项目在顶部）
y_pos = np.arange(len(projects))
start_nums = [mdates.date2num(d) for d in start_dates]

# 项目天数条（深蓝色）
ax.barh(y_pos, durations, left=start_nums, height=0.5,
        color=color_bar, edgecolor='none', zorder=2)

# 进行天数部分（亮蓝色）
ax.barh(y_pos, progress_days, left=start_nums, height=0.5,
        color=color_progress, edgecolor='none', zorder=3)

# 5. 完成度百分比标签
for i in range(len(projects)):
    mid_date = start_nums[i] + durations[i] / 2
    ax.text(mid_date, y_pos[i], f'{int(completion[i] * 100)}%',
            fontsize=8, color='#FFFFFF', ha='center', va='center', zorder=4,
            fontweight='bold')

# 6. Y轴标签（反转，第一个项目在顶部）
ax.set_yticks(y_pos)
ax.set_yticklabels(projects, fontsize=9, color='#FFFFFF')
ax.invert_yaxis()

# 7. X轴日期（设置为顶部）- 格式 2022/3/1（无前导零）
x_dates = [
    datetime(2022, 3, 1), datetime(2022, 3, 16), datetime(2022, 3, 31),
    datetime(2022, 4, 15), datetime(2022, 4, 30), datetime(2022, 5, 15),
    datetime(2022, 5, 30), datetime(2022, 6, 14)
]
ax.set_xticks([mdates.date2num(d) for d in x_dates])

# 自定义日期格式化：2022/3/1（无前导零）
def date_formatter(x, pos):
    dt = mdates.num2date(x)
    return f'{dt.year}/{dt.month}/{dt.day}'

ax.xaxis.set_major_formatter(mticker.FuncFormatter(date_formatter))
ax.tick_params(axis='x', labelsize=8, colors='#FFFFFF')
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

# 8. 虚线网格（垂直）：从顶部开始逐段绘制，段长16px间隙6px，线宽1pt，颜色#717993
from matplotlib.lines import Line2D
dash_len = 16 / 421
gap_len = 6 / 421
period = dash_len + gap_len
for d in x_dates:
    x_val = mdates.date2num(d)
    y = 1.0
    while y > 0:
        y2 = max(y - dash_len, 0.0)
        line = Line2D([x_val, x_val], [y2, y],
                      color='#717993', linewidth=1.0,
                      zorder=1, transform=ax.get_xaxis_transform())
        ax.add_line(line)
        y -= period

# 9. 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

# 10. 设置X轴范围
ax.set_xlim(mdates.date2num(datetime(2022, 3, 1)), mdates.date2num(datetime(2022, 6, 14)))

# 11. 标题（居中）
fig.text(0.5, 0.9795, '2022年化妆品类目采购项目进度',
         fontsize=16, fontweight='bold', color='#FFFFFF', va='top', ha='center')

# 12. 精确设置绘图区域（基于原图像素测量）
ax.set_position([0.1648, 0.0592, 0.7374, 0.7183])

# 13. 保存
plt.savefig(r'D:\数据可视化\第一章前15\甘特图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '甘特图.png' 已成功生成！")
