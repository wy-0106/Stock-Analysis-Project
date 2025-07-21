# Import the necessary libraries
from sqlalchemy import create_engine
import pymysql

# Database configuration
DATABASE_CONFIG = {

    'user': 'root',
    'password': '000000',
    'host': 'localhost',
    'port': '3306',
    'database': 'tmx_database',
    'table_name': 'top_volume_table'

}

# Get connection string function
def get_connection_string(database_config):

    user = database_config['user']
    password = database_config['password']
    host = database_config['host']
    port = database_config['port']
    database = database_config['database']

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# Create database engine function
def create_database_engine():

    connection_string = get_connection_string(DATABASE_CONFIG)
    return create_engine(connection_string)

# Upload dataframe to SQL function
def upload_dataframe_to_sql(dataframe, table_name = DATABASE_CONFIG['table_name'], if_exists_option = 'append'):

    engine = create_database_engine()

    try:

        dataframe.to_sql(name = table_name, con = engine, if_exists = if_exists_option, index = False)

    except Exception as e:

        raise e
