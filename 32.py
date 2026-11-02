import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import imageio
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TC = '#FFFFFF'
SC = '#D9D9D9'
AC = '#4FC3F7'

years = list(range(2011, 2026))
total = [134916,135922,136726,137646,138326,139232,140011,140541,141008,141212,141260,141175,140967,140828,140489]
male   = [69161,69660,70063,70522,70857,71307,71650,71864,72039,72357,72311,72206,72032,71909,71685]
female = [65755,66262,66663,67124,67469,67925,68361,68677,68969,68855,68949,68969,68935,68919,68804]
urban  = [69927,72175,74502,76738,79302,81924,84343,86433,88426,90220,91425,92071,93267,94350,95380]
rural  = [64989,63747,62224,60908,59024,57308,55668,54108,52582,50992,49835,49104,47700,46478,45109]

br = {2016:13.57,2017:12.64,2018:10.86,2019:10.41,2020:8.52,2021:7.52,2022:6.77,2023:6.39,2024:6.77,2025:5.63}
dr = {2016:7.04,2017:7.06,2018:7.08,2019:7.09,2020:7.07,2021:7.18,2022:7.37,2023:7.87,2024:7.76,2025:8.04}
ng = {2016:6.53,2017:5.58,2018:3.78,2019:3.32,2020:1.45,2021:0.34,2022:-0.60,2023:-1.48,2024:-0.99,2025:-2.41}
a014 = {2016:23252,2017:23522,2018:23751,2019:23689,2020:25277,2021:24678,2022:23908,2023:23063,2024:22240,2025:21276}
a1564 = {2016:100943,2017:100528,2018:100065,2019:99552,2020:96871,2021:96526,2022:96289,2023:96228,2024:96565,2025:96848}
a65 = {2016:15037,2017:15961,2018:16724,2019:17767,2020:19064,2021:20056,2022:20978,2023:21676,2024:22023,2025:22365}

C_UM, C_UF = '#2E86C1', '#5DADE2'
C_RM, C_RF = '#E67E22', '#F5B041'

def lerp(a, b, t):
    return a + (b - a) * t

def get_data(fi, fpy, hs, n_trans):
    if fi < hs:
        return {'year':years[0],'total':total[0],'male':male[0],'female':female[0],'urban':urban[0],'rural':rural[0]}
    fi2 = fi - hs
    if fi2 >= n_trans:
        i = len(years) - 1
        return {'year':years[i],'total':total[i],'male':male[i],'female':female[i],'urban':urban[i],'rural':rural[i]}
    i = fi2 // fpy
    f = (fi2 % fpy) / fpy
    frac = 3 * f**2 - 2 * f**3
    if i >= len(years) - 1:
        i = len(years) - 1
        return {'year':years[i],'total':total[i],'male':male[i],'female':female[i],'urban':urban[i],'rural':rural[i]}
    return {
        'year': lerp(years[i], years[i+1], frac),
        'total': lerp(total[i], total[i+1], frac),
        'male': lerp(male[i], male[i+1], frac),
        'female': lerp(female[i], female[i+1], frac),
        'urban': lerp(urban[i], urban[i+1], frac),
        'rural': lerp(rural[i], rural[i+1], frac),
    }

