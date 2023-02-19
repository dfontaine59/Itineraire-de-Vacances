from k_means_constrained import KMeansConstrained


def get_clusters(df):
    clf = KMeansConstrained(
        n_clusters=1000,
        size_min=10,
        size_max=40
    )
    clf.fit_predict(df[['latitude', 'longitude']])
    return clf.labels_, clf.cluster_centers_
