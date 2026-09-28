import matplotlib.pyplot as plt
import numpy as np

# 1. 数据准备（来自 Excel "2 带均值柱形图" 工作表）
categories = ['华北', '华南', '东北', '西北', '西南', '华东']
values = [2354, 1902, 3524, 2698, 2896, 2563]
mean_val = np.mean(values)  # 2656.17

# 2. 设置中文字体（与 Excel 文档一致：微软雅黑）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 3. 创建画布，尺寸与 Excel 原图一致（416pt × 296.87pt → 5.78in × 4.12in）
fig, ax = plt.subplots(figsize=(5.78, 4.12))
fig.patch.set_facecolor('#1A1E43')
ax.set_facecolor('#1A1E43')

# 4. 绘制柱形图（纯色 #0070C0，width=0.313 与 Excel gapWidth=219 一致）
x = np.arange(len(categories))
bars = ax.bar(x, values, width=0.313, color='#0070C0', zorder=2)
ax.set_xlim(-0.5, len(categories) - 0.5)

# 5. 数据标签（9pt，接近白色，柱顶外侧；华东标签放在柱子内部顶部下方）
for i, bar in enumerate(bars):
    height = bar.get_height()
    if i == len(bars) - 1:
        # 华东：数据标签放在柱顶下方（柱子内部），与原图一致
        ax.text(bar.get_x() + bar.get_width() / 2, height - 30,
                f'{int(height)}', ha='center', va='top',
                fontsize=9, color='#F2F2F2')
    else:
        ax.text(bar.get_x() + bar.get_width() / 2, height + 60,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=9, color='#F2F2F2')

# 6. 均值线（橙色 #FFC000，1.5pt，与 Excel lineChart 一致）
ax.axhline(y=mean_val, color='#FFC000', linewidth=1.5, zorder=3)

# 7. 标题与副标题（微软雅黑，与 Excel 文本框一致）
fig.text(0.05, 0.93, '3月各区域销量分布', fontsize=20, fontweight='bold',
         color='white', va='top', ha='left')
fig.text(0.05, 0.85, '东北销量最多占比总销量的22%，华南销量最低',
         fontsize=14, color='white', va='top', ha='left')

# 8. "平均值：2656" 标注（8pt，橙色，均值线上方右侧，与原图一致）
fig.text(0.83, 0.60, '平均值：2656', fontsize=8, color='#FFC000',
         va='top', ha='left')

# 9. 底部注释（8pt，浅灰色，与 Excel 一致）
fig.text(0.04, 0.025, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=8, color='#D9D9D9', va='bottom', ha='left')

# 10. X 轴设置（白色标签 9pt，有轴线 50%透明度，无刻度线）
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9, color='#F2F2F2')
ax.tick_params(axis='x', length=0, pad=5)
ax.spines['bottom'].set_color('white')
ax.spines['bottom'].set_alpha(0.5)

# 11. Y 轴隐藏（与 Excel valAx delete=1 一致）
ax.set_ylim(0, 4000)
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 12. 精确设置绘图区域位置（与 Excel XML manualLayout 一致）
plt.subplots_adjust(left=0.0588, right=0.9635, top=0.7656, bottom=0.1657)

# 13. 保存图片（dpi=144 与 Excel 导出尺寸一致）
plt.savefig('带均值柱形图.png', facecolor=fig.get_facecolor(), dpi=144)
print("图片 '带均值柱形图.png' 已成功生成！")
