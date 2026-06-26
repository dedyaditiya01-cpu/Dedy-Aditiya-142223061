import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ╔══════════════════════════════════════════════════════╗
# ║              KONFIGURASI HALAMAN                    ║
# ╚══════════════════════════════════════════════════════╝
st.set_page_config(
    page_title="Survei Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ╔══════════════════════════════════════════════════════╗
# ║                  STYLE / CSS                        ║
# ╚══════════════════════════════════════════════════════╝
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* ── Background utama gelap ── */
.stApp {
    background: #0a0e1a !important;
}

/* ── Sidebar gelap elegan ── */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1e2d4a !important;
    min-width: 280px !important;
}
section[data-testid="stSidebar"] > div {
    background: #0d1117 !important;
    padding: 0 !important;
}
/* Semua teks sidebar putih */
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}
/* Selectbox di sidebar */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1a2332 !important;
    border: 1px solid #2d4a6b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stSelectbox svg {
    fill: #64748b !important;
}
/* Metric di sidebar */
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #1a2332 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    margin-bottom: 10px !important;
}
section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    color: #60a5fa !important;
}
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: #64748b !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #1e2d4a !important;
    margin: 14px 0 !important;
}

/* ── Tombol collapse sidebar — pastikan muncul ── */
button[kind="header"] {
    background: #1a2332 !important;
    color: white !important;
    border: 1px solid #2d4a6b !important;
}
[data-testid="collapsedControl"] {
    background: #1a2332 !important;
    border-right: 1px solid #2d4a6b !important;
}
[data-testid="collapsedControl"] svg {
    fill: #60a5fa !important;
}

/* ── Main content area ── */
.main .block-container {
    background: transparent !important;
    padding: 24px 32px 40px !important;
    max-width: 1400px !important;
}

/* ── KPI Cards ── */
.kpi-wrap {
    background: linear-gradient(135deg, #111827 0%, #1a2332 100%);
    border: 1px solid #1e3a5f;
    border-radius: 18px;
    padding: 22px 18px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform .2s, box-shadow .2s;
}
.kpi-wrap:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,.5);
}
.kpi-wrap::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent-color);
    border-radius: 18px 18px 0 0;
}
.kpi-icon  { font-size: 1.9rem; line-height: 1; margin-bottom: 10px; }
.kpi-value { font-size: 2.1rem; font-weight: 800; color: #f1f5f9; line-height: 1; }
.kpi-label { font-size: 0.72rem; color: #64748b; margin-top: 6px;
             font-weight: 600; text-transform: uppercase; letter-spacing: 0.7px; }
.kpi-sub   { font-size: 0.7rem; color: #475569; margin-top: 4px; }

/* ── Section header ── */
.sec-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #60a5fa;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 28px 0 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2d4a;
    margin-left: 8px;
}

/* ── Chart / Content cards ── */
.card {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 22px 20px 14px;
    margin-bottom: 16px;
}
.card-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
}
.card-sub {
    font-size: 0.75rem;
    color: #475569;
    margin-bottom: 14px;
}

