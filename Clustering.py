import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import davies_bouldin_score
import seaborn as sns
from pyclustering.cluster.clarans import clarans
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

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
            font-size: 24px;
            font-weight: bold;
        }
        .title-center {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<p class="center title">Analisis Clustering Kemiskinan Kabupaten/Kota di Indonesia</p>', unsafe_allow_html=True)

    #Ketentuan
    st.write("Ketentuan data yang akan digunakan untuk proses clustering: ")
    st.write('''
             - Wajib memiliki kolom yang mencakup nama Kabupaten/Kota di Indonesia
             - Memiliki minimal 2 variabel indikator yang akan digunakan untuk proses clustering
             ''')

    st.write("Contoh dataset yang dapat digunakan: https://tinyurl.com/datasetkemiskinan2022")

    # File upload
    uploaded_file = st.file_uploader("Upload data", type=["csv", "xlsx"])
    global data

    if uploaded_file is not None:
        # Read dataset
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        
        st.write("Preview Data:")
        st.dataframe(data)
        
        # Dropdown for Region Name
        region_column = st.selectbox("Pilih kolom Nama Kabupaten/Kota", data.columns)
        
        # Rename the selected column to 'Kabupaten/Kota'
        data = data.rename(columns={region_column: 'Kabupaten/Kota'})
        
        # Multiselect for Indicator Variables
        indicator_columns = st.multiselect("Pilih kolom Variabel Indikator", data.columns)
        
        # Check if the selected indicator columns are more than 2
        if indicator_columns:
            if len(indicator_columns) < 2:
                st.warning("Pilih minimal 2 kolom variabel indikator.")
            else:
                # Check if the selected columns are numeric
                non_numeric_columns = [col for col in indicator_columns if not pd.api.types.is_numeric_dtype(data[col])]
                
                if non_numeric_columns:
                    st.warning(f"Kolom berikut bukan numerik: {', '.join(non_numeric_columns)}. Silakan pilih kolom numerik.")
                else:
                    # 1. Create new dataframe "df" with only the selected indicator columns
                    df = data[['Kabupaten/Kota'] + indicator_columns].copy()
                    ori_data = data[['Kabupaten/Kota'] + indicator_columns].copy()

                    # 2. Normalize the data in dataframe "df"
                    scaler = StandardScaler()
                    df_to_normalize = df.iloc[:, 1:]
                    df_normalized = pd.DataFrame(scaler.fit_transform(df_to_normalize), columns=df_to_normalize.columns)
                    
                    # 3. Transform the normalized dataframe into a list
                    df_data = df_normalized.values.tolist()

                    # Option to determine number of clusters or use automatic number of clusters
                    cluster_option = st.radio("Pilih cara menentukan jumlah cluster", ("Tentukan sendiri jumlah cluster", "Jumlah cluster optimum ditentukan secara otomatis"))

                    if cluster_option == "Tentukan sendiri jumlah cluster":
                        n_clusters = st.selectbox("Pilih jumlah cluster", list(range(2, 11)))
                    else:
                        davies_bouldin_scores = []
                        for n_clusters in range(2, 11):
                            clarans_instance_1 = clarans(df_data, n_clusters, 2, 4)
                            clarans_instance_1.process()
                            cluster_1 = clarans_instance_1.get_clusters()

                            cluster_labels_1 = [-1] * len(df_normalized)
                            for cluster_idx_1, cluster in enumerate(cluster_1):
                                for point_idx_1 in cluster:
                                    cluster_labels_1[point_idx_1] = cluster_idx_1
                            davies_bouldin_score_value = davies_bouldin_score(df_normalized, cluster_labels_1)
                            davies_bouldin_scores.append(davies_bouldin_score_value)

                        # Find the number of clusters with the smallest Davies-Bouldin Index
                        min_dbi_value = min(davies_bouldin_scores)
                        optimal_n_clusters = range(2, 11)[davies_bouldin_scores.index(min_dbi_value)]
                        n_clusters = optimal_n_clusters
                        st.write(f"Jumlah cluster yang optimum: {n_clusters}")

                    # Option to determine own parameters or use automatic parameters
                    param_option = st.radio("Pilih cara menentukan parameter CLARANS", ("Tentukan sendiri parameter CLARANS", "Parameter CLARANS Default"))

                    if param_option == "Tentukan sendiri parameter CLARANS":
                        numlocal = st.number_input("Tentukan numlocal", min_value=2, value=2, step=1)
                        maxneighbor = st.number_input("Tentukan maxneighbor", min_value=2, value=4, step=1)
                    else:
                        numlocal = 2
                        maxneighbor = 4
                        st.write(f"Parameter Default:")
                        st.write(f"numlocal = {numlocal}")
                        st.write(f"maxneighbor = {maxneighbor}")

                    if st.button("Run CLARANS Analysis"):
                        gif_placeholder = st.empty()
                        #gif_placeholder.markdown('cargando-loading.gif')
                        #gif_placeholder.markdown('<img src="https://media.tenor.com/JwPW0tw69vAAAAAi/cargando-loading.gif" alt="loading" style="width: 30%;">', unsafe_allow_html=True)
                        gif_placeholder.markdown(
                            """
                            <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
                                <img src="https://media.tenor.com/JwPW0tw69vAAAAAi/cargando-loading.gif" alt="loading" style="width: 30%;">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Run CLARANS algorithm
                        clarans_instance_1 = clarans(df_data, n_clusters, numlocal, maxneighbor)
                        clarans_instance_1.process()
                        cluster_1 = clarans_instance_1.get_clusters()

                        # Assign cluster labels to the original dataframe
                        cluster_labels_1 = [-1] * len(df_normalized)
                        for cluster_idx_1, cluster in enumerate(cluster_1):
                            for point_idx_1 in cluster:
                                cluster_labels_1[point_idx_1] = cluster_idx_1

                        # Assign cluster labels to the dataframe
                        df['Cluster'] = cluster_labels_1

                        gif_placeholder.empty()

                        # Display Analysis Result
                        st.markdown('<h3 class="title-center">Hasil Analisis CLARANS</h3>', unsafe_allow_html=True)
                        
                        st.markdown("##### Jumlah Kabupaten/Kota di tiap Cluster: ") 
                        cluster_counts = df['Cluster'].value_counts()
                        cluster_counts_df = pd.DataFrame({'Cluster': cluster_counts.index, 'Count': cluster_counts.values})
                        st.write(cluster_counts_df)

                        st.markdown("##### Hasil Clustering: ") 
                        st.dataframe(df)
                        
                        st.markdown("##### Visualisasi Parallel Plot: ")
                        parplot = px.parallel_coordinates(df, color="Cluster", labels={"Cluster": "Cluster"})
                        st.plotly_chart(parplot)

                        st.markdown("##### Statistik Deskriptif: ")
                        st.write(ori_data.describe())
                        
                        st.markdown("##### Peta Hasil Clustering: ")
                        clarans_result = df[['Kabupaten/Kota', 'Cluster']]
                        shapefile = gpd.read_file('peta-indonesia/indonesia_kab.shp')

                        shapefile['NAMA_KAB'] = shapefile['NAMA_KAB'].str.strip().str.lower()
                        clarans_result['Kabupaten/Kota'] = clarans_result['Kabupaten/Kota'].str.strip().str.lower()
                        merged = shapefile.merge(clarans_result, left_on='NAMA_KAB', right_on='Kabupaten/Kota', how='inner')

                        # Create a color map for clusters
                        cluster_colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#ffa500', '#008000', '#800080', '#800000']
                        cluster_color_map = {cluster: color for cluster, color in zip(merged['Cluster'].unique(), cluster_colors)}

                        indo_location = [-2.49607,117.89587]

                        m = folium.Map(location=indo_location, zoom_start=5)

                        # Add GeoJson data with custom style function
                        def style_function(feature):
                            cluster = feature['properties']['Cluster']
                            return {'fillColor': cluster_color_map.get(cluster, '#ffffff'), 'color': '#000000', 'fillOpacity': 0.5, 'weight': 1}

                        # Add GeoJson layer to the map
                        folium.GeoJson(
                            merged,
                            name='Clustered Areas',
                            style_function=style_function
                        ).add_to(m)

                        st_folium(m, width=725, height=400, returned_objects=[])

                        st.markdown('Keterangan:')
                        if n_clusters == 2:
                            st.markdown('0 = Merah')
                            st.markdown('1 = Hijau Neon')
                        elif n_clusters == 3:
                            st.markdown('0 = Merah')
                            st.markdown('1 = Hijau Neon')
                            st.markdown('3 = Biru')
                        elif n_clusters == 4:
                            st.markdown('0 = Merah')
                            st.markdown('1 = Hijau Neon')
                            st.markdown('3 = Biru')
                            st.markdown('4 = Kuning')
                        elif n_clusters == 5:
                            st.markdown('0 = Merah')
                            st.markdown('1 = Hijau Neon')
                            st.markdown('3 = Biru')
                            st.markdown('4 = Kuning')
                            st.markdown('5 = Cyan/Aqua')
                        elif n_clusters == 6:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('0 = Merah')
                                st.markdown('1 = Hijau Neon')
                                st.markdown('3 = Biru')
                                st.markdown('4 = Kuning')
                                st.markdown('5 = Cyan/Aqua')
                            with col2:
                                st.markdown('6 = Magenta/Fuchsia')
                        elif n_clusters == 7:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('0 = Merah')
                                st.markdown('1 = Hijau Neon')
                                st.markdown('3 = Biru')
                                st.markdown('4 = Kuning')
                                st.markdown('5 = Cyan/Aqua')
                            with col2:
                                st.markdown('6 = Magenta/Fuchsia')
                                st.markdown('7 = Oranye')
                        elif n_clusters == 8:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('0 = Merah')
                                st.markdown('1 = Hijau Neon')
                                st.markdown('3 = Biru')
                                st.markdown('4 = Kuning')
                                st.markdown('5 = Cyan/Aqua')
                            with col2:
                                st.markdown('6 = Magenta/Fuchsia')
                                st.markdown('7 = Oranye')
                                st.markdown('8 = Hijau Tua')
                        elif n_clusters == 9:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('0 = Merah')
                                st.markdown('1 = Hijau Neon')
                                st.markdown('3 = Biru')
                                st.markdown('4 = Kuning')
                                st.markdown('5 = Cyan/Aqua')
                            with col2:
                                st.markdown('5 = Cyan/Aqua')
                                st.markdown('6 = Magenta/Fuchsia')
                                st.markdown('7 = Oranye')
                                st.markdown('8 = Hijau Tua')
                                st.markdown('9 = Ungu')
                        elif n_clusters == 10:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('0 = Merah')
                                st.markdown('1 = Hijau Neon')
                                st.markdown('3 = Biru')
                                st.markdown('4 = Kuning')
                                st.markdown('5 = Cyan/Aqua')
                            with col2:
                                st.markdown('6 = Magenta/Fuchsia')
                                st.markdown('7 = Oranye')
                                st.markdown('8 = Hijau Tua')
                                st.markdown('9 = Ungu')
                                st.markdown('10 = Merah Marun')

                        st.markdown('')

                        # Write DataFrame to an Excel file
                        df.to_excel('DataHasilCLARANS.xlsx', index=False)

                        # Read the Excel file as binary data
                        with open('DataHasilCLARANS.xlsx', 'rb') as f:
                            excel_data = f.read()

                        # Create two columns, one for the download button and the other for the Markdown text
                        col1, col2 = st.columns([3, 7])

                        # Place the download button in the first column
                        with col1:
                            st.download_button(label='Download Data Hasil CLARANS', data=excel_data, file_name='DataHasilCLARANS.xlsx')

                        # Place the Markdown text in the second column
                        with col2:
                            st.markdown("_Hati-hati karena setelah tombol download di-klik, page akan langsung ter-refresh._")
