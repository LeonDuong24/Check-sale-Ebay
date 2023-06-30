import traceback

import sys
import os
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import db,login
import sys
import os
from sqlalchemy import MetaData, Table, create_engine,text
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import CONFIG,ZONE,logger


def excute_query(query,engine):
    try:
        with engine.connect() as connection:
            result=connection.execute(text(query))
            connection.commit()
        return True
    except:
        logger.error(traceback.format_exc())
        return False 