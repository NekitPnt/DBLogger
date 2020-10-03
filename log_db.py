import logging
import psycopg2
import json
from datetime import datetime


class LogDBHandler(logging.Handler):
    def __init__(self, conn, db_tbl_log):
        logging.Handler.__init__(self)
        self.conn = conn
        self.db_tbl_log = db_tbl_log

    def emit(self, record):
        operation_code = record.args[0]
        result_code = record.args[1]
        parameters = record.args[2]
        entity_type_code = record.args[3]
        user_name = record.args[4]

        user_name = 'NULL' if not user_name else f"'{user_name}'"
        entity_uuid = 'NULL' if entity_type_code in ['TransactionHistory', 'Chatbot'] else "uuid_generate_v4()"
        sql = f"INSERT INTO {self.db_tbl_log} VALUES (uuid_generate_v4(), '{operation_code}', '{result_code}', " \
              f"'{json.dumps(parameters)}', {entity_uuid}, '{entity_type_code}', {user_name}, '{datetime.now()}');"
        try:
            with self.conn, self.conn.cursor() as cur:
                cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
