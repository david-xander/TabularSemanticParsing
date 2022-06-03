import os, sys
from src.parse_args import args
from src.data_processor.schema_graph import SchemaGraph
from src.demos.demos import Text2SQLWrapper, demo_preprocess
from src.trans_checker.args import args as cs_args
import src.utils.utils as utils

from pathlib import Path
import sqlite3
import pandas as pd
import configparser

# Set model ID
args.model_id = utils.model_index[args.model]
assert(args.model_id is not None)

def setup(args):
    csv_name = "Energy"
    csv_dir = "data/"
    
    global db_path    
    delimiter = ","
    csv_path = os.path.join(csv_dir, '{}.csv'.format(csv_name))
    print('* csv_path = ' + csv_path + '\n')
    csv = pd.read_csv(csv_path, sep=delimiter)


def setup2(args):
    csv_name = "Energy"
    csv_dir = "data/"
    delimiter = ","

    global db_path
    db_path = os.path.join(csv_dir, '{}.sqlite'.format(csv_name))
    print('* db_path = ' + db_path + '\n')
    if os.path.exists(db_path):
        os.remove(db_path)
    schema = SchemaGraph(csv_name, db_path=db_path)
    csv_path = os.path.join(csv_dir, '{}.csv'.format(csv_name))
    conn = sqlite3.connect(db_path)
    csv = pd.read_csv(csv_path, sep=delimiter)
    print('* rows: ' + str(csv.shape[0]) + ', columns: ' + str(csv.shape[1]) + '\n')
    csv.to_sql(csv_name, conn, if_exists='append', index = False)
    conn.close()
    schema.load_data_from_csv_file(csv_path)
    schema.pretty_print()
    return Text2SQLWrapper(args, cs_args, schema), schema

    # global db_path
    # db_path = os.path.join(csv_dir, '{}.csv'.format(csv_name))
    
    # print("* db_path = " + db_path + "\n")
    # schema = SchemaGraph(csv_name, db_path=db_path)
    # csv_path = os.path.join(csv_dir, '{}.csv'.format(csv_name))
    # if not os.path.exists(db_path):    
    #     Path(db_path).touch()
    #     conn = sqlite3.connect(db_path)
    #     csv = pd.read_csv(csv_path)
    #     csv.to_sql(csv_name, conn, if_exists='append', index = False)
    #     conn.close()
    # schema.load_data_from_csv_file(csv_path)
    # schema.pretty_print()
    # return Text2SQLWrapper(args, cs_args, schema), schema

def show_readline():
    sys.stdout.write('NL questions about the DB: ')
    sys.stdout.write('> ')
    sys.stdout.flush()

if __name__ == '__main__':
    t2sql, schema = setup2(args)
    show_readline()
    text = sys.stdin.readline()

    while text:
        output = t2sql.process(text, schema.name)
        sql_query = output['sql_query']
        print(sql_query)
        show_readline()
        text = sys.stdin.readline()
