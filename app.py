import pandas as pd
import streamlit as st

# ============================
# Load data
# ============================
df = pd.read_excel("ACEH_dengan_Tahun_Bulan_Hari.xlsx", sheet_name="Sheet1")

# Pastikan nama kolom bersih dan huruf kecil semua
df.columns = df.columns.str.strip().str.lower()

# Cek kolom penting
required_columns = {"tahun", "bulan", "rr", "tavg", "tx", "tn", "tekanan"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"❌ Kolom berikut tidak ditemukan di data: {missing_columns}")
    st.stop()

# ============================
# Konversi bulan ke nama
# ============================
bulan_dict = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
}
df["bulan_nama"] = df["bulan"].map(bulan_dict)

# ============================
# Sidebar
# ============================
st.sidebar.title("Filter Data")
tahun_terpilih = st.sidebar.selectbox("Pilih Tahun", sorted(df["tahun"].unique()))
variabel = st.sidebar.selectbox("Pilih Variabel", ["rr", "tavg", "tx", "tn", "tekanan"])

# ============================
# Filter data sesuai pilihan
# ============================
data_tahun = df[df["tahun"] == tahun_terpilih]

# ============================
# Judul & Visualisasi
# ============================
st.title("📊 Dashboard Iklim Bulanan - ACEH")
st.subheader(f"📈 Visualisasi {variabel.upper()} Tahun {tahun_terpilih}")
st.line_chart(data_tahun.set_index("bulan_nama")[variabel])

# ============================
# Statistik ringkas
# ============================
st.write("### 📌 Statistik Ringkas")
st.write(data_tahun[variabel].describe().to_frame())

# ============================
# Unduh data
# ============================
csv = data_tahun.to_csv(index=False)
st.download_button("📥 Unduh Data Tahun Ini", csv, file_name=f"Data_ACEH{tahun_terpilih}.csv")
