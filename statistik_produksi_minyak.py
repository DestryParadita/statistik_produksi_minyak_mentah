"""
Aplikasi Streamlit untuk menggambarkan statistik produksi minyak mentah dari berbagai negara di seluruh sunia

Sumber data berasal dari produksi_minyak_mentah.csv
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""

import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia")
st.markdown("*Sumber data berasal dari produksi_minyak_mentah.csv")
############### title ###############)

############### sidebar ###############
image = Image.open('rig.jpg')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, right_col = st.columns(2)

with open("kode_negara_lengkap.json") as f:
    data = json.load(f)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_nama_negara = []
list_kode_negara = []
for i in data:
    list_nama_negara.append(i['name'])
    list_kode_negara.append(i['alpha-3'])
nama_negara = st.sidebar.selectbox("Pilih negara (N)", list_nama_negara)

############### upper left column ###############
left_col.subheader("Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N")

filepath = "produksi_minyak_mentah.csv"
df = pd.read_csv(filepath)
exclude = []
for i in df['kode_negara'].values.tolist():
    if i not in list_kode_negara and i not in exclude:
        exclude.append(i)

df = df[df['kode_negara'] != 'OEU']
df = df[df['kode_negara'] !='WLD']
df = df[df['kode_negara'] != 'EU28']
df = df[df['kode_negara'] != 'G20']
df = df[df['kode_negara'] != 'OECD']

for i in range(len(data)):
    if nama_negara == list_nama_negara[i]:
        kode_negara = list_kode_negara[i]
negara = df[df['kode_negara'] == kode_negara]

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(negara)]
fig, ax = plt.subplots()
ax.bar(negara['tahun'].values.tolist(), negara['produksi'].values.tolist(), color=colors)
ax.set_xticklabels(negara['tahun'], rotation=45)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Produksi", fontsize=12)
plt.tight_layout()

left_col.pyplot(fig)

############### upper left column ###############

############### upper right column ###############
right_col.subheader("B-besar negara dengan jumlah produksi terbesar pada tahun T")

n_negara= st.sidebar.number_input("Masukkan jumlah negara dengan produksi terbesar pada tahun T yang ingin ditampilkan (B)", min_value=1, max_value=None)
tahun = st.sidebar.number_input("Pilih tahun (T)", min_value=1971, max_value=2015)

negara = df[df['tahun'] == tahun]
negara = negara.sort_values(by=['produksi'], ascending=False)
negara=negara[:n_negara]
list_negara = []
daftar_negara = negara['kode_negara'].values.tolist()
for i in daftar_negara:
    for j in range(len(list_kode_negara)):
        if i == list_kode_negara[j]:
            list_negara.append(list_nama_negara[j])
            
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(negara)]
fig, ax = plt.subplots()
ax.bar(list_negara, negara['produksi'].values.tolist(), color=colors)
ax.set_xticklabels(list_negara, rotation=90)
ax.set_xlabel("Negara", fontsize=12)
ax.set_ylabel("Produksi", fontsize=12)
plt.tight_layout()

right_col.pyplot(fig)

############### upper right column ###############

############### lower left column ###############
left_col.subheader("Grafik B-besar negara dengan jumlah produksi terbesar secara kumulatif keseluruhan tahun")

banyak_country= st.sidebar.number_input("Masukkan jumlah negara dengan produksi kumulatif terbesar yang ingin ditampilkan (B)", min_value=1, max_value=None)

country = df.groupby(['kode_negara'])['produksi'].sum().reset_index()
country = country.sort_values(by=['produksi'], ascending=False)
country=country[:banyak_country]
list_country = []
daftar_country = country['kode_negara'].values.tolist()
for i in daftar_country:
    for j in range(len(list_kode_negara)):
        if i == list_kode_negara[j]:
            list_country.append(list_nama_negara[j])
          
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(country)]
fig, ax = plt.subplots()
ax.bar(list_country, country['produksi'].values.tolist(), color=colors)
ax.set_xticklabels(list_country, rotation=90)
ax.set_xlabel("Negara", fontsize=12)
ax.set_ylabel("Produksi", fontsize=12)
plt.tight_layout()

left_col.pyplot(fig)

############### lower left column ###############

############### lower right column ###############
right_col.subheader("Summary")

for j in range(len(list_kode_negara)):
    if daftar_negara[0] == list_kode_negara[j]:
        nama = data[j]['name']
        kode = data[j]['alpha-3']
        region = data[j]['region']
        sub_region = data[j]['sub-region']
        jumlah = negara['produksi'].values.tolist()[0]

right_col.markdown(f"**Negara dengan jumlah produksi terbesar pada tahun {tahun}: ** \n {nama}, {kode}, {region}, {sub_region}, {jumlah}")

for j in range(len(list_kode_negara)):
    if daftar_country[0]== list_kode_negara[j]:
        nama = data[j]['name']
        kode = data[j]['alpha-3']
        region = data[j]['region']
        sub_region = data[j]['sub-region']
        jumlah = country['produksi'].values.tolist()[0]

right_col.markdown(f"**Negara dengan jumlah produksi terbesar pada keseluruhan tahun: ** \n {nama}, {kode}, {region}, {sub_region}, {jumlah}")

#Jika ingin menampilkan semua negara dengan produksi sama dengan nol
negara = df[df['tahun'] == tahun]
negara = negara.sort_values(by=['produksi'], ascending=False)
daftar_negara = negara['kode_negara'].values.tolist()

for i in range(len(negara)):
    for j in range(len(list_kode_negara)):
        if negara['produksi'].values.tolist()[i]==0 and daftar_negara[i]==list_kode_negara[j]:
            nama = data[j]['name']
            kode = data[j]['alpha-3']
            region = data[j]['region']
            sub_region = data[j]['sub-region']
            right_col.markdown(f"**Negara dengan produksi sama dengan nol pada {tahun}: ** \n {nama}, {kode}, {region}, {sub_region}")
    
# #Jika hanya ingin menampilkan salah satu negara dengan produksi sama dengan nol
# negara = df[df['tahun'] == tahun]
# negara = negara.sort_values(by=['produksi'], ascending=False)
# daftar_negara = negara['kode_negara'].values.tolist()
            
for j in range(len(list_kode_negara)):
    if negara['produksi'].values.tolist()[-1]==0 and daftar_negara[-1]==list_kode_negara[j]:
        nama = data[j]['name']
        kode = data[j]['alpha-3']
        region = data[j]['region']
        sub_region = data[j]['sub-region']
        right_col.markdown(f"**Salah satu negara dengan jumlah produksi sama dengan nol pada tahun {tahun}: ** \n {nama}, {kode}, {region}, {sub_region}")

#Jika ingin menanmpilkan seluruh negara dengan produksi kumulatif sama dengan nol
country = df.groupby(['kode_negara'])['produksi'].sum().reset_index()
country = country.sort_values(by=['produksi'], ascending=False)
daftar_country = country['kode_negara'].values.tolist()

for i in range(len(country)):
    for j in range(len(list_kode_negara)):
        if country['produksi'].values.tolist()[i]==0 and daftar_country [i]==list_kode_negara[j]:
            nama = data[j]['name']
            kode = data[j]['alpha-3']
            region = data[j]['region']
            sub_region = data[j]['sub-region']
            right_col.markdown(f"**Negara dengan produksi sama dengan nol pada keseluruhan tahun: ** \n {nama}, {kode}, {region}, {sub_region}")

# #Jika hanya ingin menampilkan salah satu negara dengan produksi kumulatif sama dengan nol           
# for j in range(len(list_kode_negara)):
#     if country['produksi'].values.tolist()[-1]==0 and daftar_country[-1]==list_kode_negara[j]:
#         nama = data[j]['name']
#         kode = data[j]['alpha-3']
#         region = data[j]['region']
#         sub_region = data[j]['sub-region']
#         right_col.markdown(f"**Salah satu negara dengan jumlah produksi sama dengan nol pada keseluruhan tahun: ** \n {nama}, {kode}, {region}, {sub_region}")

for i in range(len(negara)-1, -1, -1):
    for j in range(len(list_kode_negara)):
        if negara['produksi'].values.tolist()[i]!=0 and daftar_negara[i]==list_kode_negara[j]:
            nama = data[j]['name']
            kode = data[j]['alpha-3']
            region = data[j]['region']
            sub_region = data[j]['sub-region']
            jumlah = negara['produksi'].values.tolist()[i]
            right_col.markdown(f"**Negara dengan jumlah produksi terkecil (tidak sama dengan nol) pada tahun {tahun}: ** \n {nama}, {kode}, {region}, {sub_region}, {jumlah}")
            break
    if negara['produksi'].values.tolist()[i]!=0:
        break

for i in range(len(country)-1, -1, -1):
    for j in range(len(list_kode_negara)):
        if country['produksi'].values.tolist()[i]!=0 and daftar_country[i]==list_kode_negara[j]:
            nama = data[j]['name']
            kode = data[j]['alpha-3']
            region = data[j]['region']
            sub_region = data[j]['sub-region']
            jumlah = country['produksi'].values.tolist()[i]
            right_col.markdown(f"**Negara dengan jumlah produksi terkecil (tidak sama dengan nol) pada keseluruhan tahun: ** \n {nama}, {kode}, {region}, {sub_region}, {jumlah}")
            break
    if country['produksi'].values.tolist()[i]!=0:
        break 

############### lower right column ###############