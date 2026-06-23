import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import numpy as np

# Set page config
st.set_page_config(page_title="Survey Personality", layout="wide")

# Data dari Flask
DATA = [
  {
    "Timestamp": "2026-04-14 13:14:19.805000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "20–25 tahun",
    "  Jenis kelamin  ": "Perempuan",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya cepat frustrasi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Baru mulai mengerjakan",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 14:56:40.886000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "26–30 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya langsung mengerjakan",
    "Waktu luang  ": "Digunakan untuk hal produktif",
    "Mendekati deadline  ": "Sudah selesai sebelumnya",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 14:58:19.970000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "20–25 tahun",
    "  Jenis kelamin  ": "Perempuan",
    "Saat menghadapi masalah  ": "Saya mudah emosi",
    "Jika ada orang melakukan kesalahan  ": "Saya langsung kesal/marah",
    "Ketika rencana gagal  ": "Saya cepat frustrasi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Sudah selesai sebelumnya",
    "Saat menghadapi kesulitan  ": "Saya cenderung menyerah",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 14:58:28.738000",
    "Status Anda saat ini": "Keduanya",
    "  Usia  ": "26–30 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya mudah emosi",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Baru mulai mengerjakan",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 14:58:48.829000",
    "Status Anda saat ini": "Pekerja",
    "  Usia  ": "20–25 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya langsung kesal/marah",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Baru mulai mengerjakan",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya merasa kewalahan dan berhenti"
  },
  {
    "Timestamp": "2026-04-14 16:00:33.441000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "20–25 tahun",
    "  Jenis kelamin  ": "Perempuan",
    "Saat menghadapi masalah  ": "Saya mudah emosi",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya langsung mengerjakan",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Sudah selesai sebelumnya",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 16:01:40.927000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "< 20 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Baru mulai mengerjakan",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 16:02:00.122000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "20–25 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Sudah selesai sebelumnya",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
  {
    "Timestamp": "2026-04-14 16:08:14.484000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "20–25 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya langsung kesal/marah",
    "Ketika rencana gagal  ": "Saya cepat frustrasi",
    "Ketika ada tugas": "Saya sering menunda",
    "Waktu luang  ": "Lebih banyak digunakan untuk santai",
    "Mendekati deadline  ": "Baru mulai mengerjakan",
    "Saat menghadapi kesulitan  ": "Saya cenderung menyerah",
    "Beban kerja/tugas banyak  ": "Saya merasa kewalahan dan berhenti"
  },
  {
    "Timestamp": "2026-04-14 17:27:54.394000",
    "Status Anda saat ini": "Mahasiswa",
    "  Usia  ": "< 20 tahun",
    "  Jenis kelamin  ": "Laki-laki",
    "Saat menghadapi masalah  ": "Saya tetap tenang",
    "Jika ada orang melakukan kesalahan  ": "Saya mencoba memahami dulu",
    "Ketika rencana gagal  ": "Saya mencari solusi",
    "Ketika ada tugas": "Saya langsung mengerjakan",
    "Waktu luang  ": "Digunakan untuk hal produktif",
    "Mendekati deadline  ": "Sudah selesai sebelumnya",
    "Saat menghadapi kesulitan  ": "Saya terus mencoba",
    "Beban kerja/tugas banyak  ": "Saya tetap berusaha menyelesaikan"
  },
]

# Filter data (hanya yang valid)
def filter_valid_data(data):
    valid_data = []
    for item in data:
        if item.get("Timestamp") and item.get("Status Anda saat ini"):
            valid_data.append(item)
    return valid_data

valid_data = filter_valid_data(DATA)
df = pd.DataFrame(valid_data)

# Cleanup column names
df.columns = df.columns.str.strip()

# Header
st.title("📊 Analisis Survey Personality")
st.markdown("---")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Responden", len(df))
with col2:
    st.metric("Laki-laki", len(df[df["Jenis kelamin"] == "Laki-laki"]))
with col3:
    st.metric("Perempuan", len(df[df["Jenis kelamin"] == "Perempuan"]))
with col4:
    status_counts = df["Status Anda saat ini"].value_counts()
    st.metric("Mahasiswa", status_counts.get("Mahasiswa", 0))

st.markdown("---")

# Tab Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Dashboard", "👥 Demografi", "💭 Personality", "🔍 Detail Data", "📊 Statistik"])

# TAB 1: Dashboard
with tab1:
    st.subheader("Overview Responden")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status Distribution
        status_data = df["Status Anda saat ini"].value_counts()
        fig_status = px.pie(values=status_data.values, names=status_data.index, 
                           title="Distribusi Status",
                           color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Gender Distribution
        gender_data = df["Jenis kelamin"].value_counts()
        fig_gender = px.bar(x=gender_data.index, y=gender_data.values,
                           title="Distribusi Jenis Kelamin",
                           labels={"x": "Jenis Kelamin", "y": "Jumlah"},
                           color=gender_data.index,
                           color_discrete_sequence=["#FF6B9D", "#4A90E2"])
        st.plotly_chart(fig_gender, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Age Distribution
        age_order = ["< 20 tahun", "20–25 tahun", "26–30 tahun", "30 tahun >"]
        age_data = df["Usia"].value_counts().reindex(age_order, fill_value=0)
        fig_age = px.bar(x=age_data.index, y=age_data.values,
                        title="Distribusi Usia",
                        labels={"x": "Usia", "y": "Jumlah"},
                        color_discrete_sequence=["#FF6B9D"])
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col4:
        # Status x Gender
        cross_tab = pd.crosstab(df["Status Anda saat ini"], df["Jenis kelamin"])
        fig_cross = px.bar(cross_tab, title="Status vs Jenis Kelamin",
                          barmode="group",
                          color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_cross, use_container_width=True)

# TAB 2: Demografi
with tab2:
    st.subheader("Analisis Demografi")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Filter Data")
        selected_status = st.multiselect("Status", df["Status Anda saat ini"].unique(), 
                                        default=df["Status Anda saat ini"].unique())
        selected_gender = st.multiselect("Jenis Kelamin", df["Jenis kelamin"].unique(),
                                       default=df["Jenis kelamin"].unique())
        
        filtered_df = df[(df["Status Anda saat ini"].isin(selected_status)) & 
                        (df["Jenis kelamin"].isin(selected_gender))]
    
    with col2:
        st.write("### Statistik Terpilih")
        st.metric("Total", len(filtered_df))
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Laki-laki", len(filtered_df[filtered_df["Jenis kelamin"] == "Laki-laki"]))
        with col_b:
            st.metric("Perempuan", len(filtered_df[filtered_df["Jenis kelamin"] == "Perempuan"]))
        with col_c:
            st.metric("Mahasiswa", len(filtered_df[filtered_df["Status Anda saat ini"] == "Mahasiswa"]))
    
    st.markdown("---")
    
    # Age-Gender Cross Tab
    age_gender = pd.crosstab(filtered_df["Usia"], filtered_df["Jenis kelamin"])
    fig_age_gender = px.bar(age_gender, title="Usia by Jenis Kelamin",
                           barmode="group",
                           color_discrete_sequence=["#FF6B9D", "#4A90E2"])
    st.plotly_chart(fig_age_gender, use_container_width=True)

# TAB 3: Personality
with tab3:
    st.subheader("Analisis Personality Traits")
    
    personality_questions = [
        "Saat menghadapi masalah",
        "Jika ada orang melakukan kesalahan",
        "Ketika rencana gagal",
        "Ketika ada tugas",
        "Waktu luang",
        "Mendekati deadline",
        "Saat menghadapi kesulitan",
        "Beban kerja/tugas banyak"
    ]
    
    selected_question = st.selectbox("Pilih Pertanyaan", personality_questions)
    
    if selected_question:
        # Count responses
        response_counts = df[selected_question].value_counts().sort_values(ascending=True)
        
        fig = px.barh(x=response_counts.values, y=response_counts.index,
                     title=f"Respons: {selected_question}",
                     labels={"x": "Jumlah Responden", "y": "Respons"},
                     color=response_counts.values,
                     color_continuous_scale="Viridis")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show percentage
        st.write("### Persentase Respons")
        percentages = (response_counts / len(df) * 100).round(2)
        for resp, pct in percentages.items():
            st.write(f"- **{resp}**: {pct}%")
    
    st.markdown("---")
    
    # Comparison between groups
    st.subheader("Perbandingan antar Kelompok")
    
    col1, col2 = st.columns(2)
    with col1:
        group_by = st.selectbox("Group By", ["Status Anda saat ini", "Jenis kelamin", "Usia"])
    with col2:
        compare_question = st.selectbox("Pertanyaan", personality_questions, key="compare_q")
    
    if group_by and compare_question:
        cross_tab = pd.crosstab(df[group_by], df[compare_question])
        fig_comp = px.bar(cross_tab, title=f"{compare_question} by {group_by}",
                         barmode="group")
        st.plotly_chart(fig_comp, use_container_width=True)

# TAB 4: Detail Data
with tab4:
    st.subheader("Data Detail Responden")
    
    col1, col2 = st.columns(2)
    with col1:
        search_status = st.multiselect("Filter Status", df["Status Anda saat ini"].unique(),
                                      default=df["Status Anda saat ini"].unique(), key="search_status")
    with col2:
        search_gender = st.multiselect("Filter Jenis Kelamin", df["Jenis kelamin"].unique(),
                                      default=df["Jenis kelamin"].unique(), key="search_gender")
    
    filtered_display = df[(df["Status Anda saat ini"].isin(search_status)) &
                         (df["Jenis kelamin"].isin(search_gender))]
    
    st.dataframe(filtered_display, use_container_width=True, height=400)
    
    # Download data
    csv = filtered_display.to_csv(index=False)
    st.download_button(label="📥 Download CSV", data=csv, file_name="survey_data.csv", mime="text/csv")

# TAB 5: Statistik
with tab5:
    st.subheader("Statistik Lanjutan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Statistik Status")
        status_stats = df["Status Anda saat ini"].value_counts()
        st.bar_chart(status_stats)
    
    with col2:
        st.write("### Statistik Usia")
        age_order = ["< 20 tahun", "20–25 tahun", "26–30 tahun", "30 tahun >"]
        age_stats = df["Usia"].value_counts().reindex(age_order, fill_value=0)
        st.bar_chart(age_stats)
    
    st.markdown("---")
    
    st.write("### Personality Trait Summary")
    
    personality_questions = [
        "Saat menghadapi masalah",
        "Jika ada orang melakukan kesalahan",
        "Ketika rencana gagal",
        "Ketika ada tugas",
        "Waktu luang",
        "Mendekati deadline",
        "Saat menghadapi kesulitan",
        "Beban kerja/tugas banyak"
    ]
    
    for question in personality_questions:
        top_response = df[question].value_counts().head(1)
        if len(top_response) > 0:
            response = top_response.index[0]
            count = top_response.values[0]
            pct = (count / len(df) * 100)
            st.write(f"**{question}**: {response} ({pct:.1f}%)")

st.markdown("---")
st.caption("📊 Dashboard Survei Personality | Data Survey Perilaku dan Kepribadian")