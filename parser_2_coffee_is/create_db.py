from mysql.connector import connect, Error
from config import user, password, host, name_db


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


if __name__ == "__main__":
    c = connect_to_db(host, user, password)
    create_db_query = "CREATE DATABASE finca_coffee;"
    # drop_db_query = "DROP DATABASE IF EXISTS finca_coffee"
    create_new_db(c, create_db_query)

    ec = connect_to_exist_db(host, user, password, name_db)
    create_table_price_query = """ CREATE TABLE IF NOT EXISTS price(
                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                        country VARCHAR(40),
                                        region VARCHAR(40),
                                        price DECIMAL(4, 2),
                                        currency VARCHAR(8)
                                        );
                                    """

    execute_query(ec, create_table_price_query)
