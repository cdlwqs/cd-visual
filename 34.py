import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
import imageio
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TC = '#FFFFFF'
SC = '#D9D9D9'
GRID = '#3D4A7A'

years = list(range(2011, 2026))
total = [134916,135922,136726,137646,138326,139232,140011,140541,141008,141212,141260,141175,140967,140828,140489]
male   = [69161,69660,70063,70522,70857,71307,71650,71864,72039,72357,72311,72206,72032,71909,71685]
female = [65755,66262,66663,67124,67469,67925,68361,68677,68969,68855,68949,68969,68935,68919,68804]
urban  = [69927,72175,74502,76738,79302,81924,84343,86433,88426,90220,91425,92071,93267,94350,95380]
rural  = [64989,63747,62224,60908,59024,57308,55668,54108,52582,50992,49835,49104,47700,46478,45109]

br_dict = {2016:13.57,2017:12.64,2018:10.86,2019:10.41,2020:8.52,2021:7.52,2022:6.77,2023:6.39,2024:6.77,2025:5.63}
dr_dict = {2016:7.04,2017:7.06,2018:7.08,2019:7.09,2020:7.07,2021:7.18,2022:7.37,2023:7.87,2024:7.76,2025:8.04}
ng_dict = {2016:6.53,2017:5.58,2018:3.78,2019:3.32,2020:1.45,2021:0.34,2022:-0.60,2023:-1.48,2024:-0.99,2025:-2.41}
a014_dict = {2016:23252,2017:23522,2018:23751,2019:23689,2020:25277,2021:24678,2022:23908,2023:23063,2024:22240,2025:21276}
a1564_dict = {2016:100943,2017:100528,2018:100065,2019:99552,2020:96871,2021:96526,2022:96289,2023:96228,2024:96565,2025:96848}
a65_dict = {2016:15037,2017:15961,2018:16724,2019:17767,2020:19064,2021:20056,2022:20978,2023:21676,2024:22023,2025:22365}

br_years = list(range(2016, 2026))
br_vals = [br_dict[y] for y in br_years]
dr_vals = [dr_dict[y] for y in br_years]
ng_vals = [ng_dict[y] for y in br_years]

def lerp(a, b, t):
    return a + (b - a) * t

def get_frame_data(fi, fpy, hs, n_trans):
    if fi < hs:
        return {'year': years[0], 'yi': 0}
    fi2 = fi - hs
    if fi2 >= n_trans:
        return {'year': years[-1], 'yi': len(years) - 1}
    i = fi2 // fpy
    f = (fi2 % fpy) / fpy
    frac = 3 * f**2 - 2 * f**3
    if i >= len(years) - 1:
        return {'year': years[-1], 'yi': len(years) - 1}
    return {'year': lerp(years[i], years[i+1], frac), 'yi': i, 'frac': frac}

