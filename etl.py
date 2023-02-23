import pandas as pd
from source_communes import SourceCommunes
from source_poi import SourcePoi
from clusters import get_clusters
from destination import Destination


sc = SourceCommunes()
sp = SourcePoi()
d = Destination()

df_communes = sc.transform(sc.extract())
df_poi = sp.transform(sp.extract())
df_poi['cluster'], centroids = get_clusters(df_poi)  # Last about 1 hour ! Maybe split by departement
df_clusters = pd.DataFrame(centroids, columns=['latitude', 'longitude']).rename_axis('cluster').reset_index()

d.load(df_communes, 'communes')
d.load(df_poi, 'poi')
d.load(df_clusters, 'clusters')