def draw_sun(ax, d):
    ax.clear()
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect('equal')
    ax.axis('off')
    yr, tot = d['year'], d['total']
    urb, rur = d['urban'], d['rural']
    ml, fm = d['male'], d['female']
    mr = ml / tot
    um, uf = urb * mr, urb * (1 - mr)
    rm, rf = rur * mr, rur * (1 - mr)
    r1, r2 = 0.38, 0.62
    ax.add_patch(mpatches.Wedge((0,0), r1, 0, 360, width=r1, facecolor='#2C3E50', edgecolor=BG, linewidth=2))
    pu = urb / tot * 360
    pr = rur / tot * 360
    ax.add_patch(mpatches.Wedge((0,0), r2, 90, 90+pu, width=r2-r1, facecolor='#3D5A80', edgecolor=BG, linewidth=2))
    ax.add_patch(mpatches.Wedge((0,0), r2, 90+pu, 90+360, width=r2-r1, facecolor='#7B4F2C', edgecolor=BG, linewidth=2))
    pmu, pfu = um/urb*pu, uf/urb*pu
    pmr, pfr = rm/rur*pr, rf/rur*pr
    b = 90.0
    segs = [(b, b+pmu, C_UM, um), (b+pmu, b+pu, C_UF, uf),
            (b+pu, b+pu+pmr, C_RM, rm), (b+pu+pmr, b+360, C_RF, rf)]
    for a0, a1, c, v in segs:
        ax.add_patch(mpatches.Wedge((0,0), r2+(r2-r1), a0, a1, width=r2-r1, facecolor=c, edgecolor=BG, linewidth=1.5))
    ax.text(0, 0.06, '中国', ha='center', va='center', fontsize=13, color=TC, fontweight='bold')
    ax.text(0, -0.02, f'{yr:.0f}年', ha='center', va='center', fontsize=11, color=AC, fontweight='bold')
    ax.text(0, -0.10, f'{tot/10000:.2f}亿', ha='center', va='center', fontsize=10, color=SC)
    for ma, lb, pct in [(90+pu/2,'城镇',urb/tot*100), (90+pu+pr/2,'乡村',rur/tot*100)]:
        rd = np.radians(ma)
        ax.text((r1+r2)/2*np.cos(rd), (r1+r2)/2*np.sin(rd), f'{lb}\n{pct:.1f}%', ha='center', va='center', fontsize=9, color=TC, fontweight='bold')
    for a0, a1, c, v in segs:
        ma = (a0+a1)/2
        rd = np.radians(ma)
        lr = r2 + (r2-r1)/2
        pct = v/tot*100
        if pct > 4:
            lb = '男' if c in (C_UM, C_RM) else '女'
            ax.text(lr*np.cos(rd), lr*np.sin(rd), f'{lb}\n{pct:.1f}%', ha='center', va='center', fontsize=7, color='white')

def draw_info(ax, d):
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    yi = int(round(d['year']))
    t, u, r, m, f = d['total'], d['urban'], d['rural'], d['male'], d['female']
    ur = u/t*100
    sr = m/f*100
    ax.text(0.5, 0.95, f'{yi} 年', ha='center', va='top', fontsize=22, color=TC, fontweight='bold')
    ax.text(0.5, 0.86, '中国人口结构', ha='center', va='top', fontsize=12, color=SC)
    rows = [
        ('年末总人口', f'{t:,.0f} 万人', TC),
        ('城镇人口', f'{u:,.0f} 万人', C_UF),
        ('乡村人口', f'{r:,.0f} 万人', C_RF),
        ('城镇化率', f'{ur:.1f}%', AC),
        ('性别比(男:女)', f'{sr:.2f}', TC),
    ]
    y = 0.74
    for lb, val, c in rows:
        ax.text(0.08, y, lb, fontsize=10, color=SC, va='top')
        ax.text(0.92, y, val, fontsize=10, color=c, va='top', ha='right', fontweight='bold')
        y -= 0.07
    if yi in br:
        y -= 0.03
        ax.plot([0.08, 0.92], [y+0.02, y+0.02], color='#3D4A7A', linewidth=1)
        y -= 0.06
        ngc = '#66BB6A' if ng[yi] >= 0 else '#EF5350'
        for lb, val, c in [('出生率', f'{br[yi]:.2f} ‰', '#66BB6A'), ('死亡率', f'{dr[yi]:.2f} ‰', '#EF5350'), ('自然增长率', f'{ng[yi]:+.2f} ‰', ngc)]:
            ax.text(0.08, y, lb, fontsize=10, color=SC, va='top')
            ax.text(0.92, y, val, fontsize=10, color=c, va='top', ha='right', fontweight='bold')
            y -= 0.07
    if yi in a014:
        y -= 0.03
        ax.plot([0.08, 0.92], [y+0.02, y+0.02], color='#3D4A7A', linewidth=1)
        y -= 0.06
        for lb, val, c in [('0-14岁', f'{a014[yi]:,} 万人', '#AB47BC'), ('15-64岁', f'{a1564[yi]:,} 万人', '#42A5F5'), ('65岁及以上', f'{a65[yi]:,} 万人', '#FF7043'), ('老龄化率', f'{a65[yi]/t*100:.1f}%', '#FF7043')]:
            ax.text(0.08, y, lb, fontsize=10, color=SC, va='top')
            ax.text(0.92, y, val, fontsize=10, color=c, va='top', ha='right', fontweight='bold')
            y -= 0.07

