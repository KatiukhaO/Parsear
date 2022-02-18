from mysql.connector import connect, Error
from config import user, password, host, name_db
from query_to_db import create_db_query, create_table_price_query, drop_db_query


def connect_to_db(host, user, password):
    connection = None
    try:
        connection = connect(
            host=host,
            user=user,
            password=password)
        print("Connection to MySQL Server is successful")
    except Error as e:
        print(F"CONNECTION TO SERVER IS FAIL - {e}")
    return connection


def connect_to_exist_db(host, user, password, name_db):
    connection = None
    try:
        connection = connect(
            host=host,
            user=user,
            password=password,
            database=name_db)
        print(f"Connection to < {name_db} > is successful")
    except Error as e:
        print(F"CONNECTION TO SERVER IS FAIL - {e}")
    return connection


def create_new_db(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print("Create DB is successful")
    except Error as e:
        print(f"CREATE DB IS FAIL - {e}")


def drop_db(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print("Drop DB is successful")
    except Error as e:
        print(f"DROP DB IS FAIL - {e}")


def execute_query(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print("Execute query is successful")
    except Error as e:
        print(f"EXECUTE QUERY IS FAIL - {e}")



ec = connect_to_exist_db(host, user, password, name_db)
if ec is not None:
    execute_query(ec, create_table_price_query)
else:
    c = connect_to_db(host, user, password)
    create_new_db(c, create_db_query)
    ec = connect_to_exist_db(host, user, password, name_db)
    execute_query(ec, create_table_price_query)






