from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URL = 'POSTRGRESS_URL'

engine = create_engine(DATABASE_URL)
metadata = MetaData()
database = Database(DATABASE_URL)
