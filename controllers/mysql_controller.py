from config.mcp_config import mcp
from mysqldb.services.schema import get_schema,get_tables, get_table_description
from mysqldb.services.reads import get_all_rows, get_filtered_rows, get_sorted_rows, get_limited_rows, get_distinct_values, get_aggregated_data, get_grouped_data, execute_custom_query
from mysqldb.services.ddl import create_table, drop_table, show_indexes, create_index
from mysqldb.services.dml import insert_row, insert_multiple_rows, delete_rows, update_rows

from typing import Optional, Dict, List, Any

@mcp.tool()
def mysql_get_tables(host:str, user:str, password:str, database:str, port:int = 3306) -> Optional[List[str]] :
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
    return get_tables(host=host, user=user, password=password, database=database, port=port)

@mcp.tool()
def mysql_get_schema(host:str, user:str, password:str, database:str, port:int = 3306) -> Optional[Dict[str, list]] :
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
    return get_schema(host=host, user=user, password=password, database=database, port=port)

@mcp.tool()
def mysql_get_table_description(host:str, user:str, password:str, database:str, table_name:str, port:int = 3306) -> Optional[Dict[str, list]] :
    """
    Retrieves the schema of a specific table from a given MySQL database.

    Args:
        host (str): The host address of the MySQL server.
        user (str): The username to authenticate with.
        password (str): The password for the MySQL user.
        database (str): The name of the database containing the table.
        table_name (str): The name of the table to retrieve the schema from.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[Dict[str, list]]: A dictionary where the key is the table name and the value is a list of column definitions.
        Returns None if the connection or schema retrieval fails.
    """
    return get_table_description(host=host, user=user, password=password, database=database, table_name=table_name, port=port)

@mcp.tool()
def mysql_get_all_rows(host:str, user:str, password:str, database:str, table_name:str, port:int = 3306) -> Optional[List[Dict]]:
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
    return get_all_rows(host=host, user=user, password=password, database=database, table_name=table_name, port=port)

@mcp.tool()
def mysql_get_filtered_rows(host: str, user: str, password: str, database: str, table_name: str, filters: Dict[str, Any], port: int = 3306) -> Optional[List[Dict]]:
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
    return get_filtered_rows(host, user, password, database, table_name, filters, port=port)

@mcp.tool()
def mysql_get_sorted_rows(host: str, user: str, password: str, database: str, table_name: str, sort_by: str, order: str = 'ASC', port: int = 3306)  -> Optional[List[Dict]]:
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
    return get_sorted_rows(host, user, password, database, table_name, sort_by, order, port=port)

@mcp.tool()
def mysql_get_limited_rows(host: str, user: str, password: str, database: str, table_name: str, limit: int, offset: int = 0, port: int = 3306)  -> Optional[List[Dict]]:
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
    return get_limited_rows(host, user, password, database, table_name, limit, offset, port=port)

@mcp.tool()
def mysql_get_distinct_values(host: str, user: str, password: str, database: str, table_name: str, column: str, port: int = 3306) -> Optional[List[Any]]:
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
    return get_distinct_values(host, user, password, database, table_name, column, port=port)

@mcp.tool()
def mysql_get_aggregated_data(host: str, user: str, password: str, database: str, table_name: str, aggregation: str, column: str, port: int = 3306) -> Optional[Any]:
    """
    Retrieves aggregated data from a specified column in the given table.

    Args:
        aggregation (str): The aggregation function (e.g., COUNT, SUM, AVG).
        column (str): The column name.
        port (int): The port number for the MySQL server.

    Returns:
        Optional[Any]: The result of the aggregation or None on error.
    """
    return get_aggregated_data(host, user, password, database, table_name, aggregation, column, port=port)

@mcp.tool()
def mysql_get_grouped_data(host: str, user: str, password: str, database: str, table_name: str, group_by: str, aggregation: str, column: str, port: int = 3306) -> Optional[Dict[str, Any]]:
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
    return get_grouped_data(host, user, password, database, table_name, group_by, aggregation, column, port=port)

