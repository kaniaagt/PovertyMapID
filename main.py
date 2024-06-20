import streamlit as st
from streamlit_option_menu import option_menu
import About, Mapping, Clustering
from streamlit_folium import st_folium

st.set_page_config(page_title="POVERTYMAPID")

class MultipagesApp:
    def __init__(self):
        self.apps = []

    def add_application(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
        
    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='POVERTYMAPID',
                options=['Beranda', 'Peta', 'Clustering'],
                icons=['question-circle', 'geo-alt', 'columns-gap'],
                menu_icon='map-fill',
                default_index=0,
                styles={
                    "container": {"padding": "10", "background-color": "grey"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "--hover-color": "black"},
                    "nav-link-selected": {"background-color": "#4a4a49"},
                }
            )
        if app == "Beranda":
            About.app()
        if app == "Peta":
            Mapping.app()
        if app == "Clustering":
            Clustering.app()

app = MultipagesApp()
app.run()
