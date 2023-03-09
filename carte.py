import folium
import pandas as pd
import route
import streamlit as st


def type_to_icon(s):
    if "Hébergement" in s:
        return "icons/lodging.png"
    if "Restauration" in s:
        return "icons/restaurant.png"
    if "Site naturel" in s:
        return "icons/park.png"
    if "Site culturel" in s:
        return "icons/museum.png"
    if "Site sportif et de loisirs" in s:
        return "icons/sport.png"
    if "Start" in s:
        return "icons/start.png"
    return "icons/default.png"


def array_to_string(s):
    return ", ".join([x.strip('"') for x in s.strip("{}").split(",")]) if s else ""


def float_to_5dstring(s):
    return "" if pd.isnull(s) else f"{int(s):05d}"


@st.cache_resource
def get_map(df_communes, df, df_hotel_resto, mode):
    m = folium.Map(control_scale=True)

    # Affichage du point de départ
    folium.Marker(
        location=[df_communes.iloc[0].latitude, df_communes.iloc[0].longitude],
        tooltip=f"Point de départ: {df_communes.iloc[0].commune} ({df_communes.iloc[0].departement})",
        icon=folium.features.CustomIcon(icon_image=type_to_icon("Start"), icon_size=(45, 45)),
    ).add_to(m)

    # Affichage des points de l'itinéraire, des hotels et des restaurants
    for row in pd.concat([df, df_hotel_resto]).itertuples():
        html = (
            f"<b>{row.nom}</b><br>"
            f"{row.description}<br>"
            f"#️⃣ {array_to_string(row.type)}<br>"
            f"☎️ {array_to_string(row.telephone)}<br>"
            f"✉️ {array_to_string(row.email)}<br>"
            f"@ {array_to_string(row.site_internet)}<br>"
            f"🏠 {array_to_string(row.adresse)} {float_to_5dstring(row.code_postal)} {array_to_string(row.ville)}"
        )
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=folium.Popup(html, min_width=400, max_width=400),
            tooltip=row.nom,
            icon=folium.features.CustomIcon(icon_image=type_to_icon(row.type), icon_size=(45, 45)),
        ).add_to(m)

    # Calcul du trajet sans les hotels et les restaurants
    locations = route.get_route(df[["latitude", "longitude"]].values.tolist() + [[df_communes.iloc[0].latitude, df_communes.iloc[0].longitude]], mode)
    folium.PolyLine(locations, weight=5).add_to(m)

    # Centrage de la carte en fonctions des points de l'itinéraire
    df_loc = pd.DataFrame(locations + df_hotel_resto[["latitude", "longitude"]].values.tolist())
    south_west = df_loc.min().values.tolist()
    north_east = df_loc.max().values.tolist()
    m.fit_bounds([south_west, north_east])

    return m
