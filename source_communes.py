import pandas as pd


class SourceCommunes:

    COMMUNES_URL = 'https://static.data.gouv.fr/resources/communes-de-france-base-des-codes-postaux/20200309-131459/communes-departement-region.csv'

    def extract(self):
        return pd.read_csv(self.COMMUNES_URL)

    def transform(self, df):
        columns = {
            'nom_departement': 'departement',
            'nom_commune_complet': 'commune',
            'latitude': 'latitude',
            'longitude': 'longitude',
        }
        df = df[df['nom_region'] == 'Auvergne-Rhône-Alpes']  # Keep only data for this region
        df = df[columns.keys()]  # Keep only useful columns
        df = df.rename(columns=columns)
        df[['latitude', 'longitude']] = df[['latitude', 'longitude']].applymap(lambda x: pd.to_numeric(x, errors='coerce')) 
        df = df.dropna()  # Suppress rows with null
        return df