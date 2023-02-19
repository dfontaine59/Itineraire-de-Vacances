from source_poi import SourcePoi
from destination import Destination
from neighbours import get_n_closest_points
import pandas as pd
import streamlit as st


@st.cache_data
def retrieve():
    d = Destination()
    return d.retrieve('poi'), d.retrieve('communes'), d.retrieve('clusters')

df_poi, df_communes, df_clusters = retrieve()

st.sidebar.title("Itinéraire de vacances")
jours = st.sidebar.slider(
    label='Durée du séjour',
    min_value=1,
    max_value=15,
    value=2,
    step=1
)
visites = st.sidebar.slider(
    label='Nombre de visites par jour',
    min_value=1,
    max_value=8,
    value=4,
    step=1
)
types = st.sidebar.multiselect(
    "Types d'itinéraires", 
    SourcePoi.TYPES.values(),
    SourcePoi.TYPES.values())

departement = st.sidebar.selectbox(
    'Département', 
    df_communes['departement'].unique()
)
commune = st.sidebar.selectbox(
    'Commune', 
    df_communes[df_communes['departement'] == departement]['commune'].unique()
)
df_communes = df_communes[df_communes['commune'] == commune]
df_poi = df_poi[df_poi['type'].map(lambda x: any([t in x for t in types]))]

st.write("POI (10 premiers)", df_poi.head(5))
st.write("Commune", df_communes)
st.map(df_poi)
centroids = get_n_closest_points(df_communes, df_clusters, jours)
st.map(pd.concat([df_communes, centroids]))
