from sqlalchemy import create_engine


class Destination:

    DATABASE_URL = "postgresql://znckjdyz:1Z1UVKsGHICvNknjnOSrzw3mlNjnN1jn@trumpet.db.elephantsql.com/znckjdyz"

    def load(self, df, table):
        with create_engine(self.DATABASE_URL).begin() as connection:
            df.to_sql(table, connection, if_exists="replace", index=False)
