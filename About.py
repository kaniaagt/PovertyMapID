import streamlit as st
from PIL import Image

def app():
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
        }
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<p class="center title">Welcome to POVERTYMAPID</p>', unsafe_allow_html=True)

    text = """
    Website POVERTMAPID merupakan website untuk memantau tingkat kemiskinan setiap kabupaten dan kota yang ada di Indonesia berdasarkan hasil analisis cluster menggunakan algoritma CLARANS. Website ini dirancang untuk para pengguna yang memiliki pemahaman tentang analisis statistik dan ingin memantau tingkat kemiskinan dari kabupaten dan kota yang ada di Indonesia. Selain itu, di dalam website ini, pengguna juga dapat melakukan analisis cluster menggunakan metode CLARANS dengan data indikator kemiskinan milik sendiri lho! Tunggu apa lagi? Ayo mari kita melakukan analisis clustering untuk lebih memahami tingkat kemiskinan setiap kabupaten dan kota di Indonesia !
    """
    st.write('<div style="text-align: justify;">{}</div>'.format(text), unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")

    st.markdown("#### Panduan Penggunaan Aplikasi")
    analysis_option = st.selectbox("Pilih page yang ingin diketahui informasi mengenai panduan penggunaannya:", ["Peta", "Clustering"])

    if analysis_option == "Peta":
        st.markdown("##### Halaman Peta")
        st.write("Pada halaman ini akan ditampilkan: ")
        
        st.write("1. Peta kemiskinan kabupaten dan kota di seluruh Indonesia pada tahun 2023.")
        petakemiskinan = Image.open("SS PovertyMapID/Halaman Peta/Halaman Peta.png")
        st.image(petakemiskinan, caption='Peta Kemiskinan Kabupaten dan Kota di seluruh Indonesia pada tahun 2023', use_column_width=True)
        
        st.write("2. Informasi Tentang Data yang mencakup preview tabel data yang digunakan, tabel deskripsi kolom dan beberapa macam informasi statistik seperti statistik deskriptif, plot korelasi dan histogram.")
        tentangdata = Image.open("SS PovertyMapID/Halaman Peta/Tentang Data.png")
        st.image(tentangdata, caption='Informasi Tentang Data', use_column_width=True)
        plotkorelasi = Image.open("SS PovertyMapID/Halaman Peta/Plot Korelasi.png")
        histogram = Image.open("SS PovertyMapID/Halaman Peta/Histogram.png")
        col1, col2 = st.columns(2)
        with col1:
            st.image(plotkorelasi, caption='Plot Korelasi', use_column_width=True)

        with col2:
            st.image(histogram, caption='Histogram', use_column_width=True)

        st.write("3. Informasi Hasil Cluster yang mencakup visualisasi parallel coordinates plot dan tabel karakteristik cluster yang terbentuk.")
        hasilcluster = Image.open("SS PovertyMapID/Halaman Peta/Hasil Cluster.png")
        st.image(hasilcluster, caption='Informasi Hasil Cluster', use_column_width=True)

    elif analysis_option == "Clustering":
        st.markdown("##### Halaman Clustering")
        st.write("Halaman ini digunakan untuk melakukan analisis cluster dengan algoritma CLARANS menggunakan dataset dari user. Berikut tahapan penggunaan halaman Clustering: ")

        st.write("1. User diminta untuk menginput data mengenai Penduduk Miskin di Kabupaten/Kota di Indonesia dengan beberapa variabel indikator kemiskinan sesuai dengan ketentuan.")
        uploaddata = Image.open("SS PovertyMapID/Halaman Clustering/Upload Data.png")
        st.image(uploaddata, caption='Upload data', use_column_width=True)

        st.write("2. Setelah user mengupload data, user dapat melihat preview data.")
        prevdata = Image.open("SS PovertyMapID/Halaman Clustering/Preview Data.png")
        st.image(prevdata, caption='Preview data', use_column_width=True)

        st.write('3. Selanjutnya, user dapat menginput informasi yang dibutuhkan (kolom nama kabupaten/kota dan kolom variabel indikator yang akan digunakan) dan parameter CLARANS yang meliputi jumlah cluster, numlocal (jumlah iterasi yang dilakukan untuk memperoleh hasil akhir) dan maxneighbor (jumlah data point berdekatan yang akan dianalisis). Parameter CLARANS juga dapat ditentukan secara otomatis oleh aplikasi.')
        inputparameter = Image.open("SS PovertyMapID/Halaman Clustering/Define Parameter.png")
        st.image(inputparameter, caption='Input informasi kolom dan parameter CLARANS', use_column_width=True)

        st.write("4. Untuk menge-run proses clustering, user harus memencet tombol `Run CLARANS Analysis`")

        st.write("5. Setelah beberapa saat dan program telah selesai menge-run proses clustering, pengguna dapat melihat hasil analisis cluster dan peta berdasarkan hasil clustering.")
        result = Image.open("SS PovertyMapID/Halaman Clustering/CLARANS result.png")
        st.image(result, caption='Hasil Analisis CLARANS', use_column_width=True)

        st.write("6. Pengguna dapat menyimpan data hasil clustering berupa data excel dengan memencet tombol `Download Data Hasil CLARANS`.")
        downloadhasil = Image.open("SS PovertyMapID/Halaman Clustering/Download Hasil.png")
        st.image(downloadhasil, caption='Download Data Hasil Analisis CLARANS', use_column_width=True)

        st.write("7. Hasil data hasil analisis CLARNS yang didownload pengguna adalah sebagai berikut:")
        hasil = Image.open("SS PovertyMapID/Halaman Clustering/Hasil.png")
        st.image(hasil, caption='Data Hasil Analisis CLARANS yang terdownload', use_column_width=True)


