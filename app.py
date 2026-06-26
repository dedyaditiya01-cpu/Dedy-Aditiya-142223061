import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Survei Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Background & main */
    .stApp { background-color: #f0f4ff; }
    section[data-testid="stSidebar"] { background-color: #1a237e; }
    section[data-testid="stSidebar"] * { color: white !important; }
    section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 22px 20px 16px;
        box-shadow: 0 2px 12px rgba(26,35,126,.10);
        text-align: center;
        border-left: 5px solid #3949ab;
    }
    .metric-card h2 { font-size: 2.2rem; color: #1a237e; margin: 0; font-weight: 700; }
    .metric-card p  { color: #555; margin: 4px 0 0; font-size: .9rem; }

    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        margin: 24px 0 14px;
        font-size: 1.05rem;
        font-weight: 600;
    }

    /* Table */
    .dataframe thead th { background: #1a237e !important; color: white !important; }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
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
    # Recode: 1 = Ya / Puas, 2 = Tidak / Kurang
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()
PERTANYAAN = df.columns[4:].tolist()
LABEL = {1: "Ya / Puas ✅", 2: "Tidak / Kurang ❌"}
WARNA  = {"Ya / Puas ✅": "#43a047", "Tidak / Kurang ❌": "#e53935"}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Survei Kepuasan\nMahasiswa Teknik Industri")
    st.divider()
    kelas_list = ["Semua Kelas"] + sorted(df["Kelas"].unique().tolist())
    kelas_filter = st.selectbox("📚 Filter Kelas", kelas_list)
    st.divider()
    st.markdown("### 📊 Statistik Cepat")
    df_f = df if kelas_filter == "Semua Kelas" else df[df["Kelas"] == kelas_filter]
    st.metric("Total Responden", len(df_f))
    avg_puas = (df_f[PERTANYAAN] == 1).mean().mean() * 100
    st.metric("Rata-rata Kepuasan", f"{avg_puas:.1f}%")
    st.divider()
    st.caption("Data: Google Form Survey\nTeknik Industri — 2026")

df_f = df if kelas_filter == "Semua Kelas" else df[df["Kelas"] == kelas_filter]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#1a237e,#3949ab);padding:28px 30px;border-radius:16px;
            margin-bottom:20px;color:white;'>
  <h1 style='margin:0;font-size:1.9rem;'>📋 Dashboard Survei Kepuasan Mahasiswa</h1>
  <p style='margin:6px 0 0;opacity:.85;'>Program Studi Teknik Industri &nbsp;|&nbsp; Fasilitas Ruang Kelas</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
cols = st.columns(4)
kpi_data = [
    ("👥", len(df_f), "Total Responden"),
    ("🏫", df_f["Kelas"].nunique(), "Jumlah Kelas"),
    (f"✅", f"{avg_puas:.1f}%", "Tingkat Kepuasan"),
    ("📅", df_f["Timestamp"].dt.date.nunique(), "Hari Pengisian"),
]
for col, (icon, val, label) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
          <div style='font-size:1.8rem'>{icon}</div>
          <h2>{val}</h2>
          <p>{label}</p>
        </div>""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Ringkasan", "📈 Per Pertanyaan", "🏫 Per Kelas", "📋 Data Mentah"]
)

# ─── Tab 1: Ringkasan ─────────────────────────────────────────────────────────
with tab1:
    st.markdown("<div class='section-header'>📊 Persentase Kepuasan Per Aspek</div>",
                unsafe_allow_html=True)

    pct_puas = (df_f[PERTANYAAN] == 1).mean() * 100
    bar_df = pd.DataFrame({"Aspek": PERTANYAAN, "% Puas": pct_puas.values})
    bar_df = bar_df.sort_values("% Puas")

    fig_bar = px.bar(
        bar_df, x="% Puas", y="Aspek", orientation="h",
        color="% Puas",
        color_continuous_scale=["#e53935", "#ffb300", "#43a047"],
        range_color=[0, 100],
        text=bar_df["% Puas"].apply(lambda x: f"{x:.1f}%"),
        height=420,
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        margin=dict(l=10, r=60, t=20, b=20),
        coloraxis_showscale=False,
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 115], showgrid=True, gridcolor="#eee"),
        yaxis=dict(tickfont=dict(size=12)),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Donut keseluruhan
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-header'>🥧 Distribusi Kepuasan Keseluruhan</div>",
                    unsafe_allow_html=True)
        total_yes = int((df_f[PERTANYAAN] == 1).sum().sum())
        total_no  = int((df_f[PERTANYAAN] == 2).sum().sum())
        fig_pie = go.Figure(go.Pie(
            labels=["Ya / Puas ✅", "Tidak / Kurang ❌"],
            values=[total_yes, total_no],
            hole=0.55,
            marker_colors=["#43a047", "#e53935"],
            textinfo="label+percent",
            hoverinfo="label+value",
        ))
        fig_pie.update_layout(
            showlegend=False, height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10),
            annotations=[dict(text=f"<b>{avg_puas:.0f}%</b><br>Puas",
                              x=0.5, y=0.5, font_size=18,
                              showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.markdown("<div class='section-header'>🌡️ Heat Map Kepuasan per Kelas</div>",
                    unsafe_allow_html=True)
        heat_df = df_f.groupby("Kelas")[PERTANYAAN].apply(
            lambda g: (g == 1).mean() * 100
        )
        short = [p[:18]+"…" if len(p) > 18 else p for p in PERTANYAAN]
        fig_heat = px.imshow(
            heat_df.values,
            x=short, y=heat_df.index.tolist(),
            color_continuous_scale=["#e53935", "#ffb300", "#43a047"],
            zmin=0, zmax=100,
            text_auto=".0f",
            aspect="auto", height=320,
        )
        fig_heat.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

# ─── Tab 2: Per Pertanyaan ────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-header'>📈 Detail Jawaban Per Pertanyaan</div>",
                unsafe_allow_html=True)
    selected_q = st.selectbox("Pilih pertanyaan:", PERTANYAAN)

    counts = df_f[selected_q].map(LABEL).value_counts().reset_index()
    counts.columns = ["Jawaban", "Jumlah"]
    counts["Persen"] = (counts["Jumlah"] / counts["Jumlah"].sum() * 100).round(1)

    c1, c2 = st.columns([1, 1])
    with c1:
        fig_d = px.pie(
            counts, names="Jawaban", values="Jumlah",
            color="Jawaban", color_discrete_map=WARNA,
            hole=0.5, height=300,
        )
        fig_d.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10))
        st.plotly_chart(fig_d, use_container_width=True)

    with c2:
        # Stacked bar per kelas untuk pertanyaan ini
        kelas_q = df_f.groupby("Kelas")[selected_q].apply(
            lambda s: s.map(LABEL).value_counts(normalize=True).mul(100)
        ).unstack(fill_value=0).reset_index()
        fig_k = px.bar(
            kelas_q.melt(id_vars="Kelas", value_name="Persen", var_name="Jawaban"),
            x="Kelas", y="Persen", color="Jawaban",
            color_discrete_map=WARNA, barmode="stack", height=300,
            text_auto=".1f",
        )
        fig_k.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white",
            legend=dict(orientation="h", y=-0.25),
            margin=dict(t=10, b=10), yaxis_title="% Responden",
        )
        st.plotly_chart(fig_k, use_container_width=True)

    st.dataframe(counts, use_container_width=True, hide_index=True)

