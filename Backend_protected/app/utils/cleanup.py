from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from ..models.database import engine

def clear_database():
    """
    Deletes all data from all tables in the database.
    """
    meta = MetaData()
    meta.reflect(bind=engine)
    with engine.begin() as connection:
        for table in reversed(meta.sorted_tables):
            connection.execute(table.delete())
    print("All tables have been cleared from the database.")
