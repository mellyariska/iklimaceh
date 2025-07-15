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


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# BACA DATA
# =====================
data = pd.read_excel("ACEH_dengan_Tahun_Bulan_Hari.xlsx")


# =====================
# HEADER
# =====================
st.title("🌦️ Dashboard Analisis Iklim Aceh")
st.markdown("Visualisasi data iklim tahunan berdasarkan parameter suhu, curah hujan, kelembaban, angin, dan radiasi matahari.")

# =====================
# TABEL DATA
# =====================
st.subheader("📄 Data Iklim")
st.dataframe(data)

# =====================
# SUHU
# =====================
st.subheader("🌡️ Tren Suhu Rata-rata Tahunan")
st.line_chart(data.set_index("Tahun")["Tavg"])

# =====================
# CURAH HUJAN
# =====================
st.subheader("🌧️ Curah Hujan Tahunan")
st.bar_chart(data.set_index("Tahun")["RR"])

# =====================
# RENTANG SUHU
# =====================
st.subheader("📉 Rentang Suhu Tahunan (Max - Min)")
data["Rentang_Suhu"] = data["Tx"] - data["Tn"]
st.line_chart(data.set_index("Tahun")["Rentang_Suhu"])

# =====================
# ANOMALI SUHU
# =====================
st.subheader("📈 Anomali Suhu terhadap Rata-rata 1985–2020")
baseline = data[(data["Tahun"] >= 1985) & (data["Tahun"] <= 2020)]["Tavg"].mean()
data["Anomali_Suhu"] = data["Tavg"] - baseline

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(x="Tahun", y="Anomali_Suhu", data=data, palette="coolwarm", ax=ax1)
ax1.axhline(0, color="black", linestyle="--")
ax1.set_ylabel("Anomali (°C)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# =====================
# KORELASI SUHU - HUJAN
# =====================
st.subheader("🔍 Korelasi Suhu vs Curah Hujan")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=data, x="Tavg", y="RR", ax=ax2)
sns.regplot(data=data, x="Tavg", y="RR", scatter=False, ax=ax2, color="red")
st.pyplot(fig2)

# =====================
# RATA-RATA PER DEKADE
# =====================
st.subheader("📊 Rata-rata Suhu & Curah Hujan per Dekade")
data["Dekade"] = (data["Tahun"] // 10) * 10
avg_dekade = data.groupby("Dekade")[["Tavg", "RR"]].mean().round(2)
st.dataframe(avg_dekade)

fig3, ax3 = plt.subplots()
avg_dekade.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Rata-rata")
st.pyplot(fig3)

# =====================
# TAHUN EKSTREM
# =====================
st.subheader("📌 Tahun Ekstrem")
st.markdown(f"""
- 🌡️ **Tahun Terpanas**: {data.loc[data['Tavg'].idxmax()]['Tahun']} ({data['Tavg'].max():.2f} °C)  
- ❄️ **Tahun Terdingin**: {data.loc[data['Tavg'].idxmin()]['Tahun']} ({data['Tavg'].min():.2f} °C)  
- 🌧️ **Hujan Terbanyak**: {data.loc[data['RR'].idxmax()]['Tahun']} ({data['RR'].max():.1f} mm)  
- ☀️ **Hujan Terkering**: {data.loc[data['RR'].idxmin()]['Tahun']} ({data['RR'].min():.1f} mm)
""")


# =====================
# TREN TEKANAN
# =====================
if "kecepatan_angin" in data.columns:
    st.subheader("🍃 Tekanan Tahunan")
    st.line_chart(data.set_index("Tahun")["Tekanan"])

# =====================
# MATRIX KORELASI
# =====================
st.subheader("📌 Korelasi Antar Variabel Iklim")
fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.heatmap(data.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm", ax=ax5)
st.pyplot(fig5)
