from geopy.distance import distance


def get_n_closest_points(df_ref, df_other, n):
    df_other['distance'] = df_other.apply(
        lambda row: distance(
            (df_ref['latitude'].iloc[0], df_ref['longitude'].iloc[0]), 
            (row['latitude'], row['longitude'])
        ).meters, 
        axis=1
    )
    return df_other.sort_values('distance').head(n)