import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json
import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─── Variabel Input ───────────────────────────────────────────────────────────
beban_akademik   = ctrl.Antecedent(np.arange(0, 101, 1), 'beban_akademik')
kualitas_tidur   = ctrl.Antecedent(np.arange(0, 101, 1), 'kualitas_tidur')
dukungan_sosial  = ctrl.Antecedent(np.arange(0, 101, 1), 'dukungan_sosial')
tekanan_waktu    = ctrl.Antecedent(np.arange(0, 101, 1), 'tekanan_waktu')

# ─── Variabel Output ──────────────────────────────────────────────────────────
risiko_burnout   = ctrl.Consequent(np.arange(0, 101, 1), 'risiko_burnout')

# ─── Fungsi Keanggotaan Input ─────────────────────────────────────────────────
for var in [beban_akademik, tekanan_waktu]:
    var['rendah']   = fuzz.trapmf(var.universe, [0,  0,  25, 45])
    var['sedang']   = fuzz.trimf(var.universe,  [25, 50, 75])
    var['tinggi']   = fuzz.trapmf(var.universe, [55, 75, 100, 100])

for var in [kualitas_tidur, dukungan_sosial]:
    var['buruk']    = fuzz.trapmf(var.universe, [0,  0,  25, 45])
    var['sedang']   = fuzz.trimf(var.universe,  [25, 50, 75])
    var['baik']     = fuzz.trapmf(var.universe, [55, 75, 100, 100])

# ─── Fungsi Keanggotaan Output ────────────────────────────────────────────────
risiko_burnout['sangat_rendah'] = fuzz.trapmf(risiko_burnout.universe, [0,  0,  10, 25])
risiko_burnout['rendah']        = fuzz.trapmf(risiko_burnout.universe, [10, 25, 35, 45])
risiko_burnout['sedang']        = fuzz.trapmf(risiko_burnout.universe, [35, 45, 55, 65])
risiko_burnout['tinggi']        = fuzz.trapmf(risiko_burnout.universe, [55, 65, 75, 85])
risiko_burnout['sangat_tinggi'] = fuzz.trapmf(risiko_burnout.universe, [75, 85, 100, 100])

