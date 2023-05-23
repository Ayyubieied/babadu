import psycopg2
from psycopg2 import Error

# CARA GUNAIN DI VIEWS
# 1. import utils-nya
# from utils.query import *
# 2. retreive datanya sebagai list 
# lst = execute_query("SELECT * FROM ATLET WHERE negara_asal='Indonesia';")


try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                password="y9a1zNV2FmVbQECwKeEq",
                                host="containers-us-west-25.railway.app",
                                port="7777",
                                database="railway")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    # Executing a SQL query
    cursor.execute("SELECT version();")

    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    cursor.execute("SET search_path TO BABADU;")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def execute_query(query:str):
    query = query.strip()
    if not (query.endswith(";")):
        query += ";"
    cursor.execute(query)
    if (query.upper().startswith("SELECT")):
        return cursor.fetchall()
    elif (query.upper().startswith("INSERT")) or (query.upper().startswith("UPDATE")) or (query.upper().startswith("CREATE")):
        connection.commit()

def list_tup_to_list_list(lst):
    ret = []
    for x in lst:
        ret.append(list(x))
    return ret
    
def iterate_list(lst):
    for x in lst:
        print(x)
    print()

def exec_and_print(query:str):
    iterate_list(execute_query(query))

# cara pake 
# queryErrorFlag, queryResult = try_except_query("SELECT ....")
def try_except_query(query:str):
    try:
        return False, execute_query(query)
    except (Exception, Error) as error:
        connection.rollback()
        cursor.execute("SET SEARCH_PATH TO BABADU;")
        return True, error

# test
if __name__ == '__main__':
    exec_and_print("SELECT * FROM ATLET WHERE negara_asal='Indonesia';")
    exec_and_print("SELECT * FROM ATLET;")
    nama = 'gaga'
    email = 'dfdf'
    error, result = try_except_query(f'SELECT * FROM babadu.member WHERE nama = \'{nama}\' AND email = \'{email}\';');
    print(error, result)
    if not error:
        id_user_login = result[0][0]
        is_pelatih = execute_query(f'SELECT * FROM babadu.pelatih WHERE id = \'{id_user_login}\';')