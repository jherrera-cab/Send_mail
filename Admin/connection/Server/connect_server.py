from sqlalchemy import create_engine
import os
import pandas as pd
print(os.getenv('user_server'))
print(os.getenv('password_server'))
print(os.getenv('host_server'))
print(os.getenv('name_db_server'))

engine = create_engine(f"postgresql://{os.getenv('user_server')}:{os.getenv('password_server')}@{os.getenv('host_server')}/{os.getenv('name_DB_server')}")


df=pd.read_sql_query("SELECT * FROM data_sinfin.obligaciones", engine)

print(len(df))

engine.dispose()