# ─── Rules ────────────────────────────────────────────────────────────────────
rules = [
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['rendah'],  risiko_burnout['sangat_rendah']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['sedang'],  risiko_burnout['sangat_rendah']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['baik']   & dukungan_sosial['sedang']& tekanan_waktu['rendah'],  risiko_burnout['rendah']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['baik']   & dukungan_sosial['buruk'] & tekanan_waktu['rendah'],  risiko_burnout['rendah']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['sedang'] & dukungan_sosial['baik']  & tekanan_waktu['rendah'],  risiko_burnout['rendah']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['buruk']  & dukungan_sosial['baik']  & tekanan_waktu['rendah'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['rendah'],  risiko_burnout['rendah']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['sedang'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['baik']   & dukungan_sosial['sedang']& tekanan_waktu['sedang'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['sedang'] & dukungan_sosial['sedang']& tekanan_waktu['sedang'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['buruk']  & dukungan_sosial['sedang']& tekanan_waktu['sedang'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['buruk']  & dukungan_sosial['buruk'] & tekanan_waktu['sedang'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['baik']   & dukungan_sosial['buruk'] & tekanan_waktu['tinggi'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['sedang'] & dukungan_sosial['buruk'] & tekanan_waktu['tinggi'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['sedang'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['baik']   & dukungan_sosial['sedang']& tekanan_waktu['tinggi'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['sedang'] & dukungan_sosial['sedang']& tekanan_waktu['tinggi'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['buruk']  & dukungan_sosial['sedang']& tekanan_waktu['tinggi'],  risiko_burnout['sangat_tinggi']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['buruk']  & dukungan_sosial['buruk'] & tekanan_waktu['tinggi'],  risiko_burnout['sangat_tinggi']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['sedang'] & dukungan_sosial['buruk'] & tekanan_waktu['tinggi'],  risiko_burnout['sangat_tinggi']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['baik']   & dukungan_sosial['buruk'] & tekanan_waktu['tinggi'],  risiko_burnout['tinggi']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['buruk']  & dukungan_sosial['buruk'] & tekanan_waktu['tinggi'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['tinggi'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['tinggi']  & kualitas_tidur['baik']   & dukungan_sosial['baik']  & tekanan_waktu['rendah'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['sedang'] & dukungan_sosial['sedang']& tekanan_waktu['sedang'],  risiko_burnout['rendah']),
    ctrl.Rule(beban_akademik['rendah']  & kualitas_tidur['buruk']  & dukungan_sosial['sedang']& tekanan_waktu['sedang'],  risiko_burnout['sedang']),
    ctrl.Rule(beban_akademik['sedang']  & kualitas_tidur['sedang'] & dukungan_sosial['baik']  & tekanan_waktu['rendah'],  risiko_burnout['rendah']),
]

burnout_ctrl = ctrl.ControlSystem(rules)
burnout_sim  = ctrl.ControlSystemSimulation(burnout_ctrl)


def compute_burnout(beban, tidur, sosial, tekanan):
    burnout_sim.input['beban_akademik']  = beban
    burnout_sim.input['kualitas_tidur']  = tidur
    burnout_sim.input['dukungan_sosial'] = sosial
    burnout_sim.input['tekanan_waktu']   = tekanan
    burnout_sim.compute()
    nilai = burnout_sim.output['risiko_burnout']

    if nilai < 20:
        label = "Sangat Rendah"
        color = "#7F77DD"
        advice = "Kamu dalam kondisi prima! Pertahankan keseimbangan akademik dan istirahatmu."
        emoji  = "✨"
    elif nilai < 40:
        label = "Rendah"
        color = "#9B8FE8"
        advice = "Kondisimu cukup baik. Tetap jaga pola tidur dan koneksi sosialmu."
        emoji  = "🌿"
    elif nilai < 60:
        label = "Sedang"
        color = "#B8A0E8"
        advice = "Ada tanda-tanda kelelahan. Cobalah manajemen waktu yang lebih baik dan minta dukungan teman."
        emoji  = "⚠️"
    elif nilai < 80:
        label = "Tinggi"
        color = "#D4A0CC"
        advice = "Risiko burnout cukup serius. Kurangi beban, prioritaskan tidur, dan konsultasi ke konselor kampus."
        emoji  = "🔥"
    else:
        label = "Sangat Tinggi"
        color = "#E88FA0"
        advice = "Segera ambil tindakan! Istirahat total, bicara dengan dosen pembimbing, dan cari bantuan profesional."
        emoji  = "🚨"

    chart_b64 = generate_membership_chart(nilai)

    return {
        "nilai": round(nilai, 2),
        "label": label,
        "color": color,
        "advice": advice,
        "emoji": emoji,
        "chart": chart_b64,
    }


def generate_membership_chart(output_val):
    PURPLE = "#7F77DD"
    LIGHT  = "#EEEDFE"
    ACCENT = "#534AB7"

    fig, ax = plt.subplots(figsize=(7, 3))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')

    x = risiko_burnout.universe
    mfs = {
        'Sangat Rendah': risiko_burnout['sangat_rendah'].mf,
        'Rendah':        risiko_burnout['rendah'].mf,
        'Sedang':        risiko_burnout['sedang'].mf,
        'Tinggi':        risiko_burnout['tinggi'].mf,
        'Sangat Tinggi': risiko_burnout['sangat_tinggi'].mf,
    }
    colors = ['#AFA9EC', '#7F77DD', '#9B8FE8', '#B8A0E8', '#D4A0CC']

    for (name, mf), col in zip(mfs.items(), colors):
        ax.plot(x, mf, color=col, linewidth=2, label=name)
        ax.fill_between(x, mf, alpha=0.12, color=col)

    ax.axvline(x=output_val, color=ACCENT, linewidth=2, linestyle='--', alpha=0.8)
    ax.text(output_val + 1, 0.95, f'{output_val:.1f}', color=ACCENT,
            fontsize=9, va='top', fontweight='bold')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel('Tingkat Risiko Burnout', fontsize=9, color='#534AB7')
    ax.set_ylabel('Derajat Keanggotaan', fontsize=9, color='#534AB7')
    ax.tick_params(colors='#888')
    for spine in ax.spines.values():
        spine.set_edgecolor('#DDD')
    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.6,
              edgecolor='#DDD', facecolor='white')
    ax.grid(axis='y', linestyle=':', alpha=0.4, color='#CCC')

    plt.tight_layout(pad=0.8)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


if __name__ == '__main__':
    r = compute_burnout(75, 40, 35, 80)
    print(json.dumps(r, indent=2, ensure_ascii=False))
