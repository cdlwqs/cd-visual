import matplotlib.pyplot as plt
import numpy as np

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

W, H = 832, 594
fig, ax = plt.subplots(figsize=(W / 144, H / 144))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
monthly = [2354, 1902, 3524, 2698, 2896, 2563, 3156, 2896, 3621, 2635, 2963, 2789]
quarterly = [7780, 8157, 9673, 8387]
q_colors = ['#4A5BD1', '#FC6C0F', '#F6A50B', '#A2417B']

month_x = []
for q in range(4):
    for m in range(3):
        month_x.append(q * 3 + 1 + (m - 1) * 0.7)
month_x = np.array(month_x)
bar_w = 0.3

for q in range(4):
    cx = q * 3 + 1
    ax.bar(cx, quarterly[q], width=2.2, color=q_colors[q], alpha=0.25, edgecolor='none', zorder=2)
    ax.text(cx, quarterly[q] + max(quarterly) * 0.02, str(quarterly[q]), ha='center', va='bottom',
            color='#FFFFFF', fontsize=7, zorder=5)

for i in range(12):
    q = i // 3
    ax.bar(month_x[i], monthly[i], width=bar_w, color=q_colors[q], edgecolor='none', zorder=3)
    ax.text(month_x[i], monthly[i] + max(quarterly) * 0.03, str(monthly[i]), ha='center', va='bottom',
            color='#FFFFFF', fontsize=6, zorder=5)

ax.set_ylim(0, max(quarterly) * 1.15)
ax.set_xticks(month_x)
ax.set_xticklabels(months, color='#FFFFFF', fontsize=7)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0)
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.06, 0.95, '2021年各月化妆品销量走势', fontsize=18, fontweight='bold',
         color='#FFFFFF', va='top', ha='left')
fig.text(0.062, 0.88, '2021年第三季度销量最多9673，9月单月销量最大3621',
         fontsize=11, color='#D9D9D9', va='top', ha='left')
fig.text(0.06, 0.05, '*注：数据来源于公司销售系统，统计日期截至2021.12.31',
         fontsize=8, color='#D9D9D9', va='top', ha='left')

plt.subplots_adjust(left=0.08, right=0.92, top=0.75, bottom=0.15)
plt.savefig(r'D:\数据可视化\第一章后15\复合柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '复合柱形图.png' 已成功生成！")
