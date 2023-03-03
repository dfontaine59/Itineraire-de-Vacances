import pandas as pd
import requests


class SourcePoi:

    POI_URL = "https://diffuseur.datatourisme.fr/webservice/bfadcf44012b7156ca3e297b468c4f75/380d2fe9-2c9c-4190-a79e-8301b37d03fb"
    TYPES = {
        "WalkingTour": "Itinéraire pédestre",
        "CyclingTour": "Itinéraire cyclable",
        "HorseTour": "Itinéraire équestre",
        "RoadTour": "Itinéraire routier",
        "FluvialTour": "Itinéraire fluvial",
        "UnderwaterRoute": "Itinéraire sous-marin",
        "Accommodation": "Hébergement",
        "FoodEstablishment": "Restauration",
        "CulturalSite": "Site culturel",
        "NaturalHeritage": "Site naturel",
        "SportsAndLeisurePlace": "Site sportif et de loisirs",
    }

    def get_types(self, type):
        types = [self.TYPES[t] for t in set(self.TYPES.keys()) & set(type)]
        return types if types else None

    def extract(self):
        data = requests.get(self.POI_URL).json()
        return pd.json_normalize(data["@graph"])

    def transform(self, df):
        columns = {
            "@type": "type",
            "rdfs:label.@value": "nom",
            "rdfs:comment.@value": "description",
            "hasContact.schema:email": "email",
            "hasContact.schema:telephone": "telephone",
            "hasContact.foaf:homepage": "site_internet",
            "isLocatedAt.schema:address.schema:streetAddress": "adresse",
            "isLocatedAt.schema:address.schema:addressLocality": "ville",
            "isLocatedAt.schema:address.schema:postalCode": "code_postal",
            "isLocatedAt.schema:geo.schema:latitude.@value": "latitude",
            "isLocatedAt.schema:geo.schema:longitude.@value": "longitude",
        }
        df = df[columns.keys()]  # Keep only useful columns
        df = df.rename(columns=columns)
        df[["latitude", "longitude"]] = df[["latitude", "longitude"]].applymap(
            lambda x: pd.to_numeric(x, errors="coerce")
        )
        df["type"] = df["type"].apply(self.get_types)  # Keep only interesting types
        df = df.dropna(subset=["nom", "type", "latitude", "longitude"])  # Delete nulls
        return df
