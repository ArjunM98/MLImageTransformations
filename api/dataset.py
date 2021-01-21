from configparser import ConfigParser
from sqlalchemy import create_engine, exc
import uuid
import os

def read_config(): 
    '''
        Config file reader for connecting to PSQL DB
        hosted on GCP PSQL
    :return: ConfigParser    
    '''

    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, '../config.ini')

    config = ConfigParser()
    config.read(file_path)

    return config

def connection_uri():
    '''
        Creating connection URI for connecting to PSQL DB. URI will
        be used to create SQLAlchemy engine for executing queries.
        :return: URI for our PSQL DB hosted in GCP SQL
    '''

    config = read_config()

    URI = 'postgresql+psycopg2://{}:{}@/{}?host={}'.format(
        config['scaleai_database']['user'],
        config['scaleai_database']['password'],
        config['scaleai_database']['dbname'],
        config['scaleai_database']['host']
    )

    return URI

def create_dataset(name):
    
    URI = connection_uri()
    conn = None

    try:
        print("CONNECTING TO DB!!!!")
        engine = create_engine(URI, echo=True)
        conn = engine.connect()
        
        datasetUUID = str(uuid.uuid4())
        
        INSERT_DATASET_ENTRY = """
                            INSERT INTO dataset 
                            VALUES ({0}, {1})
                            """.format(name, datasetUUID)
        print("WRITING TO DB!!!!")
        conn.execute(INSERT_DATASET_ENTRY)
        return datasetUUID

    except exc.SQLAlchemyError as err: 
        print(err)
        return 'Error occured inserting into table dataset. Exception: {}'.format(err)

    finally: 
        conn.close()
        engine.dispose()