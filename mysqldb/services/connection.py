from mysql.connector import connect, Error, MySQLConnection
from config.logger_config import LoggerFactory
from typing import Optional

# Set up logger for this module
logger = LoggerFactory.get_logger(__name__)

def connect_to_mysql(host:str, user:str, password:str, database:str, port:int = 3306) -> Optional[MySQLConnection]:
    """
    Establishes a connection to a MySQL database.

    Args:
        host (str): The host address of the MySQL server.
        user (str): The username to authenticate with.
        password (str): The password for the MySQL user.
        database (str): The name of the database to connect to.
        port (int): The port number of the MySQL server. Defaults to 3306.

    Returns:
        Optional[MySQLConnection]: A MySQLConnection object if the connection is successful, otherwise None.
    """
    try:
        connection = connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        if connection.is_connected():
            logger.info(f"Successfully connected to MySQL database '{database}' on port {port} as user '{user}'")
            return connection
        else:
            logger.error(f"Failed to connect to MySQL database '{database}' on port {port}")
            return None
    except Error as e:
        logger.error(f"Error while connecting to MySQL database '{database}' on port {port}: {str(e)}")
        return None