@mcp.tool()
def mysql_create_table(host:str, user:str, password:str, database:str, table_name:str, columns: Dict[str, str], options: Optional[Dict[str, str]] = None, port: int = 3306) -> bool:
    """
    Creates a table with the specified columns and options.
    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to create.
        columns (Dict[str, str]): A dictionary of column names and their data types.
        options (Optional[Dict[str, str]]): Additional options like PRIMARY KEY, AUTO_INCREMENT, UNIQUE, NOT NULL.
        port (int): The port number for the MySQL server.
    Returns:
        bool: True if the table was created successfully, False otherwise.
    """
    return create_table(host, user, password, database, table_name, columns, options, port=port)

@mcp.tool()
def mysql_drop_table(host: str, user: str, password: str, database: str, table_name: str, port: int = 3306) -> bool:
    """
    Drops the specified table.
    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to drop.
        port (int): The port number for the MySQL server.
    Returns:
        bool: True if the table was dropped successfully, False otherwise.
    """
    return drop_table(host, user, password, database, table_name, port=port)

@mcp.tool()
def mysql_show_indexes(host: str, user: str, password: str, database: str, table_name: str, port: int = 3306) -> Optional[List[Dict[str, str]]]:
    """
    Retrieves all indexes from a given table.
    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to retrieve indexes from.
        port (int): The port number for the MySQL server.
    Returns:
        Optional[List[Dict[str, str]]]: A list of dictionaries containing index information, or None if an error occurs.
    """
    return show_indexes(host, user, password, database, table_name, port=port)

@mcp.tool()
def mysql_create_index(host: str, user: str, password: str, database: str, table_name: str, index_name: str, columns: List[str], unique: bool = False, port: int = 3306) -> bool:
    """
    Creates an index on the specified columns of a table.
    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The table to create the index on.
        index_name (str): The name of the index.
        columns (List[str]): A list of column names to be indexed.
        unique (bool): If True, creates a UNIQUE index. Defaults to False.
        port (int): The port number for the MySQL server.
    Returns:
        bool: True if the index was created successfully, False otherwise.
    """
    return create_index(host, user, password, database, table_name, index_name, columns, unique, port=port)

@mcp.tool()
def mysql_insert_row(host:str, user:str, password:str, database:str, table_name:str, data:Dict[str, Any], port: int = 3306) -> bool :
    """
    Inserts a single row into the specified table.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to insert into.
        data (Dict[str, Any]): A dictionary containing column names and their values.
        port (int): The port number for the MySQL server.

    Returns:
        bool: True if the insertion was successful, False otherwise.
    """
    return insert_row(host, user, password, database, table_name, data, port=port)

@mcp.tool()
def mysql_insert_multiple_rows(host: str, user: str, password: str, database: str, table_name: str, data: List[Dict[str, Any]], port: int = 3306) -> bool:
    """
    Inserts multiple rows into the specified table.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to insert into.
        data (List[Dict[str, Any]]): A list of dictionaries, each representing a row to insert.
        port (int): The port number for the MySQL server.

    Returns:
        bool: True if the insertion was successful, False otherwise.
    """
    return insert_multiple_rows(host, user, password, database, table_name, data, port=port)

@mcp.tool()
def mysql_delete_rows(host: str, user: str, password: str, database: str, table_name: str, conditions: Dict[str, Any], port: int = 3306) -> bool:
    """
    Deletes rows from the specified table based on conditions.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to delete from.
        conditions (Dict[str, Any]): A dictionary containing conditions to match for deletion.
        port (int): The port number for the MySQL server.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    return delete_rows(host, user, password, database, table_name, conditions, port=port)

@mcp.tool()
def mysql_update_rows(host: str, user: str, password: str, database: str, table_name: str, data: Dict[str, Any], conditions: Dict[str, Any], port: int = 3306) -> bool:
    """
    Updates rows in the specified table based on conditions.

    Args:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        table_name (str): The name of the table to update.
        data (Dict[str, Any]): A dictionary containing columns and their new values.
        conditions (Dict[str, Any]): A dictionary containing conditions to match for updating.
        port (int): The port number for the MySQL server.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    return update_rows(host, user, password, database, table_name, data, conditions, port=port)

@mcp.tool()
def mysql_execute_custom_query(host: str, user: str, password: str, database: str, query: str, port: int = 3306) -> Optional[List[Dict]]:
    """
    Executes a custom SQL query and returns the result as a list of dictionaries. Only use this if necessary like for complex queries. Reply on built in methods to execute queries.

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
    return execute_custom_query(host, user, password, database, query, port=port)