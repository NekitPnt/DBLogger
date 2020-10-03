import psycopg2
import logging
import log_db
import config

# подключаемся к базе
db_tbl_log = config.TABLE_NAME
conn = psycopg2.connect(dbname=config.DB_NAME, host=config.HOST, user=config.USER)
conn.autocommit = True

# настраиваем логгирование
logdb = log_db.LogDBHandler(conn, db_tbl_log)
logging.basicConfig()
logging.getLogger('').addHandler(logdb)
log = logging.getLogger('test_logger')
log.setLevel('DEBUG')


# прогоняем по тесткейсам
test_case_1 = {
    "OperationCode": "TransactionHistoryAccess",
    "ResultCode": "Success",
    "Parameters": {"number": "over9000"},
    "EntityTypeCode": "TransactionHistory",
    "UserName": "test@test.test",
}
test_case_2 = {
    "OperationCode": "TransactionHistoryDeny",
    "ResultCode": "Fail",
    "Parameters": {"number": "over9000"},
    "EntityTypeCode": "Test",
    "UserName": "",
}
test_case_3 = {
    "OperationCode": "TransactionHistoryDeny",
    "ResultCode": "Fail",
    "Parameters": {"number": "over9000"},
    "EntityTypeCode": "Chatbot",
    "UserName": "",
}

for test_case in [test_case_1, test_case_2, test_case_3]:
    log.info('%s%s%s%s%s ', *[v for k, v in test_case.items()])