# ─── Tab 3: Per Kelas ─────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-header'>🏫 Perbandingan Kepuasan Antar Kelas</div>",
                unsafe_allow_html=True)

    kelas_avg = df_f.groupby("Kelas")[PERTANYAAN].apply(
        lambda g: (g == 1).mean() * 100
    ).reset_index()
    kelas_long = kelas_avg.melt(id_vars="Kelas", var_name="Aspek", value_name="% Puas")

    fig_grp = px.bar(
        kelas_long, x="Aspek", y="% Puas", color="Kelas",
        barmode="group", height=420,
        color_discrete_sequence=["#1a237e", "#43a047", "#e53935"],
    )
    fig_grp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white",
        xaxis_tickangle=-30, xaxis=dict(tickfont=dict(size=10)),
        margin=dict(t=10, b=120, l=10, r=10),
        legend_title="Kelas",
    )
    st.plotly_chart(fig_grp, use_container_width=True)

    # Radar chart per kelas
    st.markdown("<div class='section-header'>🕸️ Radar Chart Kepuasan Per Kelas</div>",
                unsafe_allow_html=True)
    fig_radar = go.Figure()
    colors_r = ["#1a237e", "#43a047", "#e53935"]
    short_labels = [p.split(" ")[:3] for p in PERTANYAAN]
    short_labels = [" ".join(w) for w in short_labels]

    for i, kelas in enumerate(df_f["Kelas"].unique()):
        vals = (df_f[df_f["Kelas"] == kelas][PERTANYAAN] == 1).mean() * 100
        fig_radar.add_trace(go.Scatterpolar(
            r=list(vals) + [vals.iloc[0]],
            theta=short_labels + [short_labels[0]],
            fill="toself", name=kelas,
            line_color=colors_r[i % 3],
            opacity=0.7,
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
        height=420, paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.1),
        margin=dict(t=20, b=60),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ─── Tab 4: Data Mentah ───────────────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-header'>📋 Tabel Data Responden</div>",
                unsafe_allow_html=True)

    show_df = df_f.copy()
    for col in PERTANYAAN:
        show_df[col] = show_df[col].map({1: "✅ Ya", 2: "❌ Tidak"})
    show_df["Timestamp"] = show_df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M")

    st.dataframe(show_df, use_container_width=True, height=420)

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "survei_kepuasan.csv", "text/csv")