def draw_frame(ax1, ax2, ax3, fig, d):
    yr = d['year']
    yi = d['yi']
    frac = d.get('frac', 0.0)

    ax1.clear()
    ax1.set_facecolor(BG)
    for spine in ax1.spines.values():
        spine.set_color(GRID)
    ax1.tick_params(colors=SC, labelsize=9)
    ax1.grid(True, alpha=0.15, color=GRID, linestyle='--')
    ax1.set_title('年末总人口（万人）', fontsize=13, color=TC, pad=10, loc='left')

    x = np.array(years, dtype=float)
    y = np.array(total, dtype=float)
    x_smooth = np.linspace(x.min(), x.max(), 200)
    interp = PchipInterpolator(x, y)
    y_smooth = interp(x_smooth)
    ax1.fill_between(x_smooth, y_smooth, y_smooth.min()-500, alpha=0.15, color='#4FC3F7')
    ax1.plot(x_smooth, y_smooth, color='#4FC3F7', linewidth=2.5)
    show_idx = min(yi, len(years)-1)
    if yi < len(years) - 1:
        cur_x = lerp(years[yi], years[yi+1], frac)
        cur_y = lerp(total[yi], total[yi+1], frac)
    else:
        cur_x = years[yi]
        cur_y = total[yi]
    ax1.scatter(x[:show_idx+1], y[:show_idx+1], color='#4FC3F7', s=30, zorder=5, edgecolors='white', linewidth=0.5)
    ax1.scatter([cur_x], [cur_y], color='#FFD700', s=80, zorder=6, edgecolors='white', linewidth=1)
    ax1.set_xlim(2010.5, 2025.5)
    ax1.set_ylim(134000, 142000)
    ax1.set_xticks(range(2011, 2026, 2))
    ax1.annotate(f'{cur_y:,.0f}', (cur_x, cur_y), textcoords="offset points",
                 xytext=(0, 12), ha='center', fontsize=9, color='#FFD700', fontweight='bold')

    ax2.clear()
    ax2.set_facecolor(BG)
    ax2.axis('off')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    yr_int = int(round(yr))
    ax2.text(0.0, 0.95, f'年龄结构（{yr_int}年）', fontsize=13, color=TC, fontweight='bold', va='top')

    if yi < len(years) - 1 and frac > 0:
        if yr_int in a014_dict and yr_int+1 in a014_dict:
            a014 = lerp(a014_dict[yr_int], a014_dict[yr_int+1], frac) if yr_int >= 2016 else a014_dict.get(yr_int, 23252)
            a1564 = lerp(a1564_dict[yr_int], a1564_dict[yr_int+1], frac) if yr_int >= 2016 else a1564_dict.get(yr_int, 100943)
            a65 = lerp(a65_dict[yr_int], a65_dict[yr_int+1], frac) if yr_int >= 2016 else a65_dict.get(yr_int, 15037)
        else:
            a014 = a014_dict.get(yr_int, 23252)
            a1564 = a1564_dict.get(yr_int, 100943)
            a65 = a65_dict.get(yr_int, 15037)
    else:
        a014 = a014_dict.get(yr_int, 23252)
        a1564 = a1564_dict.get(yr_int, 100943)
        a65 = a65_dict.get(yr_int, 15037)
    cur_total = lerp(total[yi], total[min(yi+1, len(total)-1)], frac) if yi < len(total)-1 else total[yi]

    age_data = [('0-14岁', a014, '#AB47BC'), ('15-64岁', a1564, '#42A5F5'), ('65岁及以上', a65, '#FF7043')]
    y_start = 0.82
    bar_h = 0.10
    for i, (label, val, color) in enumerate(age_data):
        yp = y_start - i * 0.25
        pct = val / cur_total * 100
        ax2.text(0.0, yp + bar_h + 0.03, label, fontsize=10, color=SC, va='bottom')
        ax2.add_patch(plt.Rectangle((0.0, yp), 1.0, bar_h, facecolor='#2C3E50', edgecolor='none'))
        ax2.add_patch(plt.Rectangle((0.0, yp), pct / 100, bar_h, facecolor=color, edgecolor='none'))
        ax2.text(pct / 100 + 0.02, yp + bar_h / 2, f'{pct:.1f}%', fontsize=10, color=color, va='center', fontweight='bold')
        ax2.text(0.0, yp - 0.03, f'{val:,.0f} 万人', fontsize=9, color=SC, va='top')

    ax3.clear()
    ax3.set_facecolor(BG)
    for spine in ax3.spines.values():
        spine.set_color(GRID)
    ax3.tick_params(colors=SC, labelsize=9)
    ax3.grid(True, alpha=0.15, color=GRID, linestyle='--')
    ax3.set_title('出生率、死亡率、自然增长率（‰）', fontsize=13, color=TC, pad=10, loc='left')

    xb = np.array(br_years, dtype=float)
    xb_smooth = np.linspace(xb.min(), xb.max(), 200)
    for data, color, label in [(br_vals, '#66BB6A', '出生率'), (dr_vals, '#EF5350', '死亡率'), (ng_vals, '#FFB74D', '自然增长率')]:
        yd = np.array(data, dtype=float)
        interp_d = PchipInterpolator(xb, yd)
        yd_smooth = interp_d(xb_smooth)
        ax3.plot(xb_smooth, yd_smooth, color=color, linewidth=2.5, label=label, alpha=0.4)
        if yr >= 2016:
            show_n = sum(1 for yb in br_years if yb <= yr)
            if show_n > 0:
                ax3.plot(xb_smooth[:int(show_n/len(br_years)*200)], yd_smooth[:int(show_n/len(br_years)*200)], color=color, linewidth=2.5)
                ax3.scatter(xb[:show_n], yd[:show_n], color=color, s=30, zorder=5, edgecolors='white', linewidth=0.5)
    ax3.axhline(y=0, color=GRID, linewidth=1, linestyle='-')
    ax3.set_xlim(2015.5, 2025.5)
    ax3.set_xticks(range(2016, 2026))
    ax3.set_ylim(-4, 16)
    ax3.legend(loc='upper right', fontsize=10, framealpha=0.3, facecolor=BG, edgecolor=GRID, labelcolor=TC)

    if yr >= 2016:
        ax3.axvline(x=yr, color='#FFD700', linewidth=1.5, linestyle='--', alpha=0.7)

    fig.texts.clear()
    fig.text(0.5, 0.97, '中国人口 2011—2025', ha='center', va='top', fontsize=22, color=TC, fontweight='bold')
    fig.text(0.5, 0.935, '数据来源：国家统计局年度数据', ha='center', va='top', fontsize=11, color=SC)
    fig.text(0.95, 0.97, f'{yr:.0f}', ha='right', va='top', fontsize=24, color='#4FC3F7', fontweight='bold', alpha=0.5)
    if yr >= 2016 and yr_int in ng_dict:
        ng_val = ng_dict[yr_int]
        fig.text(0.5, 0.025, f'出生率{br_dict[yr_int]:.2f}‰，自然增长率{ng_val:+.2f}‰', ha='center', va='bottom',
                 fontsize=11, color=SC, style='italic')
    else:
        fig.text(0.5, 0.025, f'{yr_int}年', ha='center', va='bottom', fontsize=11, color=SC, style='italic')

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    fpy, hs, he = 12, 12, 36
    n_trans = (len(years) - 1) * fpy
    tf = hs + n_trans + he
    print(f'总帧数: {tf}')

    fig = plt.figure(figsize=(16, 9), facecolor=BG)
    ax1 = fig.add_axes([0.06, 0.52, 0.42, 0.34])
    ax2 = fig.add_axes([0.55, 0.52, 0.40, 0.34])
    ax3 = fig.add_axes([0.06, 0.10, 0.88, 0.34])

    mp4 = os.path.join(out_dir, '中国人口仪表盘动画.mp4')
    w = imageio.get_writer(mp4, fps=24, codec='libx264', output_params=['-pix_fmt', 'yuv420p', '-crf', '20'])
    for fi in range(tf):
        d = get_frame_data(fi, fpy, hs, n_trans)
        draw_frame(ax1, ax2, ax3, fig, d)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
        w.append_data(buf)
        if (fi+1) % 30 == 0 or fi == 0:
            print(f'  {fi+1}/{tf}')
    w.close()
    plt.close(fig)
    print(f'视频: {mp4}')

if __name__ == '__main__':
    main()
