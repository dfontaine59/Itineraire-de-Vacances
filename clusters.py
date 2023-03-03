from k_means_constrained import KMeansConstrained


def get_clusters(df):
    clf = KMeansConstrained(
        n_clusters=1000,
        size_min=20,
        size_max=40,
        n_jobs=-1,  # Parallelisation on all CPUs
    )
    clf.fit_predict(df[["latitude", "longitude"]])
    return clf.labels_, clf.cluster_centers_
