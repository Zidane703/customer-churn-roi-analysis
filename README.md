<div align="center">
  <h1>📊 Customer Churn & Marketing ROI Analysis</h1>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/SQL-SQLite-lightgrey.svg?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQL" />
    <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-orange.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  </p>

  <p><em>Proyek end-to-end analisis data untuk mengevaluasi karakteristik retensi pelanggan dan mengukur efektivitas finansial dari kampanye pemasaran.</em></p>
</div>

<hr>

## 📌 Project Overview
Proyek ini mengintegrasikan query SQL tingkat lanjut (*Common Table Expressions* & *Window Functions*) dengan manipulasi data menggunakan Python Pandas. Tujuannya adalah menyajikan metrik bisnis yang presisi, terstruktur, dan berbasis data untuk mendukung keputusan strategis dalam upaya menekan angka kehilangan pelanggan (*churn*) serta mengoptimalkan alokasi anggaran pemasaran perusahaan.

---

## 🔬 Research Result

### 1. Breakdown Churn Rate Berdasarkan Lokasi & Channel
Metrik *churn* dihitung secara objektif berdasarkan pengguna yang tidak melakukan aktivitas transaksi selama **lebih dari 60 hari** terhitung dari tanggal *cutting-off* (`2026-06-15`).

<div align="center">
  <img src="reports/churn_rate_table.png" alt="Churn Rate Analysis Table" width="800">
  <br>
  <a href="reports/churn_rate_table.html"><b>📄 Buka Source File: Churn Rate HTML Format</b></a>
</div>
<br>

> **💡 Key Insight:**
> Tingkat kehilangan pelanggan (*Churn Rate*) tertinggi secara agregat terdeteksi di **Surabaya melalui jalur Organic (75.00%)** dan **Bali melalui Google Search (70.83%)**. Hal ini mengindikasikan adanya potensi ketidaksesuaian antara ekspektasi awal pengguna dari channel tersebut dengan kualitas retensi produk, yang memerlukan tinjauan lebih lanjut pada strategi akuisisi.

<br>

### 2. ROI & Performa Kampanye "Retention Promo Q1"
Analisis ini mengukur dampak nyata dari kampanye dengan mengisolasi arus pendapatan (*revenue*) yang murni dihasilkan dari transaksi pengguna **setelah** tanggal pelaksanaan kampanye.

<div align="center">
  <img src="reports/roi_analysis_table.png" alt="ROI Analysis Table" width="800">
  <br>
  <a href="reports/roi_analysis_table.html"><b>📄 Buka Source File: ROI Analysis HTML Format</b></a>
</div>
<br>

> **💡 Key Insight:**
> Kampanye "Retention Promo Q1" mencetak performa yang luar biasa dengan **Success Rate mencapai 81.33%**. Kampanye ini tidak hanya berhasil menyelamatkan mayoritas target pengguna dari risiko churn, tetapi juga memberikan pengembalian investasi (**ROI**) yang sangat positif dan margin keuntungan bersih (*Net Profit*) yang signifikan bagi perusahaan.

---

## 🛠️ Tech Stack & Metodologi
* **Database Engine:** `SQLite` (Manajemen basis data relasional, ekstraksi transaksi, segmentasi user).
* **Data Wrangling:** `pandas` (Pembersihan, agregasi lanjutan, dan pemformatan data tabular).
* **Data Presentation:** `pandas.io.formats.style` terintegrasi dengan HTML/CSS untuk pelaporan data tabular dengan hierarki visual yang tajam.
* **Formulasi Metrik Bisnis:**
  * **Churn Rate (%):** $\frac{\text{Churned Customers}}{\text{Total Customers}} \times 100$
  * **Success Rate (%):** $\frac{\text{Saved Customers}}{\text{Targeted Customers}} \times 100$
  * **Return on Investment (ROI %):** $\frac{\text{Total Revenue Generated} - \text{Total Campaign Cost}}{\text{Total Campaign Cost}} \times 100$

---

## 📁 Struktur Repositori

```text
Customer-Churn-ROI-Analysis/
│
├── data/
│   └── churn_roi_project.db      # Skema relasional dan sumber data utama
├── notebooks/
│   └── churn_roi_analysis.ipynb  # Kode sumber analisis utama (SQL & Python)
├── reports/
│   ├── churn_rate_table.html     # Hasil ekspor tabel Churn (Format HTML)
│   ├── churn_rate_table.png      # Aset visual hasil analisis churn
│   ├── roi_analysis_table.html   # Hasil ekspor tabel ROI (Format HTML)
│   └── roi_analysis_table.png    # Aset visual hasil analisis ROI
└── README.md                     # Dokumentasi portofolio
