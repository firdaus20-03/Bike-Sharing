import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#load dataset nya
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/all_data.csv")
    return df
df = load_data()

# konversi tanggal ke format datetime
df["dteday"] = pd.to_datetime(df["dteday"])

#sidebar
st.sidebar.image('dashboard/bike.jpg')
st.sidebar.header('Muhammad Firdaus_MC211D5Y2137')
st.sidebar.title('Analisis Bike Sharing')
menu = st.sidebar.selectbox("Pilih Analisis", 
                            ["1️⃣ Pengaruh Hari Libur", "2️⃣ Pola Penyewaan per Jam", "3️⃣ RFM Analysis"])

#Pertanyaan 1. Pengaruh Hari Libur terhadap Jumlah Peminjaman Sepeda
if menu == "1️⃣ Pengaruh Hari Libur":
    st.title("📊 Pengaruh Hari Libur terhadap Penyewaan Sepeda")
    holiday_avg = df.groupby("holiday")["cnt"].mean().reset_index()

    # visualisasi nya
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=holiday_avg['holiday'], y=holiday_avg['cnt'], palette=['#1f77b4', '#ff7f0e'], ax=ax)
    plt.xticks([0, 1], ['Hari Biasa', 'Hari Libur'])
    plt.xlabel('Hari')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    plt.title('Pengaruh Hari Libur terhadap Penyewaan Sepeda')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # bagian kesimpulan
    st.write("**📌 Kesimpulan:**")
    st.write("Penyewaan sepeda lebih tinggi pada hari biasa dibandingkan hari libur")
    st.write("Hari libur tetap memiliki penyewaan yang signifikan, kemungkinan untuk rekreasi/olahraga")
    st.write("**Strategi:** Promosi khusus di hari libur untuk meningkatkan penyewaan")

#Pertanyaan 2. Bagaimana pola penyewaan sepeda berdasarkan jam dalam sehari?
elif menu == "2️⃣ Pola Penyewaan per Jam":
    st.title("⏰ Pola Penyewaan Sepeda Berdasarkan Jam")
    hourly_rentals = df.groupby("hr")["cnt"].mean().reset_index()

    # visualisasi nya
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=hourly_rentals["hr"], y=hourly_rentals["cnt"], marker="o", color="#1f77b4", ax=ax)
    plt.xticks(range(0, 24))
    plt.xlabel("Jam")
    plt.ylabel("Rata-rata Penyewaan Sepeda")
    plt.title("Pola Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # bagian kesimpulan
    st.write("**📌 Kesimpulan:**")
    st.write("Puncak penyewaan terjadi pada jam sibuk: pagi (07:00-09:00) & sore (17:00-19:00)")
    st.write("Penyewaan menurun di siang dan malam hari")
    st.write("**Strategi:** Menyesuaikan jumlah sepeda dan harga berdasarkan waktu")
