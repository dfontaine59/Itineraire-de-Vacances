from source_poi import SourcePoi
from destination import Destination
from neighbours import get_n_closest_points
from carte import get_map
import route
import streamlit as st
from streamlit_folium import st_folium


@st.cache_data
def retrieve():
    d = Destination()
    return d.retrieve('poi'), d.retrieve('communes'), d.retrieve('clusters')

df_poi, df_communes, df_clusters = retrieve()

st.sidebar.title("Itinéraire de vacances")
jours = st.sidebar.number_input(
    label='Durée du séjour',
    min_value=1,
    max_value=7,
    value=2,
    step=1
)
visites = st.sidebar.number_input(
    label='Nombre de visites par jour',
    min_value=1,
    max_value=10,
    value=5,
    step=1
)
mode = st.sidebar.selectbox(
    'Mode de transport', 
    route.mode_map.keys()
)
departement = st.sidebar.selectbox(
    'Département', 
    df_communes['departement'].unique()
)
commune = st.sidebar.selectbox(
    'Commune', 
    df_communes[df_communes['departement'] == departement]['commune'].unique()
)
types = st.multiselect(
    "Types d'itinéraires", 
    SourcePoi.TYPES.values(),
    SourcePoi.TYPES.values()
)
df_communes = df_communes[df_communes['commune'] == commune]
df_centroids = get_n_closest_points(df_communes, df_clusters, jours)
df_poi = df_poi[df_poi['type'].map(lambda x: any([t in x for t in types]))]

for jour, cluster in enumerate(df_centroids.index):
    df_zoom = df_poi[df_poi.cluster == cluster].head(visites)
    st.write(f"Jour n°{jour + 1}", df_zoom)
    st_folium(get_map(df_zoom, mode), width=700)