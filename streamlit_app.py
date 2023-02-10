from source_communes import SourceCommunes
from source_poi import SourcePoi
import streamlit as st


@st.cache_data
def retrieve():
    return SourcePoi().retrieve(), SourceCommunes().retrieve()

df_poi, df_communes = retrieve()

st.sidebar.title("Itinéraire de vacances")
jours = st.sidebar.slider(
    label='Durée du séjour',
    min_value=1,
    max_value=15,
    value=2,
    step=1
)
jours = st.sidebar.slider(
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

st.write("POI (10 premiers)", df_poi.head(10))
st.write("Commune", df_communes)
st.map(df_poi[['latitude', 'longitude']])
st.map(df_communes[['latitude', 'longitude']])