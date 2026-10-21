from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
df=pd.read_csv(ROOT/"data/dataset_sintesis_penjualan_1000.csv",parse_dates=["Tanggal"])
df["Omzet_Rp"]=df.Harga_Rp*df.Jumlah_Terjual
out=ROOT/"output"; out.mkdir(exist_ok=True)

df[["Harga_Rp","Jumlah_Terjual","Omzet_Rp"]].describe().T.to_csv(out/"statistik_deskriptif.csv",encoding="utf-8-sig")
p=df.groupby(["Produk","Kategori"]).agg(transaksi=("Produk","size"),jumlah_terjual=("Jumlah_Terjual","sum"),omzet=("Omzet_Rp","sum"),harga_rata2=("Harga_Rp","mean")).reset_index()
p["share_omzet_pct"]=p.omzet/df.Omzet_Rp.sum()*100
p["share_qty_pct"]=p.jumlah_terjual/df.Jumlah_Terjual.sum()*100
p.to_csv(out/"ringkasan_produk.csv",index=False,encoding="utf-8-sig")
m=df.set_index("Tanggal").resample("MS").agg(transaksi=("Produk","size"),jumlah_terjual=("Jumlah_Terjual","sum"),omzet=("Omzet_Rp","sum")).reset_index()
m.to_csv(out/"ringkasan_bulanan.csv",index=False,encoding="utf-8-sig")
df[["Harga_Rp","Jumlah_Terjual","Omzet_Rp"]].corr().to_csv(out/"korelasi.csv")
plt.figure(figsize=(10,5)); plt.plot(m.Tanggal,m.omzet,marker="o"); plt.title("Tren Omzet Bulanan"); plt.xlabel("Bulan"); plt.ylabel("Omzet (Rp)"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(out/"01_tren_omzet_bulanan.png",dpi=160); plt.close()
plt.figure(figsize=(8,5)); plt.bar(p.Produk,p.omzet); plt.title("Omzet berdasarkan Produk"); plt.ylabel("Omzet (Rp)"); plt.tight_layout(); plt.savefig(out/"02_omzet_produk.png",dpi=160); plt.close()
plt.figure(figsize=(8,5)); plt.bar(p.Produk,p.jumlah_terjual); plt.title("Jumlah Terjual berdasarkan Produk"); plt.ylabel("Unit"); plt.tight_layout(); plt.savefig(out/"03_qty_produk.png",dpi=160); plt.close()
plt.figure(figsize=(9,5)); plt.hist(df.Jumlah_Terjual,bins=30); plt.title("Distribusi Jumlah Terjual"); plt.xlabel("Jumlah Terjual"); plt.ylabel("Frekuensi"); plt.tight_layout(); plt.savefig(out/"05_distribusi_qty.png",dpi=160); plt.close()
