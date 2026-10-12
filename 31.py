import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge

bg_color = '#1A1E43'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'aspect': 'equal'})
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

data = [
    ('信息科学与工程学院', '#4FC3F7', [
        ('计算机科学与技术', 450), ('软件工程', 400), ('网络工程', 300), ('数据科学与大数据技术', 350),
    ]),
    ('机电工程学院', '#81C784', [
        ('机械设计制造及其自动化', 400), ('材料成型及控制工程', 250), ('车辆工程', 300), ('机器人工程', 250),
    ]),
    ('商学院', '#FFB74D', [
        ('国际经济与贸易', 350), ('市场营销', 300), ('财务管理', 400), ('工商管理', 250),
    ]),
    ('文学院', '#E57373', [
        ('汉语言文学', 500), ('汉语国际教育', 300), ('新闻学', 200),
    ]),
    ('医学院', '#BA68C8', [
        ('临床医学', 500), ('护理学', 300), ('药学', 200), ('医学检验技术', 200),
    ]),
    ('外国语学院', '#7986CB', [
        ('英语', 500), ('日语', 200), ('翻译', 150),
    ]),
    ('经济管理学院', '#4DB6AC', [
        ('会计学', 400), ('经济学', 300), ('金融学', 300),
    ]),
    ('教育学院', '#FFD54F', [
        ('小学教育', 300), ('学前教育', 300), ('教育技术学', 200),
    ]),
    ('材料与纺织工程学院', '#A1887F', [
        ('高分子材料与工程', 300), ('纺织工程', 250), ('非织造材料与工程', 150),
    ]),
    ('生物与环境工程学院', '#90A4AE', [
        ('生物工程', 200), ('环境工程', 200), ('应用化学', 200),
    ]),
    ('建筑工程学院', '#F06292', [
        ('土木工程', 250), ('建筑学', 200), ('工程管理', 150),
    ]),
    ('艺术学院', '#64B5F6', [
        ('视觉传达设计', 150), ('环境设计', 120), ('产品设计', 100), ('服装与服饰设计', 130),
    ]),
    ('体育学院', '#AED581', [
        ('体育教育', 200), ('社会体育指导与管理', 100),
    ]),
    ('马克思主义学院', '#D4A574', [
        ('思想政治教育', 200),
    ]),
]

total = sum(sum(p[1] for p in majors) for _, _, majors in data)
print(f"总人数: {total}")

r0 = 0.12
r1 = 0.38
r2 = 0.62

center_circle = plt.Circle((0, 0), r0, facecolor='#0070C0', edgecolor='white', linewidth=1.5, zorder=5)
ax.add_patch(center_circle)
ax.text(0, 0.015, '嘉兴大学', ha='center', va='center', color='white', fontsize=10, fontweight='bold', zorder=6)
ax.text(0, -0.04, f'{total}人', ha='center', va='center', color='#D9D9D9', fontsize=7, zorder=6)

start_angle = 90
for college_name, college_color, majors in data:
    college_total = sum(m[1] for m in majors)
    college_sweep = 360 * college_total / total
    end_angle = start_angle - college_sweep

    wedge1 = Wedge((0, 0), r1, end_angle, start_angle, width=r1 - r0,
                   facecolor=college_color, edgecolor='white', linewidth=0.8, zorder=3)
    ax.add_patch(wedge1)

    mid_angle_col = np.radians((start_angle + end_angle) / 2)
    label_r_col = (r0 + r1) / 2
    lx_col = label_r_col * np.cos(mid_angle_col)
    ly_col = label_r_col * np.sin(mid_angle_col)
    rotation_col = (start_angle + end_angle) / 2
    if 90 < rotation_col < 270:
        rotation_col -= 180
    if college_sweep > 12:
        ax.text(lx_col, ly_col, college_name, ha='center', va='center', color='white',
                fontsize=5.5, rotation=rotation_col, zorder=5)

    major_start = start_angle
    for major_name, major_value in majors:
        major_sweep = 360 * major_value / total
        major_end = major_start - major_sweep

        wedge2 = Wedge((0, 0), r2, major_end, major_start, width=r2 - r1,
                       facecolor=college_color, edgecolor='white', linewidth=0.5, zorder=2, alpha=0.6)
        ax.add_patch(wedge2)

        mid_angle_major = np.radians((major_start + major_end) / 2)
        label_r_major = (r1 + r2) / 2
        lx_major = label_r_major * np.cos(mid_angle_major)
        ly_major = label_r_major * np.sin(mid_angle_major)
        rotation_major = (major_start + major_end) / 2
        if 90 < rotation_major < 270:
            rotation_major -= 180
        if major_sweep > 4:
            ax.text(lx_major, ly_major + 0.015, major_name, ha='center', va='center', color='white',
                    fontsize=4, rotation=rotation_major, zorder=4)
            ax.text(lx_major, ly_major - 0.02, f'{major_value}', ha='center', va='center', color='#E0E0E0',
                    fontsize=3.5, rotation=rotation_major, zorder=4)

        major_start = major_end

    start_angle = end_angle

ax.set_xlim(-0.75, 0.75)
ax.set_ylim(-0.75, 0.75)
ax.axis('off')

fig.text(0.5, 0.97, '嘉兴大学各学院及专业人数分布', ha='center', va='top',
         color='#FFFFFF', fontsize=16, fontweight='bold')
fig.text(0.5, 0.94, f'总人数 {total} 人（估计数据）', ha='center', va='top',
         color='#D9D9D9', fontsize=10)

plt.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02)
plt.savefig(r'D:\数据可视化\第一章后15\嘉兴大学旭日图.png', facecolor=fig.get_facecolor(), dpi=144)
plt.close()
print("图片 '嘉兴大学旭日图.png' 已成功生成！")
