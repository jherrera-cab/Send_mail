from sqlalchemy import create_engine
import os
import pandas as pd
from dotenv import load_dotenv
from Query import query_obligation

load_dotenv()


engine = create_engine(f"postgresql://{os.getenv('user_server')}:{os.getenv('password_server')}@{os.getenv('host_server')}/{os.getenv('name_DB_server')}")

text=query_obligation('2024/05/22')
df=pd.read_sql_query(text, engine)

print(len(df))

engine.dispose()