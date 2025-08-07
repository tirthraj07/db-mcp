from mysqldb.services.connection import connect_to_mysql
from config.logger_config import LoggerFactory

from typing import Dict, Optional, List, Any
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
from mysql.connector import Error

logger = LoggerFactory.get_logger(__name__)

def get_all_rows(host: str, user: str, password: str, database: str, table_name: str, port: int = 3306) -> Optional[List[Dict]]:
    """
    Retrieves all rows from the specified table in the given database.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The name of the database.
        table_name (str): The name of the table to fetch data from.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[Dict]]: A list of dictionaries where each dictionary represents a row from the table.
        Returns None if an error occurs or the table is empty.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host=host, user=user, password=password, database=database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database: '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor(dictionary=True)
        
        query = f"SELECT * FROM {table_name};"
        logger.info(f"Executing query: {query}")
        cursor.execute(query)
        
        rows: List[Dict] = cursor.fetchall()
        if not rows:
            logger.warning(f"No data found in table '{table_name}'")
            return []

        logger.info(f"Successfully fetched {len(rows)} rows from '{table_name}'")
        return rows

    except Error as e:
        logger.error(f"Error occurred while fetching data from '{table_name}': {str(e)}")
        return None

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            logger.info("Database connection closed.")
        except Exception as ex:
            logger.error(f"Error while closing resources: {str(ex)}")

def get_filtered_rows(
    host: str, user: str, password: str, database: str, table_name: str, filters: Dict[str, Any], port: int = 3306
) -> Optional[List[Dict]]:
    """
    Retrieves rows from the specified table in the given database based on filter criteria.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The name of the database.
        table_name (str): The name of the table to fetch data from.
        filters (Dict[str, Any]): A dictionary where keys are column names and values are the filtering criteria.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[Dict]]: A list of dictionaries where each dictionary represents a row from the table.
        Returns None if an error occurs or no data matches the filters.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host=host, user=user, password=password, database=database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database: '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor(dictionary=True)

        where_clauses = [f"`{key}` = %s" for key in filters.keys()]
        where_statement = " AND ".join(where_clauses)

        query = f"SELECT * FROM {table_name} WHERE {where_statement};"
        values = list(filters.values())
        logger.info(f"Executing query: {query} with values {values}")

        cursor.execute(query, values)

        rows: List[Dict] = cursor.fetchall()
        if not rows:
            logger.warning(f"No data found in table '{table_name}' with filters: {filters}")
            return []

        logger.info(f"Successfully fetched {len(rows)} rows from '{table_name}'")
        return rows

    except Error as e:
        logger.error(f"Error occurred while fetching filtered data from '{table_name}': {str(e)}")
        return None

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            logger.info("Database connection closed.")
        except Exception as ex:
            logger.error(f"Error while closing resources: {str(ex)}")

def get_sorted_rows(
    host: str, user: str, password: str, database: str, table_name: str, sort_by: str, order: str = 'ASC', port: int = 3306
) -> Optional[List[Dict]]:
    """
    Retrieves sorted rows from the specified table.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The table name.
        sort_by (str): The column to sort by.
        order (str): The sort order ('ASC' or 'DESC'). Default is 'ASC'.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[Dict]]: Sorted rows as a list of dictionaries, or None on error.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host, user, password, database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database: '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor(dictionary=True)

        query = f"SELECT * FROM {table_name} ORDER BY `{sort_by}` {order};"
        logger.info(f"Executing query: {query}")

        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except Error as e:
        logger.error(f"Error fetching sorted rows from '{table_name}': {str(e)}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_limited_rows(
    host: str, user: str, password: str, database: str, table_name: str, limit: int, offset: int = 0, port: int = 3306
) -> Optional[List[Dict]]:
    """
    Retrieves a limited number of rows from the specified table.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The table name.
        limit (int): The number of rows to fetch.
        offset (int): The starting point for fetching rows. Default is 0.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[Dict]]: Limited rows as a list of dictionaries, or None on error.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host, user, password, database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database: '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor(dictionary=True)

        query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s;"
        logger.info(f"Executing query: {query}")

        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()
        return rows

    except Error as e:
        logger.error(f"Error fetching limited rows from '{table_name}': {str(e)}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_distinct_values(
    host: str, user: str, password: str, database: str, table_name: str, column: str, port: int = 3306
) -> Optional[List[Any]]:
    """
    Retrieves distinct values from a specific column in the given table.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The table name.
        column (str): The column name.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[Any]]: A list of distinct values or None on error.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host, user, password, database, port=port)
        if not connection:
            logger.error(f"Failed to connect to database: '{database}'")
            return None

        cursor: MySQLCursor = connection.cursor()

        query = f"SELECT DISTINCT `{column}` FROM {table_name};"
        logger.info(f"Executing query: {query}")

        cursor.execute(query)
        values = [row[0] for row in cursor.fetchall()]
        return values

    except Error as e:
        logger.error(f"Error fetching distinct values from '{table_name}': {str(e)}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_aggregated_data(
    host: str, user: str, password: str, database: str, table_name: str, aggregation: str, column: str, port: int = 3306
) -> Optional[Any]:
    """
    Retrieves aggregated data from a specified column in the given table.

    Args:
        aggregation (str): The aggregation function (e.g., COUNT, SUM, AVG).
        column (str): The column name.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[Any]: The result of the aggregation or None on error.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host, user, password, database, port=port)
        if not connection:
            return None
        cursor: MySQLCursor = connection.cursor()

        query = f"SELECT {aggregation}(`{column}`) FROM {table_name};"
        logger.info(f"Executing query: {query}")

        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

    except Error as e:
        logger.error(f"Error in aggregation on '{table_name}': {str(e)}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_grouped_data(
    host: str, user: str, password: str, database: str, table_name: str, group_by: str, aggregation: str, column: str, port: int = 3306
) -> Optional[Dict[str, Any]]:
    """
    Groups data by a specified column and applies an aggregation function.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to query.
        group_by (str): The column to group by.
        aggregation (str): The aggregation function (e.g., SUM, AVG).
        column (str): The column to aggregate.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[Dict[str, Any]]: A dictionary where keys are group values and values are aggregated data,
        or None if an error occurs.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host, user, password, database, port=port)
        if not connection:
            return None
        cursor: MySQLCursor = connection.cursor(dictionary=True)

        query = f"SELECT `{group_by}`, {aggregation}(`{column}`) AS aggregate FROM {table_name} GROUP BY `{group_by}`;"
        logger.info(f"Executing query: {query}")

        cursor.execute(query)
        results = cursor.fetchall()
        return {row[group_by]: row['aggregate'] for row in results}

    except Error as e:
        logger.error(f"Error fetching grouped data from '{table_name}': {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def execute_custom_query(host: str, user: str, password: str, database: str, query: str, port: int = 3306) -> Optional[List[Dict]]:
    """
    Executes a custom SQL query and returns the result as a list of dictionaries.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        query (str): The SQL query to execute.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[List[Dict]]: The result of the query as a list of dictionaries, or None if an error occurs.
    """
    connection = None
    cursor = None
    try:
        connection: MySQLConnection = connect_to_mysql(host, user, password, database, port=port)
        if not connection:
            return None
        cursor: MySQLCursor = connection.cursor(dictionary=True)

        logger.info(f"Executing custom query: {query}")
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except Error as e:
        logger.error(f"Error executing custom query: {str(e)}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()