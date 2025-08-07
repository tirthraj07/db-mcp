from config.logger_config import LoggerFactory
from mysqldb.services.connection import connect_to_mysql


from typing import List, Optional, Dict
from mysql.connector.cursor import MySQLCursor
from mysql.connector import Error
from mysql.connector import MySQLConnection


logger = LoggerFactory.get_logger(__name__)

def get_tables(host:str, user:str, password:str, database:str, port:int=3306) -> Optional[List[str]]:
    """
    Retrieves the list of table names in a MySQL database.

    Args:
        host (str): The host address of the MySQL server.
        user (str): The username to authenticate with.
        password (str): The password for the MySQL user.
        database (str): The name of the database to fetch tables from.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[str]]: A list of table names if successful, otherwise None.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_mysql(host=host, user=user, password=password, database=database, port=port)
        if not connection:
            logger.error(f"Failed to connect to MYSQL database: '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor(dictionary=True)

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        table_names = []
        for table in tables:
            for _, value in table.items():
                table_names.append(value)

        if(len(table_names) == 0):
            logger.info(f"No tables inside database: '{database}'")
        else:
            logger.info(f"Retrieved tables from database '{database}' successfully")

        return table_names
    except Error as e:
        logger.exception(f"Error while fetching tables from MySQL database '{database}': {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_schema(host:str, user:str, password:str, database:str, port:int=3306) -> Optional[Dict[str, list]]:
    """
    Retrieves the schema of a given MySQL database as a dictionary.

    Args:
        host (str): The host address of the MySQL server.
        user (str): The username to authenticate with.
        password (str): The password for the MySQL user.
        database (str): The name of the database to retrieve the schema from.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[Dict[str, list]]: A dictionary where keys are table names and values are lists of column definitions.
        Returns None if the connection or table retrieval fails.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host=host, user=user, password=password, database=database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database : '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor(dictionary=True)

        tables = get_tables(host=host, user=user, password=password, database=database, port=port)
        if not tables:
            logger.error(f"Failed to fetch tables from database")   
            return None
        schema = {}

        
        for table_name in tables:
            cursor.execute(f"DESCRIBE {table_name}")
            columns:list = cursor.fetchall()
            
            column_info = []
            for column in columns:
                column_properties:dict = {}
                column_properties['Data Type'] = column['Type']
                column_properties['Nullable'] = True if column['Null'] == 'YES' else False
                column_properties['Default'] = column['Default']
    
                column_info.append({
                    "column_name": column['Field'],
                    "properties": column_properties
                })

            schema[table_name] = column_info
        
        logger.info(f"Schema retrieval completed for database: '{database}'")
        return schema
    
    except Error as e:
        logger.error(f"An error occurred while retrieving schema: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
def get_table_description(host:str, user: str, password:str, database:str, table_name:str, port:int=3306) -> Optional[Dict[str, list]]:
    """
    Retrieves the schema of a specific table from a given MySQL database.

    Args:
        host (str): The host address of the MySQL server.
        user (str): The username to authenticate with.
        password (str): The password for the MySQL user.
        database (str): The name of the database containing the table.
        table_name (str): The name of the table to retrieve the schema from.
        port (int): The port number of the MySQL server.

    Returns:
        Optional[Dict[str, list]]: A dictionary where the key is the table name and the value is a list of column definitions.
        Returns None if the connection or schema retrieval fails.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_mysql(host=host, user=user, password=password, database=database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database : '{database}'")
            return None
        cursor = connection.cursor(dictionary=True)

        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        table_description = {}
        column_info = []
        for column in columns:
            column_properties:dict = {}
            column_properties['Data Type'] = column['Type']
            column_properties['Nullable'] = True if column['Null'] == 'YES' else False
            column_properties['Default'] = column['Default']

            column_info.append({
                "column_name": column['Field'],
                "properties": column_properties
            })

        table_description[table_name] = column_info

        logger.info(f"Description fetched for table: '{table_name}'")
        return table_description
    except Error as e:
        logger.error(f"An error occurred while retrieving table description: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()