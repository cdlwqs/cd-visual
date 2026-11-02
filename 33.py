import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TC = '#FFFFFF'
SC = '#D9D9D9'
GRID = '#3D4A7A'

years = list(range(2011, 2026))
total = [134916,135922,136726,137646,138326,139232,140011,140541,141008,141212,141260,141175,140967,140828,140489]

br_years = list(range(2016, 2026))
br = [13.57,12.64,10.86,10.41,8.52,7.52,6.77,6.39,6.77,5.63]
dr = [7.04,7.06,7.08,7.09,7.07,7.18,7.37,7.87,7.76,8.04]
ng = [6.53,5.58,3.78,3.32,1.45,0.34,-0.60,-1.48,-0.99,-2.41]

a014_2025 = 21276
a1564_2025 = 96848
a65_2025 = 22365
total_2025 = 140489

fig = plt.figure(figsize=(16, 9), facecolor=BG)

fig.text(0.5, 0.97, '中国人口 2011—2025', ha='center', va='top', fontsize=22, color=TC, fontweight='bold')
fig.text(0.5, 0.935, '数据来源：国家统计局年度数据', ha='center', va='top', fontsize=11, color=SC)
fig.text(0.95, 0.97, '2025', ha='right', va='top', fontsize=24, color='#4FC3F7', fontweight='bold', alpha=0.5)

ax1 = fig.add_axes([0.06, 0.52, 0.42, 0.34])
ax1.set_facecolor(BG)
for spine in ax1.spines.values():
    spine.set_color(GRID)
ax1.tick_params(colors=SC, labelsize=9)
ax1.grid(True, alpha=0.15, color=GRID, linestyle='--')

x = np.array(years, dtype=float)
y = np.array(total, dtype=float)
x_smooth = np.linspace(x.min(), x.max(), 200)
interp = PchipInterpolator(x, y)
y_smooth = interp(x_smooth)

ax1.fill_between(x_smooth, y_smooth, y_smooth.min()-500, alpha=0.15, color='#4FC3F7')
ax1.plot(x_smooth, y_smooth, color='#4FC3F7', linewidth=2.5)
ax1.scatter(x, y, color='#4FC3F7', s=30, zorder=5, edgecolors='white', linewidth=0.5)
ax1.set_title('年末总人口（万人）', fontsize=13, color=TC, pad=10, loc='left')
ax1.set_xlim(2010.5, 2025.5)
ax1.set_ylim(134000, 142000)
ax1.set_xticks(range(2011, 2026, 2))

for i in [0, -1]:
    ax1.annotate(f'{y[i]:,.0f}', (x[i], y[i]), textcoords="offset points",
                 xytext=(0, 12), ha='center', fontsize=8, color='#4FC3F7')

ax2 = fig.add_axes([0.55, 0.52, 0.40, 0.34])
ax2.set_facecolor(BG)
ax2.axis('off')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.text(0.0, 0.95, '年龄结构（2025年）', fontsize=13, color=TC, fontweight='bold', va='top')

age_data = [
    ('0-14岁', a014_2025, '#AB47BC'),
    ('15-64岁', a1564_2025, '#42A5F5'),
    ('65岁及以上', a65_2025, '#FF7043'),
]
y_start = 0.82
bar_h = 0.10
for i, (label, val, color) in enumerate(age_data):
    yp = y_start - i * 0.25
    pct = val / total_2025 * 100
    ax2.text(0.0, yp + bar_h + 0.03, label, fontsize=10, color=SC, va='bottom')
    ax2.add_patch(plt.Rectangle((0.0, yp), 1.0, bar_h, facecolor='#2C3E50', edgecolor='none'))
    ax2.add_patch(plt.Rectangle((0.0, yp), pct / 100, bar_h, facecolor=color, edgecolor='none'))
    ax2.text(pct / 100 + 0.02, yp + bar_h / 2, f'{pct:.1f}%', fontsize=10, color=color, va='center', fontweight='bold')
    ax2.text(0.0, yp - 0.03, f'{val:,} 万人', fontsize=9, color=SC, va='top')

ax3 = fig.add_axes([0.06, 0.10, 0.88, 0.34])
ax3.set_facecolor(BG)
for spine in ax3.spines.values():
    spine.set_color(GRID)
ax3.tick_params(colors=SC, labelsize=9)
ax3.grid(True, alpha=0.15, color=GRID, linestyle='--')
ax3.set_title('出生率、死亡率、自然增长率（‰）', fontsize=13, color=TC, pad=10, loc='left')

xb = np.array(br_years, dtype=float)
xb_smooth = np.linspace(xb.min(), xb.max(), 200)

for data, color, label in [(br, '#66BB6A', '出生率'), (dr, '#EF5350', '死亡率'), (ng, '#FFB74D', '自然增长率')]:
    yd = np.array(data, dtype=float)
    interp_d = PchipInterpolator(xb, yd)
    yd_smooth = interp_d(xb_smooth)
    ax3.plot(xb_smooth, yd_smooth, color=color, linewidth=2.5, label=label)
    ax3.scatter(xb, yd, color=color, s=30, zorder=5, edgecolors='white', linewidth=0.5)

ax3.axhline(y=0, color=GRID, linewidth=1, linestyle='-')
ax3.set_xlim(2015.5, 2025.5)
ax3.set_xticks(range(2016, 2026))
ax3.set_ylim(-4, 16)

legend = ax3.legend(loc='upper right', fontsize=10, framealpha=0.3, facecolor=BG, edgecolor=GRID, labelcolor=TC)

ax3.annotate(f'{br[-1]:.2f}‰', (xb[-1], br[-1]), textcoords="offset points",
             xytext=(8, 0), ha='left', fontsize=9, color='#66BB6A', va='center')
ax3.annotate(f'{dr[-1]:.2f}‰', (xb[-1], dr[-1]), textcoords="offset points",
             xytext=(8, 0), ha='left', fontsize=9, color='#EF5350', va='center')
ax3.annotate(f'{ng[-1]:+.2f}‰', (xb[-1], ng[-1]), textcoords="offset points",
             xytext=(8, 0), ha='left', fontsize=9, color='#FFB74D', va='center')

fig.text(0.5, 0.025, '出生率降至5.63‰，自然增长率-2.41‰，人口负增长时代来临', ha='center', va='bottom',
         fontsize=11, color=SC, style='italic')

import os
out_dir = os.path.dirname(os.path.abspath(__file__))
png = os.path.join(out_dir, '中国人口仪表盘.png')
fig.savefig(png, dpi=144, facecolor=BG)
plt.close(fig)
print(f'已保存: {png}')
