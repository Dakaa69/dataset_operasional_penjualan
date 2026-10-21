from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data/dataset_sintesis_penjualan_1000.csv"

st.set_page_config(page_title="Bedah Kasus 1 | Raka Ramadhan",page_icon="📊",layout="wide")

@st.cache_data
def load_data():
    d=pd.read_csv(DATA,parse_dates=["Tanggal"])
    d["Omzet_Rp"]=d["Harga_Rp"]*d["Jumlah_Terjual"]
    return d

df=load_data()

st.title("Bedah Kasus 1: Dataset Operasional Penjualan")
st.markdown("### Raka Ramadhan")
st.markdown("**NIM: 241051016**")
st.caption("Dashboard analitik menggunakan dataset sintesis 1.000 observasi.")

def rp(x): return f"Rp {x:,.0f}".replace(",", ".")

with st.sidebar:
    st.header("Filter Data")
    dr=st.date_input("Rentang tanggal",(df.Tanggal.min().date(),df.Tanggal.max().date()))
    ps=st.multiselect("Produk",sorted(df.Produk.unique()),default=sorted(df.Produk.unique()))
    ks=st.multiselect("Kategori",sorted(df.Kategori.unique()),default=sorted(df.Kategori.unique()))

if isinstance(dr,tuple) and len(dr)==2:
    start,end=pd.Timestamp(dr[0]),pd.Timestamp(dr[1])
else:
    start=end=pd.Timestamp(dr)

d=df[df.Tanggal.between(start,end)&df.Produk.isin(ps)&df.Kategori.isin(ks)].copy()
if d.empty:
    st.warning("Tidak ada data untuk filter tersebut."); st.stop()

c1,c2,c3,c4=st.columns(4)
c1.metric("Total Omzet",rp(d.Omzet_Rp.sum()))
c2.metric("Total Unit",f"{d.Jumlah_Terjual.sum():,.0f}".replace(",",".")) 
c3.metric("Observasi",f"{len(d):,}".replace(",","."))
c4.metric("Rata-rata Harga",rp(d.Harga_Rp.mean()))

t1,t2,t3,t4=st.tabs(["Ringkasan","Analisis Variabel","Tren Waktu","Data & Metodologi"])

with t1:
    st.subheader("Kinerja Produk")
    p=d.groupby(["Produk","Kategori"],as_index=False).agg(
        transaksi=("Produk","size"),jumlah_terjual=("Jumlah_Terjual","sum"),
        omzet=("Omzet_Rp","sum"),harga_rata2=("Harga_Rp","mean"))
    p["share_omzet_pct"]=p.omzet/p.omzet.sum()*100
    p["share_qty_pct"]=p.jumlah_terjual/p.jumlah_terjual.sum()*100
    a,b=st.columns(2)
    with a:
        fig=px.bar(p,x="Produk",y="omzet",color="Kategori",text_auto=".2s",title="Omzet menurut Produk")
        fig.update_layout(showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=px.bar(p,x="Produk",y="jumlah_terjual",color="Kategori",text_auto=".2s",title="Jumlah Terjual menurut Produk")
        fig.update_layout(showlegend=False); st.plotly_chart(fig,use_container_width=True)
    st.dataframe(p.style.format({"transaksi":"{:,.0f}","jumlah_terjual":"{:,.0f}","omzet":"Rp {:,.0f}","harga_rata2":"Rp {:,.0f}","share_omzet_pct":"{:.2f}%","share_qty_pct":"{:.2f}%"}),use_container_width=True,hide_index=True)

with t2:
    st.subheader("Distribusi dan Hubungan Variabel")
    a,b=st.columns(2)
    with a:
        st.plotly_chart(px.histogram(d,x="Jumlah_Terjual",color="Produk",nbins=30,marginal="box",title="Distribusi Jumlah Terjual"),use_container_width=True)
    with b:
        st.plotly_chart(px.histogram(d,x="Harga_Rp",color="Produk",nbins=30,marginal="box",title="Distribusi Harga"),use_container_width=True)
    st.plotly_chart(px.scatter(d,x="Harga_Rp",y="Jumlah_Terjual",color="Produk",opacity=.65,hover_data=["Kategori","Tanggal","Omzet_Rp"],title="Harga vs Jumlah Terjual"),use_container_width=True)
    st.subheader("Matriks Korelasi")
    st.dataframe(d[["Harga_Rp","Jumlah_Terjual","Omzet_Rp"]].corr().style.format("{:.3f}"),use_container_width=True)
    st.info("Korelasi tidak menunjukkan kausalitas. Perbedaan skala harga Laptop dan Buku memengaruhi korelasi agregat.")

with t3:
    st.subheader("Tren Waktu")
    m=d.set_index("Tanggal").resample("MS").agg(transaksi=("Produk","size"),jumlah_terjual=("Jumlah_Terjual","sum"),omzet=("Omzet_Rp","sum")).reset_index()
    st.plotly_chart(px.line(m,x="Tanggal",y="omzet",markers=True,title="Tren Omzet Bulanan"),use_container_width=True)
    st.plotly_chart(px.line(m,x="Tanggal",y="jumlah_terjual",markers=True,title="Tren Jumlah Terjual Bulanan"),use_container_width=True)

with t4:
    st.subheader("Data Hasil Filter")
    st.download_button("⬇️ Download CSV",d.to_csv(index=False).encode("utf-8-sig"),"data_penjualan_hasil_filter.csv","text/csv")
    st.dataframe(d,use_container_width=True,hide_index=True)
    st.subheader("Identitas Mahasiswa")
    st.write("**Nama:** Raka Ramadhan")
    st.write("**NIM:** 241051016")
    st.subheader("Metodologi")
    st.markdown("""
    Dataset awal hanya memiliki dua observasi. Dataset 1.000 baris ini merupakan **data sintesis untuk pembelajaran**, bukan data historis.

    - Seed: 42
    - Produk: Laptop dan Buku
    - Kategori: Elektronik dan Pendidikan
    - Harga divariasikan di sekitar harga acuan
    - Jumlah terjual dibuat sebagai data diskrit
    - Tanggal dibuat sepanjang 2024
    - Omzet = Harga × Jumlah Terjual
    """)

st.caption("Bedah Kasus 1 | Raka Ramadhan | NIM 241051016")
