from sqlalchemy import create_engine
import os
import pandas as pd
from dotenv import load_dotenv
from Admin.connection.Server.Query import query_letter

def create_df():
    load_dotenv()

    engine = create_engine(f"postgresql://{os.getenv('user_server')}:{os.getenv('password_server')}@{os.getenv('host_server')}/{os.getenv('name_DB_server')}")

    text=query_letter('2024/07/19')
    df=pd.read_sql_query(text, engine)

    #df.to_excel('solicitudes.xlsx', index=False)

    engine.dispose()
    return df