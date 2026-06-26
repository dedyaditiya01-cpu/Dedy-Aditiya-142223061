# 📊 Dashboard Survei Kepuasan Mahasiswa

Dashboard interaktif hasil survei kepuasan fasilitas ruang kelas mahasiswa Teknik Industri.

## 🚀 Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## 📦 Cara Menjalankan Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Deploy ke Streamlit Community Cloud
1. Push repo ini ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo → set `app.py` sebagai main file
4. Klik **Deploy!**

## 📁 Struktur Folder
```
├── app.py                  # Aplikasi utama Streamlit
├── requirements.txt        # Dependensi Python
├── data/
│   └── Survei_kepuasan_mahasiswa__Responses_.xlsx
└── README.md
```

## 📋 Fitur
- 🎛️ Filter per kelas (Pagi, Malam A, Malam B)
- 📊 Bar chart kepuasan per aspek
- 🥧 Donut chart distribusi keseluruhan
- 🌡️ Heat map per kelas
- 🕸️ Radar chart perbandingan kelas
- 📋 Tabel data mentah + download CSV
