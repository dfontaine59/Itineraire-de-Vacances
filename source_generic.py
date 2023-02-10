import pandas as pd
from sqlalchemy import create_engine, text


class SourceGeneric:

    DATABASE_URL = 'postgresql://znckjdyz:1Z1UVKsGHICvNknjnOSrzw3mlNjnN1jn@trumpet.db.elephantsql.com/znckjdyz'

    def load(self, df):
        with create_engine(self.DATABASE_URL).begin() as connection:
            df.to_sql(self.TABLE, connection, if_exists='replace', index=False)  # Load dataframe to postgresql
    
    def retrieve(self):
        with create_engine(self.DATABASE_URL).begin() as connection:
            return pd.read_sql(text(f'SELECT * FROM {self.TABLE}'), connection)  # Retrieve dataframe from postgresql for streamlit

    def etl(self):
        self.load(self.transform(self.extract()))