def draw_tl(ax, d):
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    yr = d['year']
    p = (yr - 2011) / 14
    ax.plot([0.05, 0.95], [0.5, 0.5], color='#3D4A7A', linewidth=3)
    ax.plot([0.05, 0.05+p*0.9], [0.5, 0.5], color=AC, linewidth=3)
    for i, y in enumerate(years):
        xp = 0.05 + i/14*0.9
        c = AC if y <= yr else '#3D4A7A'
        ax.scatter(xp, 0.5, s=64 if y == int(round(yr)) else 25, color=c, zorder=5)
        if y % 5 == 0 or y == 2025:
            ax.text(xp, 0.15, str(y), ha='center', va='top', fontsize=8, color=TC if y <= yr else '#5A5E7A')

def draw_lg(ax):
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    for i, (c, lb) in enumerate([(C_UM,'城镇·男'),(C_UF,'城镇·女'),(C_RM,'乡村·男'),(C_RF,'乡村·女')]):
        y = 0.75 - i*0.22
        ax.scatter(0.15, y, s=100, color=c, zorder=5)
        ax.text(0.28, y, lb, fontsize=9, color=TC, va='center')

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    fpy, hs, he = 10, 10, 30
    n_trans = (len(years) - 1) * fpy
    tf = hs + n_trans + he
    print(f'总帧数: {tf}')

    fig = plt.figure(figsize=(14, 8), facecolor=BG)
    ax1 = fig.add_axes([0.02, 0.05, 0.52, 0.85])
    ax2 = fig.add_axes([0.56, 0.30, 0.40, 0.60])
    ax3 = fig.add_axes([0.02, 0.92, 0.96, 0.06])
    ax4 = fig.add_axes([0.56, 0.08, 0.40, 0.18])
    fig.text(0.5, 0.965, '中国人口结构变迁 2011-2025', ha='center', va='top', fontsize=16, color=TC, fontweight='bold')
    fig.text(0.5, 0.935, '数据来源：国家统计局年度数据', ha='center', va='top', fontsize=9, color=SC)

    mp4 = os.path.join(out_dir, '人口结构变迁.mp4')
    w = imageio.get_writer(mp4, fps=30, codec='libx264', output_params=['-pix_fmt', 'yuv420p', '-crf', '20'])
    for fi in range(tf):
        d = get_data(fi, fpy, hs, n_trans)
        draw_sun(ax1, d)
        draw_info(ax2, d)
        draw_tl(ax3, d)
        draw_lg(ax4)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
        w.append_data(buf)
        if (fi+1) % 30 == 0 or fi == 0:
            print(f'  {fi+1}/{tf}')
    w.close()
    plt.close(fig)
    print(f'视频: {mp4}')

    d = get_data(tf-1, fpy, hs, n_trans)
    fig2 = plt.figure(figsize=(14, 8), facecolor=BG)
    a1 = fig2.add_axes([0.02, 0.05, 0.52, 0.85])
    a2 = fig2.add_axes([0.56, 0.30, 0.40, 0.60])
    a3 = fig2.add_axes([0.02, 0.92, 0.96, 0.06])
    a4 = fig2.add_axes([0.56, 0.08, 0.40, 0.18])
    draw_sun(a1, d)
    draw_info(a2, d)
    draw_tl(a3, d)
    draw_lg(a4)
    fig2.text(0.5, 0.965, '中国人口结构变迁 2011-2025', ha='center', va='top', fontsize=16, color=TC, fontweight='bold')
    fig2.text(0.5, 0.935, '数据来源：国家统计局年度数据', ha='center', va='top', fontsize=9, color=SC)
    png = os.path.join(out_dir, '人口结构变迁_截图.png')
    fig2.savefig(png, dpi=144, facecolor=BG)
    plt.close(fig2)
    print(f'截图: {png}')

if __name__ == '__main__':
    main()
