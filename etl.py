from clusters import get_clusters
from destination import Destination
import pandas as pd
from source_communes import SourceCommunes
from source_poi import SourcePoi


sc = SourceCommunes()  # from a csv of data.gouv.fr
sp = SourcePoi()  # from a daily updated json of datatourism.fr
d = Destination()  # postgresql database

df_communes = sc.transform(sc.extract())
df_poi = sp.transform(sp.extract())
df_poi["cluster_id"], centroids = get_clusters(df_poi)  # Last about a few hours
df_clusters = (
    pd.DataFrame(centroids, columns=["latitude", "longitude"])
    .rename_axis("id")
    .reset_index()
)

d.load(df_communes, "communes")
d.load(df_poi, "poi")
d.load(df_clusters, "clusters")