/* ── Progress bars ── */
.prog-row { margin-bottom: 18px; }
.prog-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3px;
}
.prog-name  { font-size: 0.88rem; font-weight: 600; color: #e2e8f0; }
.prog-pct   { font-size: 0.88rem; font-weight: 700; }
.prog-desc  { font-size: 0.74rem; color: #475569; margin-bottom: 6px; }
.prog-track { background: #1e2d4a; border-radius: 99px; height: 12px; overflow: hidden; }
.prog-fill  { height: 12px; border-radius: 99px; }
.prog-status { font-size: 0.72rem; font-weight: 600; margin-top: 4px; }

/* ── Info box ── */
.info-box {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 14px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117 !important;
    border-bottom: 1px solid #1e2d4a !important;
    gap: 0 !important;
    padding: 0 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    color: #60a5fa !important;
    border-bottom: 2px solid #3b82f6 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 20px 0 !important;
}

/* ── Selectbox & input global (dark) ── */
.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stSelectbox label { color: #94a3b8 !important; font-size: 0.78rem !important; }

/* ── Dataframe dark ── */
.stDataFrame {
    border: 1px solid #1e2d4a !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.stDataFrame thead th {
    background: #1a2332 !important;
    color: #60a5fa !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
}
.stDataFrame tbody tr { background: #111827 !important; color: #e2e8f0 !important; }
.stDataFrame tbody tr:nth-child(even) { background: #0d1117 !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: #1a2332 !important;
    border: 1px solid #2d4a6b !important;
    color: #60a5fa !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 8px 18px !important;
    transition: all .2s !important;
}
.stDownloadButton > button:hover {
    background: #1e3a5f !important;
    border-color: #3b82f6 !important;
}

/* ── Divider ── */
hr { border-color: #1e2d4a !important; }

/* ── Sembunyikan branding Streamlit ── */
#MainMenu, footer, header { visibility: hidden !important; }

/* ── Scrollbar gelap ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════╗
# ║                   LOAD DATA                         ║
# ╚══════════════════════════════════════════════════════╝
@st.cache_data
def load_data():
    df = pd.read_excel("Survei_kepuasan_mahasiswa__Responses_.xlsx")
    df.columns = [
        "Timestamp", "Nama", "Kelas", "NIM",
        "Kursi & Meja",
        "Suhu Udara",
        "Proyektor (LCD)",
        "Stop Kontak",
        "Kedap Suara",
        "Kebersihan",
        "Kenyamanan Keseluruhan",
    ]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()
ASPEK = df.columns[4:].tolist()

ASPEK_INFO = {
    "Kursi & Meja":           {"icon": "🪑", "desc": "Ketersediaan kursi & meja untuk seluruh mahasiswa"},
    "Suhu Udara":             {"icon": "❄️", "desc": "Kenyamanan suhu & sirkulasi udara ruangan"},
    "Proyektor (LCD)":        {"icon": "📽️", "desc": "Fungsi normal proyektor & layar LCD"},
    "Stop Kontak":            {"icon": "🔌", "desc": "Ketersediaan stop kontak yang mudah dijangkau"},
    "Kedap Suara":            {"icon": "🔇", "desc": "Minimnya gangguan suara dari luar kelas"},
    "Kebersihan":             {"icon": "🧹", "desc": "Kebersihan lantai, meja, & sudut ruangan"},
    "Kenyamanan Keseluruhan": {"icon": "😊", "desc": "Kenyamanan belajar selama durasi 2 jam"},
}

WARNA_KELAS = {"Pagi": "#f59e0b", "Malam A": "#3b82f6", "Malam B": "#a855f7"}
C_HIJAU = "#22c55e"
C_KUNING = "#eab308"
C_MERAH = "#ef4444"
C_BIRU = "#3b82f6"

def warna_pct(pct):
    if pct >= 75: return C_HIJAU, "🟢 Baik"
    elif pct >= 55: return C_KUNING, "🟡 Cukup"
    else: return C_MERAH, "🔴 Perlu Perhatian"


# ╔══════════════════════════════════════════════════════╗
# ║                    SIDEBAR                          ║
# ╚══════════════════════════════════════════════════════╝
with st.sidebar:
    # Logo & judul
    st.markdown("""
    <div style='padding: 28px 20px 20px; border-bottom: 1px solid #1e2d4a;'>
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:12px;'>
            <div style='background:linear-gradient(135deg,#1d4ed8,#7c3aed);
                        width:42px; height:42px; border-radius:12px;
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.3rem;'>🎓</div>
            <div>
                <div style='font-size:0.9rem; font-weight:700; color:#f1f5f9;
                            line-height:1.2;'>Survei Kepuasan</div>
                <div style='font-size:0.7rem; color:#475569; margin-top:2px;'>
                    Mahasiswa Teknik Industri</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter
    st.markdown("""
    <div style='padding: 18px 20px 0;'>
        <div style='font-size:0.7rem; font-weight:700; color:#475569;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>
            ⚙️ Filter Data
        </div>
    </div>
    """, unsafe_allow_html=True)

    kelas_pilihan = st.selectbox(
        "Pilih Kelas",
        ["Semua Kelas"] + sorted(df["Kelas"].unique().tolist()),
        key="kelas_filter"
    )

    df_f = df if kelas_pilihan == "Semua Kelas" else df[df["Kelas"] == kelas_pilihan]
    avg_global = (df_f[ASPEK] == 1).mean().mean() * 100

    st.divider()

    # Statistik cepat
    st.markdown("""
    <div style='padding: 0 4px;'>
        <div style='font-size:0.7rem; font-weight:700; color:#475569;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>
            📊 Statistik Cepat
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.metric("👥 Total Responden", len(df_f))
    st.metric("✅ Rata-rata Puas", f"{avg_global:.1f}%")
    st.metric("🏫 Jumlah Kelas", df_f["Kelas"].nunique())

    st.divider()

    # Legenda kelas
    st.markdown("""
    <div style='padding: 0 4px;'>
        <div style='font-size:0.7rem; font-weight:700; color:#475569;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>
            🏷️ Kelas Aktif
        </div>
    </div>
    """, unsafe_allow_html=True)

    for k, w in WARNA_KELAS.items():
        n = len(df[df["Kelas"] == k])
        avg_k = (df[df["Kelas"] == k][ASPEK] == 1).mean().mean() * 100
        st.markdown(f"""
        <div style='background:#1a2332; border:1px solid #1e3a5f; border-left:3px solid {w};
                    border-radius:10px; padding:10px 14px; margin-bottom:8px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:0.83rem; font-weight:700; color:#e2e8f0;'>
                    Kelas {k}</span>
                <span style='font-size:0.72rem; color:{w}; font-weight:700;'>
                    {avg_k:.0f}%</span>
            </div>
            <div style='font-size:0.72rem; color:#475569; margin-top:3px;'>
                {n} mahasiswa</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Keterangan skala
    st.markdown("""
    <div style='padding: 0 4px;'>
        <div style='font-size:0.7rem; font-weight:700; color:#475569;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>
            📌 Keterangan Skala
        </div>
        <div style='background:#1a2332; border:1px solid #1e3a5f; border-radius:10px;
                    padding:12px 14px;'>
            <div style='font-size:0.78rem; color:#e2e8f0; margin-bottom:6px;'>
                <span style='color:#22c55e; font-weight:700;'>1 = Ya / Puas</span><br>
                <span style='color:#94a3b8; font-size:0.72rem;'>Fasilitas sudah memadai</span>
            </div>
            <div style='font-size:0.78rem; color:#e2e8f0;'>
                <span style='color:#ef4444; font-weight:700;'>2 = Tidak / Kurang</span><br>
                <span style='color:#94a3b8; font-size:0.72rem;'>Perlu perbaikan</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 18px 20px 10px; border-top: 1px solid #1e2d4a; margin-top: 14px;'>
        <div style='font-size:0.7rem; color:#334155; text-align:center; line-height:1.5;'>
            📅 Data: Maret 2026<br>Program Studi Teknik Industri
        </div>
    </div>
    """, unsafe_allow_html=True)

df_f = df if kelas_pilihan == "Semua Kelas" else df[df["Kelas"] == kelas_pilihan]
avg_global = (df_f[ASPEK] == 1).mean().mean() * 100
aspek_terbaik  = (df_f[ASPEK] == 1).mean().idxmax()
aspek_terburuk = (df_f[ASPEK] == 1).mean().idxmin()
pct_terbaik    = (df_f[ASPEK] == 1).mean().max() * 100
pct_terburuk   = (df_f[ASPEK] == 1).mean().min() * 100


# ╔══════════════════════════════════════════════════════╗
# ║                  HEADER UTAMA                       ║
# ╚══════════════════════════════════════════════════════╝
kelas_label = kelas_pilihan if kelas_pilihan != "Semua Kelas" else "Pagi · Malam A · Malam B"

st.markdown(f"""
<div style='background:linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            border: 1px solid #1e3a5f;
            border-radius: 20px; padding: 28px 32px; margin-bottom: 24px;
            box-shadow: 0 4px 24px rgba(0,0,0,.5);'>

    <div style='font-size:0.7rem; font-weight:700; color:#3b82f6;
                letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;'>
        📋 Program Studi Teknik Industri &nbsp;·&nbsp; Fasilitas Ruang Kelas
    </div>

    <h1 style='margin:0; color:#f1f5f9; font-size:1.8rem; font-weight:800;
               line-height:1.25; letter-spacing:-0.3px;'>
        Dashboard Survei Kepuasan Mahasiswa
    </h1>

    <div style='margin-top:14px; display:flex; gap:10px; flex-wrap:wrap; align-items:center;'>
        <div style='background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1);
                    color:#cbd5e1; padding:5px 14px; border-radius:99px;
                    font-size:0.78rem; font-weight:500;'>
            🏫 {kelas_label}
        </div>
        <div style='background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1);
                    color:#cbd5e1; padding:5px 14px; border-radius:99px;
                    font-size:0.78rem; font-weight:500;'>
            👥 {len(df_f)} Responden
        </div>
        <div style='background:rgba(34,197,94,.12); border:1px solid rgba(34,197,94,.3);
                    color:#4ade80; padding:5px 14px; border-radius:99px;
                    font-size:0.78rem; font-weight:700;'>
            ✅ {avg_global:.1f}% Tingkat Kepuasan
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════╗
# ║                    KPI CARDS                        ║
# ╚══════════════════════════════════════════════════════╝
c1, c2, c3, c4 = st.columns(4, gap="medium")

kpi_data = [
    ("#3b82f6", "👥", str(len(df_f)), "Total Responden", f"{df_f['Kelas'].nunique()} kelas aktif"),
    ("#22c55e", "✅", f"{avg_global:.1f}%", "Rata-rata Kepuasan", "Dari seluruh aspek fasilitas"),
    ("#f59e0b", "⭐", f"{pct_terbaik:.0f}%",
     f"Terbaik: {aspek_terbaik}",
     f"{ASPEK_INFO[aspek_terbaik]['icon']} Aspek tertinggi"),
    ("#ef4444", "⚠️", f"{pct_terburuk:.0f}%",
     f"Perhatian: {aspek_terburuk}",
     f"{ASPEK_INFO[aspek_terburuk]['icon']} Perlu ditingkatkan"),
]

for col, (accent, icon, val, label, sub) in zip([c1, c2, c3, c4], kpi_data):
    with col:
        st.markdown(f"""
        <div class='kpi-wrap' style='--accent-color:{accent}'>
            <div class='kpi-icon'>{icon}</div>
            <div class='kpi-value'>{val}</div>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════╗
# ║                      TABS                           ║
# ╚══════════════════════════════════════════════════════╝
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Ringkasan Utama",
    "🔍  Detail Per Aspek",
    "🏫  Perbandingan Kelas",
    "📋  Data Lengkap",
])


# ─────────────────────────────────────────────────────
# TAB 1 — RINGKASAN UTAMA
# ─────────────────────────────────────────────────────
with tab1:
    left, right = st.columns([3, 2], gap="large")

    # ── Kiri: Progress bars ──────────────────────────
    with left:
        st.markdown("""
        <div class='sec-title'>📈 Tingkat Kepuasan Per Aspek Fasilitas</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        pct_series = (df_f[ASPEK] == 1).mean() * 100
        for aspek, pct in pct_series.sort_values(ascending=False).items():
            info = ASPEK_INFO[aspek]
            color, status = warna_pct(pct)
            st.markdown(f"""
            <div class='prog-row'>
                <div class='prog-head'>
                    <span class='prog-name'>{info['icon']} &nbsp;{aspek}</span>
                    <span class='prog-pct' style='color:{color}'>{pct:.1f}%</span>
                </div>
                <div class='prog-desc'>{info['desc']}</div>
                <div class='prog-track'>
                    <div class='prog-fill'
                         style='width:{pct}%; background:linear-gradient(90deg,{color}88,{color});'>
                    </div>
                </div>
                <div class='prog-status' style='color:{color}'>{status}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Kanan: Donut + angka ────────────────────────
    with right:
        st.markdown("""
        <div class='sec-title'>🥧 Distribusi Ya / Tidak</div>
        """, unsafe_allow_html=True)

        total_ya    = int((df_f[ASPEK] == 1).sum().sum())
        total_tidak = int((df_f[ASPEK] == 2).sum().sum())
        pct_ya_all  = total_ya / (total_ya + total_tidak) * 100

        fig_donut = go.Figure(go.Pie(
            labels=["Ya / Puas", "Tidak / Kurang"],
            values=[total_ya, total_tidak],
            hole=0.65,
            marker=dict(
                colors=[C_HIJAU, C_MERAH],
                line=dict(color="#0d1117", width=3),
            ),
            textinfo="percent",
            textfont=dict(size=12, color="white"),
            hovertemplate="<b>%{label}</b><br>%{value} jawaban<br>%{percent}<extra></extra>",
        ))
        fig_donut.update_layout(
            showlegend=False,
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=0, l=0, r=0),
            annotations=[dict(
                text=f"<b>{pct_ya_all:.0f}%</b><br>Puas",
                x=0.5, y=0.5,
                font=dict(size=20, color="#f1f5f9"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True,
                        config={"displayModeBar": False})

        # Kotak angka
        st.markdown(f"""
        <div style='display:flex; gap:10px; margin-top:-8px;'>
            <div style='flex:1; background:#0d2818; border:1px solid #166534;
                        border-radius:14px; padding:14px; text-align:center;'>
                <div style='font-size:1.7rem; font-weight:800; color:#4ade80;'>{total_ya}</div>
                <div style='font-size:0.72rem; color:#86efac; font-weight:600;
                            margin-top:3px;'>✅ Jawaban Ya</div>
            </div>
            <div style='flex:1; background:#1c0a0a; border:1px solid #991b1b;
                        border-radius:14px; padding:14px; text-align:center;'>
                <div style='font-size:1.7rem; font-weight:800; color:#f87171;'>{total_tidak}</div>
                <div style='font-size:0.72rem; color:#fca5a5; font-weight:600;
                            margin-top:3px;'>❌ Jawaban Tidak</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Heat map ─────────────────────────────────────
    st.markdown("""
    <div class='sec-title' style='margin-top:32px;'>🌡️ Peta Kepuasan — Kelas × Aspek</div>
    <div style='font-size:0.78rem; color:#475569; margin-bottom:12px;'>
        Angka menunjukkan persentase mahasiswa yang menjawab <b style='color:#4ade80'>Ya / Puas</b>.
        Warna <b style='color:#ef4444'>merah</b> = rendah &nbsp;→&nbsp;
        <b style='color:#eab308'>kuning</b> = sedang &nbsp;→&nbsp;
        <b style='color:#22c55e'>hijau</b> = tinggi.
    </div>
    """, unsafe_allow_html=True)

    heat_data  = df_f.groupby("Kelas")[ASPEK].apply(lambda g: (g == 1).mean() * 100)
    xlabels    = [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK]

    fig_heat = px.imshow(
        heat_data.values,
        x=xlabels,
        y=heat_data.index.tolist(),
        color_continuous_scale=[[0, C_MERAH], [0.5, C_KUNING], [1, C_HIJAU]],
        zmin=0, zmax=100,
        text_auto=".0f",
        aspect="auto",
        height=200,
    )
    fig_heat.update_traces(
        textfont=dict(size=15, color="white", family="Inter"),
        hovertemplate="<b>%{y}</b> — %{x}<br>%{z:.1f}% Puas<extra></extra>",
    )
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        coloraxis_showscale=False,
        xaxis=dict(tickfont=dict(size=11, color="#94a3b8"), tickangle=-10),
        yaxis=dict(tickfont=dict(size=13, color="#e2e8f0")),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────
# TAB 2 — DETAIL PER ASPEK
# ─────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class='sec-title'>🔍 Pilih Aspek Fasilitas</div>
    """, unsafe_allow_html=True)

    opts = [f"{ASPEK_INFO[a]['icon']}  {a}" for a in ASPEK]
    sel  = st.selectbox("", opts, label_visibility="collapsed")
    selected = sel.split("  ", 1)[1]

    pct_ya    = (df_f[selected] == 1).mean() * 100
    n_ya      = int((df_f[selected] == 1).sum())
    n_tidak   = int((df_f[selected] == 2).sum())
    color_s, status_s = warna_pct(pct_ya)

    # Info card aspek
    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1e2d4a;
                border-left:4px solid {color_s};
                border-radius:16px; padding:20px 24px; margin-bottom:20px;'>
        <div style='display:flex; align-items:flex-start; gap:16px;'>
            <div style='font-size:2.5rem; line-height:1;'>{ASPEK_INFO[selected]['icon']}</div>
            <div style='flex:1;'>
                <div style='font-size:1.05rem; font-weight:700; color:#f1f5f9; margin-bottom:4px;'>
                    {selected}
                </div>
                <div style='font-size:0.82rem; color:#64748b; margin-bottom:10px;'>
                    {ASPEK_INFO[selected]['desc']}
                </div>
                <div style='font-size:0.88rem; font-weight:700; color:{color_s};'>
                    {status_s}
                </div>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:2.5rem; font-weight:900; color:{color_s}; line-height:1;'>
                    {pct_ya:.1f}%
                </div>
                <div style='font-size:0.72rem; color:#475569; margin-top:4px;'>
                    {n_ya} Ya &nbsp;/&nbsp; {n_tidak} Tidak
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("<div class='card-title'>Perbandingan Ya vs Tidak</div>",
                    unsafe_allow_html=True)
        fig_b = go.Figure(go.Bar(
            x=["✅ Ya / Puas", "❌ Tidak / Kurang"],
            y=[n_ya, n_tidak],
            marker=dict(
                color=[C_HIJAU, C_MERAH],
                line=dict(color="#0d1117", width=2),
            ),
            text=[f"<b>{n_ya}</b><br>{pct_ya:.0f}%",
                  f"<b>{n_tidak}</b><br>{100-pct_ya:.0f}%"],
            textposition="outside",
            textfont=dict(size=13),
            width=[0.45, 0.45],
        ))
        fig_b.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=30, b=20),
            showlegend=False,
            font=dict(color="#94a3b8"),
            yaxis=dict(
                showgrid=True, gridcolor="#1e2d4a",
                range=[0, max(n_ya, n_tidak) * 1.3],
                tickfont=dict(color="#64748b"),
            ),
            xaxis=dict(tickfont=dict(size=13, color="#e2e8f0")),
        )
        st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown("<div class='card-title'>Breakdown Per Kelas</div>",
                    unsafe_allow_html=True)
        rows = []
        for k in sorted(df["Kelas"].unique()):
            sub = df_f[df_f["Kelas"] == k]
            if not len(sub): continue
            ny = int((sub[selected] == 1).sum())
            nt = int((sub[selected] == 2).sum())
            rows.append({"Kelas": k, "Ya": ny, "Tidak": nt,
                          "pct": ny / len(sub) * 100 if len(sub) else 0})
        bd = pd.DataFrame(rows)

        if len(bd):
            fig_k = go.Figure()
            fig_k.add_trace(go.Bar(
                name="✅ Ya", x=bd["Kelas"], y=bd["Ya"],
                marker=dict(color=C_HIJAU, line=dict(color="#0d1117", width=1)),
                text=bd["Ya"], textposition="auto",
                textfont=dict(color="white", size=12),
            ))
            fig_k.add_trace(go.Bar(
                name="❌ Tidak", x=bd["Kelas"], y=bd["Tidak"],
                marker=dict(color=C_MERAH, line=dict(color="#0d1117", width=1)),
                text=bd["Tidak"], textposition="auto",
                textfont=dict(color="white", size=12),
            ))
            fig_k.update_layout(
                barmode="group", height=320,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=20),
                font=dict(color="#94a3b8"),
                legend=dict(orientation="h", y=-0.18,
                            font=dict(size=11, color="#94a3b8"),
                            bgcolor="rgba(0,0,0,0)"),
                yaxis=dict(showgrid=True, gridcolor="#1e2d4a",
                           tickfont=dict(color="#64748b")),
                xaxis=dict(tickfont=dict(size=13, color="#e2e8f0")),
            )
            st.plotly_chart(fig_k, use_container_width=True, config={"displayModeBar": False})

    # Tabel ringkasan
    if len(bd):
        bd["% Puas"] = bd["pct"].apply(lambda x: f"{x:.1f}%")
        bd["Status"] = bd["pct"].apply(lambda x: warna_pct(x)[1])
        st.dataframe(
            bd[["Kelas", "Ya", "Tidak", "% Puas", "Status"]],
            use_container_width=True, hide_index=True
        )


# ─────────────────────────────────────────────────────
# TAB 3 — PERBANDINGAN KELAS
# ─────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class='sec-title'>🏆 Ringkasan Per Kelas</div>
    """, unsafe_allow_html=True)

    kelas_list = sorted(df["Kelas"].unique())
    cols_k = st.columns(len(kelas_list), gap="medium")
    for col, k in zip(cols_k, kelas_list):
        sub  = df[df["Kelas"] == k]
        avg_k = (sub[ASPEK] == 1).mean().mean() * 100
        best  = (sub[ASPEK] == 1).mean().idxmax()
        worst = (sub[ASPEK] == 1).mean().idxmin()
        w = WARNA_KELAS.get(k, "#64748b")
        c, st_txt = warna_pct(avg_k)
        with col:
            st.markdown(f"""
            <div style='background:#111827; border:1px solid #1e2d4a;
                        border-top:4px solid {w}; border-radius:16px;
                        padding:20px 16px; text-align:center;'>
                <div style='font-size:0.72rem; font-weight:700; color:{w};
                            text-transform:uppercase; letter-spacing:1px;'>
                    Kelas {k}
                </div>
                <div style='font-size:2.4rem; font-weight:900; color:#f1f5f9;
                            margin:10px 0 4px; line-height:1;'>
                    {avg_k:.1f}%
                </div>
                <div style='font-size:0.72rem; font-weight:700; color:{c};
                            margin-bottom:12px;'>{st_txt}</div>
                <div style='font-size:0.72rem; color:#475569; text-align:left;
                            background:#0d1117; border-radius:10px; padding:10px 12px;'>
                    <div style='margin-bottom:5px;'>
                        👥 <b style='color:#94a3b8;'>{len(sub)}</b> mahasiswa
                    </div>
                    <div style='margin-bottom:5px;'>
                        ⭐ Terbaik:<br>
                        <b style='color:#4ade80;'>{ASPEK_INFO[best]['icon']} {best}</b>
                    </div>
                    <div>
                        ⚠️ Perhatian:<br>
                        <b style='color:#f87171;'>{ASPEK_INFO[worst]['icon']} {worst}</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Grouped bar
    st.markdown("""
    <div class='sec-title' style='margin-top:32px;'>📊 Perbandingan Per Aspek Fasilitas</div>
    """, unsafe_allow_html=True)

    rows = []
    for k in kelas_list:
        sub = df[df["Kelas"] == k]
        for a in ASPEK:
            rows.append({
                "Kelas": k,
                "Aspek": f"{ASPEK_INFO[a]['icon']} {a}",
                "% Puas": (sub[a] == 1).mean() * 100,
            })
    comp_df = pd.DataFrame(rows)

    fig_grp = px.bar(
        comp_df, x="Aspek", y="% Puas", color="Kelas",
        barmode="group", height=420,
        color_discrete_map=WARNA_KELAS,
        text=comp_df["% Puas"].apply(lambda x: f"{x:.0f}%"),
    )
    fig_grp.update_traces(textposition="outside",
                          textfont=dict(size=11, color="white"))
    fig_grp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(tickangle=-15, tickfont=dict(size=11, color="#94a3b8"),
                   gridcolor="#1e2d4a"),
        yaxis=dict(range=[0, 125], showgrid=True, gridcolor="#1e2d4a",
                   tickfont=dict(color="#64748b"), title="% Mahasiswa Puas",
                   title_font=dict(color="#64748b")),
        margin=dict(t=30, b=100, l=10, r=10),
        legend=dict(orientation="h", y=-0.22,
                    font=dict(size=12, color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)", title_text=""),
    )
    st.plotly_chart(fig_grp, use_container_width=True, config={"displayModeBar": False})

    # Radar
    st.markdown("""
    <div class='sec-title'>🕸️ Radar Chart — Profil Kepuasan Tiap Kelas</div>
    <div style='font-size:0.78rem; color:#475569; margin-bottom:14px;'>
        Semakin luas area, semakin tinggi tingkat kepuasan kelas tersebut di semua aspek.
    </div>
    """, unsafe_allow_html=True)

    rlabels = [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK]
    fig_r = go.Figure()
    for k in kelas_list:
        sub  = df[df["Kelas"] == k]
        vals = [(sub[a] == 1).mean() * 100 for a in ASPEK]
        w    = WARNA_KELAS.get(k, "#64748b")
        fig_r.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=rlabels + [rlabels[0]],
            fill="toself", name=f"Kelas {k}",
            line=dict(color=w, width=2.5),
            fillcolor=w, opacity=0.18,
            hovertemplate="%{theta}<br><b>%{r:.1f}%</b><extra>Kelas " + k + "</extra>",
        ))
    fig_r.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 105],
                tickvals=[25, 50, 75, 100],
                ticktext=["25%", "50%", "75%", "100%"],
                tickfont=dict(size=10, color="#475569"),
                gridcolor="#1e2d4a", linecolor="#1e2d4a",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#94a3b8"),
                linecolor="#1e2d4a", gridcolor="#1e2d4a",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        height=460,
        legend=dict(orientation="h", y=-0.1,
                    font=dict(size=12, color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=60, l=50, r=50),
    )
    st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────
# TAB 4 — DATA LENGKAP
# ─────────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div class='sec-title'>📋 Data Jawaban Responden</div>
    """, unsafe_allow_html=True)

    show = df_f.copy()
    for a in ASPEK:
        show[a] = show[a].map({1: "✅ Ya", 2: "❌ Tidak"})
    show["Timestamp"] = show["Timestamp"].dt.strftime("%d %b %Y, %H:%M")
    rename_map = {a: f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK}
    show = show.rename(columns=rename_map)

    st.dataframe(show, use_container_width=True, height=380, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    dl1, dl2, _ = st.columns([1, 1, 2])
    with dl1:
        st.download_button(
            "⬇️ Download Data (CSV)", df_f.to_csv(index=False).encode("utf-8"),
            "data_survei.csv", "text/csv", use_container_width=True,
        )
    with dl2:
        smry = pd.DataFrame({
            "Aspek": [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK],
            "Ya": [(df_f[a] == 1).sum() for a in ASPEK],
            "Tidak": [(df_f[a] == 2).sum() for a in ASPEK],
            "% Puas": [f"{(df_f[a]==1).mean()*100:.1f}%" for a in ASPEK],
            "Status": [warna_pct((df_f[a]==1).mean()*100)[1] for a in ASPEK],
        })
        st.download_button(
            "⬇️ Download Ringkasan (CSV)", smry.to_csv(index=False).encode("utf-8"),
            "ringkasan_survei.csv", "text/csv", use_container_width=True,
        )

    st.markdown("""
    <div class='sec-title' style='margin-top:28px;'>📊 Tabel Ringkasan Statistik</div>
    """, unsafe_allow_html=True)
    st.dataframe(smry, use_container_width=True, hide_index=True)
