import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 1. 数据准备（来自 Excel "1 渐变柱形图" 工作表）
categories = ['华北', '华南', '东北', '西北', '西南', '华东']
values = [2354, 1902, 3524, 2698, 2896, 2563]

# 2. 设置中文字体（与 Excel 文档一致：微软雅黑）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 创建画布，尺寸与 Excel 原图一致（416pt × 308.75pt → 5.78in × 4.29in）
fig, ax = plt.subplots(figsize=(5.78, 4.29))
fig.patch.set_facecolor('#1A1E43')
ax.set_facecolor('#1A1E43')

# 4. 自定义渐变 colormap: 底部 #0070C0 → 顶部 #00B0F0（与 Excel 渐变填充一致）
cmap = LinearSegmentedColormap.from_list('grad', ['#0070C0', '#00B0F0'])

# 5. 绘制柱形图（width=0.313 与 Excel gapWidth=219 一致，所有柱子等宽）
x = np.arange(len(categories))
bars = ax.bar(x, values, width=0.313, zorder=1)
ax.set_xlim(-0.5, len(categories) - 0.5)

# 6. 为每个柱子应用垂直渐变填充（从下到上：深蓝 → 浅蓝）
for bar in bars:
    height = bar.get_height()
    gradient = np.linspace(1, 0, 256).reshape(-1, 1)
    ax.imshow(gradient, aspect='auto',
              extent=[bar.get_x(), bar.get_x() + bar.get_width(), 0, height],
              cmap=cmap, zorder=2)

# 7. 数据标签（白色，9pt，加粗，柱顶外侧，与 Excel dLbls 一致）
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 60,
            f'{int(height)}', ha='center', va='bottom',
            fontsize=9, fontweight='bold', color='white')

# 8. 标题与副标题（微软雅黑，与 Excel 文本框一致）
fig.text(0.06, 0.93, '3月各区域销量分布', fontsize=20, fontweight='bold',
         color='white', va='top', ha='left')
fig.text(0.06, 0.85, '东北销量最多占比总销量的22%，华南销量最低',
         fontsize=14, color='white', va='top', ha='left')

# 9. 底部注释（8pt，浅灰色，与 Excel 一致）
fig.text(0.04, 0.025, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 10. X 轴设置（白色标签 9pt，无轴线、无刻度线）
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9, color='white')
ax.tick_params(axis='x', length=0, pad=5)

# 11. Y 轴设置（0-4000，间隔 1000，白色标签 9pt，无轴线、无刻度线）
ax.set_ylim(0, 4000)
ax.set_yticks(np.arange(0, 4001, 1000))
ax.set_yticklabels(np.arange(0, 4001, 1000), fontsize=9, color='white')
ax.tick_params(axis='y', length=0)

# 12. 网格线（浅灰虚线，与 Excel 一致）
ax.yaxis.grid(True, linestyle='--', color='#888888', alpha=0.3)
ax.set_axisbelow(True)

# 13. 隐藏所有边框
for spine in ax.spines.values():
    spine.set_visible(False)

# 14. 精确设置绘图区域位置（与 Excel XML manualLayout 完全一致）
plt.subplots_adjust(left=0.144, right=0.904, top=0.681, bottom=0.156)

# 15. 保存图片（dpi=144 与 Excel 导出尺寸一致：832×617）
plt.savefig('渐变柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
print("图片 '渐变柱形图.png' 已成功生成！")
