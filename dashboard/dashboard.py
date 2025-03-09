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

#RFM Analysis
elif menu == "3️⃣ RFM Analysis":
    st.title("📊 RFM Analysis untuk Penyewaan Sepeda")
    recent_date = df["dteday"].max()
    def calculate_rfm(df):
        rfm_df = df.groupby("weekday", as_index=False).agg({
            "dteday": "max",    
            "instant": "count", 
            "cnt": "sum"        
        })

        rfm_df.columns = ["weekday", "max_order_timestamp", "frequency", "monetary"]
        rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"])
        rfm_df["recency"] = (recent_date - rfm_df["max_order_timestamp"]).dt.days
        rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
        return rfm_df

    rfm_result = calculate_rfm(df)

    st.subheader("📋 Hasil RFM Analysis")
    st.dataframe(rfm_result)

    #visualisasi nya
    st.subheader("📊 Visualisasi RFM")

    #recency
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(rfm_result["recency"], bins=10, kde=True, color="#1f77b4", ax=ax)
    plt.xlabel("Recency (Hari sejak terakhir sewa)")
    plt.ylabel("Jumlah Pelanggan")
    plt.title("Distribusi Recency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    #frequency
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(rfm_result["frequency"], bins=10, kde=True, color="#ff7f0e", ax=ax)
    plt.xlabel("Frequency (Jumlah Sewa)")
    plt.ylabel("Jumlah Pelanggan")
    plt.title("Distribusi Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    #monetary
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(rfm_result["monetary"], bins=10, kde=True, color="#2ca02c", ax=ax)
    plt.xlabel("Monetary (Total Penyewaan)")
    plt.ylabel("Jumlah Pelanggan")
    plt.title("Distribusi Monetary")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    #bagian kesimpulan
    st.write("\n**📌 Kesimpulan:**")
    st.write("**Recency**: Mayoritas pengguna rutin menyewa sepeda dalam rentang 0-5 hari terakhir, menunjukkan layanan memiliki frekuensi penggunaan tinggi dan basis pelanggan aktif")
    st.write("**Frequency**: Tingginya frekuensi peminjaman menunjukkan keterlibatan pengguna yang konsisten, terutama dari pelanggan tetap yang mengandalkan sepeda sebagai transportasi harian")
    st.write("**Monetary**: Tingginya nilai monetary menunjukkan bahwa pengguna cenderung sering meminjam sepeda atau menggunakan layanan dalam jumlah besar")
