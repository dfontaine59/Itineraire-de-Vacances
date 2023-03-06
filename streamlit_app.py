from carte import get_map
import pandas as pd
import requests
import route
from source_poi import SourcePoi
import streamlit as st
from streamlit_folium import st_folium

# définition de l'adresse de l'API
api_address = 'fast_api'
# port de l'API
api_port = 8000

st.set_page_config(
    page_title="Itinéraire de vacances",
    page_icon="🏁",
    layout="wide",
    menu_items={
        "About": "Data Scientest December 2022 - David Fontaine, Marion Pierre, Christophe Saugé, Slimane Thighermet"
    },
)

if "df_communes" not in st.session_state:
    #req = requests.get(f"http://127.0.0.1:8000/communes")
    req = requests.get(f"http://fastapi:8000/communes")
    st.session_state["df_communes"] = pd.read_json(req.json())
df_communes = st.session_state.df_communes


@st.cache_data
def get_poi(latitude, longitude, jours):
    #req = requests.get(f"http://127.0.0.1:8000/poi/{latitude}/{longitude}/{jours}")
    req = requests.get(f"http://fastapi:8000/poi/{latitude}/{longitude}/{jours}")
    return pd.read_json(req.json())


st.sidebar.title("Itinéraire de vacances")
jours = st.sidebar.number_input("Durée du séjour", min_value=1, max_value=8, value=2)
visites = st.sidebar.number_input(
    "Nombre de visites par jour (hors restaurant/hotel)",
    min_value=1,
    max_value=8,
    value=4,
)
mode = st.sidebar.selectbox("Mode de transport", route.mode_map.keys())
departement = st.sidebar.selectbox("Département", df_communes["departement"].unique())
commune = st.sidebar.selectbox(
    "Commune",
    df_communes[df_communes["departement"] == departement]["commune"].unique(),
)
types = st.multiselect(
    "Types d'itinéraires", SourcePoi.TYPES.values(), SourcePoi.TYPES.values()
)
df_communes = df_communes[df_communes["commune"] == commune]
df_poi = get_poi(df_communes.iloc[0].latitude, df_communes.iloc[0].longitude, jours)
df_poi = df_poi[df_poi["type"].map(lambda x: any([t in x for t in types]))]

col1, col2 = st.columns(2)
for jour, df_cluster in enumerate(dict(tuple(df_poi.groupby("cluster_id"))).values()):
    df_cluster = df_cluster.head(visites)
    if jour % 2 == 0:
        with col1:
            st.write(f"Jour n°{jour + 1}", df_cluster)
            st_folium(get_map(df_cluster, mode), width=700)
    else:
        with col2:
            st.write(f"Jour n°{jour + 1}", df_cluster)
            st_folium(get_map(df_cluster, mode), width=700)
