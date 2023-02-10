import pandas as pd
import requests
from source_generic import SourceGeneric


class SourcePoi(SourceGeneric):

    POI_URL = 'https://diffuseur.datatourisme.fr/webservice/bfadcf44012b7156ca3e297b468c4f75/380d2fe9-2c9c-4190-a79e-8301b37d03fb'
    TABLE = 'poi'
    TYPES = {
        'WalkingTour': 'Itinéraire pédestre',
        'CyclingTour': 'Itinéraire cyclable',
        'HorseTour': 'Itinéraire équestre',
        'RoadTour': 'Itinéraire routier',
        'FluvialTour': 'Itinéraire fluvial ou maritime',
        'UnderwaterRoute': 'Itinéraire sous-marin',
        'Accommodation': 'Hébergement',
        'FoodEstablishment': 'Restauration',
        'CulturalSite': 'Site culturel',
        'NaturalHeritage': 'Site naturel',
        'SportsAndLeisurePlace': 'Site sportif, récréatif et de loisirs',
    }

    def get_types(self, type):
        types = [self.TYPES[t] for t in set(self.TYPES.keys()) & set(type)]
        return types if types else None

    def extract(self):
        data = requests.get(self.POI_URL).json()
        return pd.json_normalize(data['@graph'])

    def transform(self, df):
        columns = {
            '@type': 'type',
            'rdfs:label.@value': 'nom',
            'rdfs:comment.@value': 'commentaire',
            'hasContact.schema:email': 'contact_email',
            'hasContact.schema:telephone': 'contact_telephone',
            'hasContact.foaf:homepage': 'contact_homepage',
            'isLocatedAt.schema:address.schema:streetAddress': 'adresse',
            'isLocatedAt.schema:address.schema:addressLocality': 'ville',
            'isLocatedAt.schema:address.schema:postalCode': 'code_postal',
            'isLocatedAt.schema:geo.schema:latitude.@value': 'latitude',
            'isLocatedAt.schema:geo.schema:longitude.@value': 'longitude',
        }
        df = df[columns.keys()]  # Keep only useful columns
        df = df.rename(columns=columns)
        df[['latitude', 'longitude']] = df[['latitude', 'longitude']].applymap(lambda x: pd.to_numeric(x, errors='coerce')) 
        df['type'] = df['type'].apply(self.get_types)  # Keep only interesting types
        df = df.dropna(subset=['nom', 'type', 'latitude', 'longitude'])  # Suppress rows with null specific columns
        return df