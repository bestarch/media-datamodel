from faker import Faker
from jproperties import Properties
import time
import pandas as pd
import os
import traceback
import sys
import logging

from redis.commands.search.field import TextField, TagField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

sys.path.append(os.path.abspath('redis_connection'))
from connection import RedisConnection


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.INFO)
# configs = Properties()
# with open('config/app-config.properties', 'rb') as config_file:
#     configs.load(config_file)
r = RedisConnection().get_connection()


def load_movie_data():
    df = pd.read_csv('movies.csv')

    try:
        pipeline = conn.pipeline()
        index = 0
        for index, row in df.iterrows():
            redis_key = f"movie:{index}"
            pipeline.json().set(redis_key, '$', row.to_dict())

        pipeline.execute()
        print(f"Loaded {index} movie records")
    except Exception as inst:
        print(type(inst))
        traceback.print_exc()
        print("Exception occurred while loading movies data")


def createIndexes():
    try:
        # FT.CREATE idx_movie on JSON PREFIX 1 movie:
        # SCHEMA
        #   $.original_title as original_title TEXT
        #   $.tag_line as tag_line TEXT
        #   $.season as season TAG
        #   $.day_of_week as day_of_week TAG
        #   $.budget as budget NUMERIC SORTABLE
        #   $.revenue as revenue NUMERIC SORTABLE
        #   $.runtime as runtime NUMERIC SORTABLE
        #   $.vote_count as vote_count NUMERIC SORTABLE
        #   $.year as year NUMERIC
        schema = (TextField("$.original_title", as_name="original_title"),
                  TextField("$.tag_line", as_name="tag_line"),
                  TagField("$.season", as_name="season"),
                  TagField("$.day_of_week", as_name="day_of_week"),
                  NumericField("$.budget", as_name="budget", sortable=True),
                  NumericField("$.revenue", as_name="revenue", sortable=True),
                  NumericField("$.runtime", as_name="runtime", sortable=True),
                  NumericField("$.vote_count", as_name="vote_count", sortable=True),
                  NumericField("$.year", as_name="year"))
        r.ft("idx_movie").create_index(schema, definition=IndexDefinition(prefix=["movie:"], index_type=IndexType.JSON))
        print("Created index: idx_movie")
    except Exception as inst:
        logging.warning("Exception occurred while creating idx_movie index")


if __name__ == '__main__':
    conn = RedisConnection().get_connection()
    try:
        load_movie_data()
    except Exception as inst:
        print(type(inst))
        print(inst)
        raise Exception('Exception occurred while generating data. Delete the corrupted data and try again')
