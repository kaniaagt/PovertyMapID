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
from branca.element import Template, MacroElement

def app():
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px
        }
        .title {
            font-size: 24px;
            font-weight: bold;
        }
        .center-text {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<p class="center title">Peta Kemiskinan Kabupaten dan Kota di Indonesia Tahun 2023</p>', unsafe_allow_html=True)

    df = pd.read_excel('DataHasilCLARANS (3, 4, 8).xlsx')

    data_result = df[['Kabupaten/Kota', 'Cluster']]
    shapefile = gpd.read_file('peta-indonesia/indonesia_kab.shp')

    shapefile['NAMA_KAB'] = shapefile['NAMA_KAB'].str.strip().str.lower()
    data_result['Kabupaten/Kota'] = data_result['Kabupaten/Kota'].str.strip().str.lower()
    merged = shapefile.merge(data_result, left_on='NAMA_KAB', right_on='Kabupaten/Kota', how='inner')

    # Create a color map for clusters
    cluster_colors = ['yellow', 'red', 'orange']
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

    # Create the legend template as an HTML element
    legend_template = """
    {% macro html(this, kwargs) %}
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
        border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>     
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background: yellow; opacity: 0.75;'></span>Cluster 0</li>
        <li><span style='background: red; opacity: 0.75;'></span>Cluster 1</li>
        <li><span style='background: orange; opacity: 0.75;'></span>Cluster 2</li>
    </ul>
    </div>
    </div> 
    <style type='text/css'>
    .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
    .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
    .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
    </style>
    {% endmacro %}
    """
    
    # Add the legend to the map
    macro = MacroElement()
    macro._template = Template(legend_template)
    m.get_root().add_child(macro)

    st_folium(m, width=725, height=400, returned_objects=[])

    with st.expander("Tentang Data"):
        st.markdown('<p class="center-text">Tabel Data</p>', unsafe_allow_html=True)
        st.dataframe(df)

        st.markdown('<p class="center-text">Informasi Data</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            desc_table = pd.DataFrame({
                "Kolom": ["Kabupaten/Kota","<SD", "Tamat SD/SMP", ">SMA", 
                          "Tidak bekerja", "Kerja Sektor Informal", 
                          "Kerja Sektor Formal", "Garis Kemiskinan"],
                "Deskripsi": ["Nama kabupaten/kota",
                              "Persentase penduduk miskin suatu kabupaten/kota tahun 2023 yang berumur 15 tahun ke atas dan tidak tamat SD (tidak mempunyai ijazah)", 
                              "Persentase penduduk miskin suatu kabupaten/kota tahun 2023 yang berumur 15 tahun ke atas dan hanya tamat SD/SMP",
                              "Persentase penduduk miskin suatu kabupaten/kota tahun 2023 yang berumur 15 tahun ke atas dan mempunyai ijazah SMA atau ijazah perguruan tinggi", 
                              "Persentase penduduk miskin suatu kabupaten/kota tahun 2023 yang tidak bekerja", 
                              "Persentase penduduk miskin suatu kabupaten/kota tahun 2023 yang berumur 15 tahun ke atas dan bekerja di sektor informal", 
                              "Persentase penduduk miskin suatu kabupaten/kota tahun 2023 yang berumur 15 tahun ke atas dan bekerja di sektor formal", 
                              "Garis Kemiskinan merupakan representasi dari jumlah rupiah minimum yang dibutuhkan untuk memenuhi kebutuhan pokok minimum makanan yang setara dengan 2100 kilokalori per kapita per hari dan kebutuhan pokok bukan makanan"]
            })
            desc_table.index = desc_table.index + 1
            st.table(desc_table)
            #st.dataframe(desc_table, hide_index=True)

        with col2:
            analysis_option = st.selectbox("Pilih analisis statistik", ["Statistik Deskriptif", "Plot Korelasi", "Histogram"])

            if analysis_option == "Statistik Deskriptif":
                st.write(df.describe())
            elif analysis_option == "Plot Korelasi":
                fig, ax = plt.subplots(figsize=(10, 8))
                numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
                numeric_columns = numeric_columns.drop('Cluster')
                correlation_matrix = df[numeric_columns].corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
                st.pyplot(fig)
            elif analysis_option == "Histogram":
                column_to_plot = st.selectbox("Pilih variabel indikator", df.columns)
                fig, ax = plt.subplots()
                sns.histplot(df[column_to_plot], kde=True, ax=ax)
                st.pyplot(fig)


    with st.expander("Hasil Cluster"):
        st.markdown('<p class="center-text">Visualisasi Cluster</p>', unsafe_allow_html=True)
        st.write("Parallel Coordinates Plot untuk Semua Variabel Indikator")
        result_parplot = px.parallel_coordinates(df, color="Cluster", labels={"Cluster": "Cluster"})
        st.plotly_chart(result_parplot)

        st.markdown('<p class="center-text">Karakteristik Cluster</p>', unsafe_allow_html=True)
        char_table = pd.DataFrame({
                        "Nomor Cluster": ["0","1", "2"],
                        "Nama CLuster": ["Relatively Self-Sufficient",
                                         "High Prirority for Assistance", 
                                         "Support for Sustainable Growth"],
                        "Jumlah Anggota Cluster": ["162", "164", "188"],
                        "Karakteristik Cluster": [ "Tingkat kelulusan pendidikan cukup tinggi, tingkat ketenagakerjaan menengah, tingkat standar hidup cukup tinggi",
                                                  "Tingkat kelulusan pendidikan menengah,ringkat ketenagakerjaan rendah, ringkat standar hidup rendah",
                                                  "Tingkat kelulusan pendidikan rendah, tingkat ketenagakerjaan menengah, tingkat standar hidup menengah"]
                    })
        char_table.index = char_table.index + 1
        st.table(char_table)
        #st.dataframe(char_table, hide_index=True)
        #st.dataframe(char_table, height=300, width=800, hide_index=True)