import folium
import route


def get_map(df, mode):
    m = folium.Map(control_scale=True)

    for i,row in df.iterrows():
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            popup=row.commentaire,
            tooltip=row.nom,
            icon=folium.Icon(icon='home', prefix='fa')
        ).add_to(m)

    df = df[['latitude','longitude']]
    sw = df.min().values.tolist()
    ne = df.max().values.tolist()
    m.fit_bounds([sw, ne], max_zoom=14) 

    latlon_start = df.values.tolist()
    latlon_end = latlon_start[1:]
    for start, end in zip(latlon_start, latlon_end):
        routeLatLons = route.get_route(start, end, mode)
        folium.PolyLine(routeLatLons, weight=5, opacity=1).add_to(m)

    return m