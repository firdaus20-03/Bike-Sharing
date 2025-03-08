import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load dataset nya
file_path = "dashboard/all_data.csv" 
@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    category_cols = ["season", "yr", "mnth", "holiday", "weekday", "workingday", "weathersit"]
    for col in category_cols:
        df[col] = df[col].astype("category")
    return df

df = load_data()

# sidebar
st.sidebar.image('bike.jpg')
st.sidebar.header('Muhammad Firdaus_MC211D5Y2137')
st.sidebar.title("Analisis Bike Sharing")
option = st.sidebar.selectbox("Pilih Analisis", ["Pengaruh Hari Libur", "Pola Pengguna Baru vs Lama", "RFM Analysis"])

# 1. Pengaruh Hari Libur terhadap Jumlah Peminjaman Sepeda
if option == "Pengaruh Hari Libur":
    st.title("📊Pengaruh Hari Libur terhadap Jumlah Peminjaman Sepeda")
    holiday_group = df.groupby("holiday")["cnt"].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=holiday_group.index, y=holiday_group.values, ax=ax, palette="coolwarm")
    ax.set_xticklabels(["Bukan Hari Libur", "Hari Libur"])
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Perbandingan Penyewaan Sepeda pada Hari Libur dan Biasa")
    st.pyplot(fig)

# 2. Pola Pengguna Baru vs Pengguna Lama
elif option == "Pola Pengguna Baru vs Lama":
    st.title("📈Pola Pengguna Baru vs Pengguna Lama")
    user_trend = df.groupby("dteday")[["casual", "registered"]].sum()
    fig, ax = plt.subplots()
    sns.lineplot(data=user_trend, x=user_trend.index, y=user_trend["casual"], label="Casual (Baru)", ax=ax)
    sns.lineplot(data=user_trend, x=user_trend.index, y=user_trend["registered"], label="Registered (Lama)", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Tren Pengguna Baru vs Lama")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 3. RFM Analysis
elif option == "RFM Analysis":
    st.title("📊📈RFM Analysis")
    rfm = df.groupby("dteday").agg({"cnt": "sum"})
    rfm.columns = ["Total Penyewaan"]
    rfm["Recency"] = (df["dteday"].max() - rfm.index).days
    st.write("## Tabel RFM Analysis")
    st.dataframe(rfm.head(10))

    fig, ax = plt.subplots()
    sns.histplot(rfm["Total Penyewaan"], bins=20, kde=True, ax=ax, color="blue")
    ax.set_xlabel("Total Penyewaan Sepeda")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Distribusi Total Penyewaan Sepeda")
    st.pyplot(fig)
