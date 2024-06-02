import psycopg2 
from datetime import datetime, date
from psycopg2 import Error, IntegrityError
from fastapi import HTTPException
from models import employee
import helper

'''
-- Obsolete
db_name = "postgres"
db_user = "postgres"
db_password = "World1954"
db_host = "127.0.0.1"  # e.g., "localhost"
db_port = "5432"  # default PostgreSQL ports
'''

global db_name 
global db_user 
global db_password 
global db_host 
global db_port 

class DbConfig():
    '''
    db_name:str
    db_user: str
    db_password: str
    db_host:str
    db_port: str
    '''

    def __init__(self):
        configuration = helper.get_config()
        self.db_name = configuration['POSTGRES_DB']
        self.db_user = configuration['POSTGRES_USER']
        self.db_password = configuration['POSTGRES_PASSWORD']
        self.db_host = configuration['POSTGRES_HOST']  # e.g., "localhost"
        self.db_port = configuration['POSTGRES_PORT']

# needs modification on AWS
DATABASE_URL = 'postgresql+psycopg2://username:password@localhost:5432/mydatabase'

# function execute_sql_file and bootstap are used in a bootstrap sttep
# thinkable is to have a separate script for this instead placing it in this file
def execute_sql_file(filename, connection):
    with connection.cursor() as cursor:
        with open(filename, 'r') as file:
            cursor.execute(file.read())
    connection.commit()

def bootstap():
    '''
    Bootstrap function using .env for DB configuration

    Returns:
        None
    '''
    configuration = DbConfig()

    '''
    db_name = configuration['POSTGRES_DB']
    db_user = configuration['POSTGRES_USER']
    db_password = configuration['POSTGRES_PASSWORD']
    db_host = configuration['POSTGRES_HOST']  # e.g., "localhost"
    db_port = configuration['POSTGRES_PORT']
    '''

    conn = create_connection(configuration.db_name, 
                             configuration.db_user, 
                             configuration.db_password, 
                             configuration.db_host, 
                             configuration.db_port)

    # path variable should be configurable
    execute_sql_file('SQL/create_table.sql', conn)
    conn.close()

def create_connection(db_name: str, db_user:str , db_password:str, db_host:str, db_port:str):
    """
    Create a connection to the PostgreSQL database.

    Parameters:
    db_name (str): The name of the database.
    db_user (str): The user name used to authenticate.
    db_password (str): The password used to authenticate.
    db_host (str): The host running the database.
    db_port (str): The port number on which the database is listening.

    Returns:
    connection (object): The PostgreSQL database connection object.
    """


    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def create_employee(employee):
    '''
    Creates a new employee with the given employee data in the PostgreSQL database.

    Parameters:
    employee (object): An object containing the following attributes:
                       - name (str): The name of the employee.
                       - employee_id (int): The unique identifier for the employee.
                       - department (str): The department in which the employee works.
                       - dob (str): The date of birth of the employee in YYYY-MM-DD format.
                       - email (str): The email address of the employee.

    Raises:
    IntegrityError: If there is a database integrity error, such as a duplicate employee_id.
    Exception: If any other error occurs while connecting to or interacting with the PostgreSQL database.

    The function connects to the PostgreSQL database, inserts the employee data into the employee table,
    and handles exceptions that may arise during the process. The database connection is closed after
    the operation, regardless of success or failure.
    '''

    configuration = DbConfig()
    try:
        connection = create_connection(configuration.db_name, 
                             configuration.db_user, 
                             configuration.db_password, 
                             configuration.db_host, 
                             configuration.db_port)

        cursor = connection.cursor()
        insert_query = """
            INSERT INTO employee (name, employee_id, department, dob, email)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (employee.name, employee.employee_id, employee.department, employee.dob, employee.email))
        connection.commit()

        print("Employee inserted successfully!")

    except IntegrityError as e: 
        raise e

    except (Exception, Error) as error:
        print("Error while connecting/writing to DB:", error)
        raise Exception("Employee not inserted!")

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("DB connection is closed")


def get_employee(id: int):
    '''
    Gets an employee with the given id

    Parameters:
        id : int  resource id

    Raises:
        Exceptions
    '''
    
    configuration = DbConfig()

    try:
        connection = create_connection(configuration.db_name, 
                             configuration.db_user, 
                             configuration.db_password, 
                             configuration.db_host, 
                             configuration.db_port)

        cursor = connection.cursor()
        select_query = "SELECT id, employee_id, name, department, dob, email FROM employee WHERE id = %s"

        cursor.execute(select_query, (id,))
        entry = cursor.fetchone()

        # If no record is found, raise a 404 error
        if entry is None:
            print("Warning - Record not found")
            raise HTTPException(status_code=404, detail="Employee not found")

        print(entry)

        # convert datatime to string format
        dob_str = entry[4].strftime('%m/%d/%Y')
        calc_age = calculate_age(dob_str)

        # Return the employee data
        employee_record = employee.EmployeeAge(
            id=entry[0],
            employee_id=entry[1],
            name=entry[1],
            department=entry[3],
            age=calc_age,
            email=entry[5]
        )

        return employee_record 
    except (Exception, Error) as error:
        print( error )
        raise Exception(error)
            #status_code=500, 
            #detail=f"Error retrieving employee data: {error}")

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("DB connection is closed")

def delete_employee(id:int):
    '''
    '''

    configuration = DbConfig()

    try:
        connection = create_connection(configuration.db_name, 
                             configuration.db_user, 
                             configuration.db_password, 
                             configuration.db_host, 
                             configuration.db_port)
        
        delete_query = f"DELETE FROM employee WHERE id = %s"
        cursor = connection.cursor()

        cursor.execute(delete_query, (id,))
        connection.commit()

        # Check if any row was deleted
        if cursor.rowcount > 0:
            print("Successfully deleted")
        else:
            print(f"No row deleted.")
            raise Exception("Resource not found. Nothing deleted.")

    except (Exception, Error) as error:
        print( error )
        raise Exception(error)
    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("DB connection is closed")
        

def calculate_age(dob_str: str) -> int:
    dob = datetime.strptime(dob_str, '%m/%d/%Y').date()
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age
