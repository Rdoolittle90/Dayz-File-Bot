"""
Module for connecting to a MySQL database using environment variables.

Attributes:
- pool (aiomysql.Pool): A pool of connections to the database.
- is_connected (bool): Indicates whether or not the connection to the database has been established.

Methods:
- sql_connect() -> None:
    Connects to the MySQL database using environment variables.
- sql_disconnect() -> None:
    Closes the connection to the MySQL database.
- sql_execute(query: str, *args) -> List[Tuple]:
    Executes the given SQL query and returns the result.
"""

from os import getenv
from typing import List, Tuple

import aiomysql
from pymysql import err

from src.helpers.colored_printing import colorized_print


class DBConnect:
    """
    Class for handling connection to MySQL database
    """

    def __init__(self) -> None:
        self.pool: aiomysql.Pool = None
        self.is_connected = False
        colorized_print("DEBUG", "DBConnect has been initialized")


    async def sql_connect(self) -> None:
        """
        Connects to the MySQL database using environment variables
        """
        try:
            self.pool = await aiomysql.create_pool(
                host=getenv("SQL_HOST"),
                port=int(getenv("SQL_PORT")),
                user=getenv("SQL_USER"),
                password=getenv("SQL_PASSWORD"),
                db=getenv("SQL_DB"),
                autocommit=True,
                max_idle_time=3600,  # Close idle connections after 1 hour (3600 seconds)
                max_lifetime=86400  # Close connections after 24 hours (86400 seconds)
            )
            self.is_connected = True
            colorized_print("INFO", "Successfully Connected to SQL server")
        except err.OperationalError:
            colorized_print("ERROR", "Failed to connect to SQL server")


    async def sql_disconnect(self) -> None:
        """
        Closes the connection to the MySQL database
        """
        self.pool.close()
        await self.pool.wait_closed()
        colorized_print("DEBUG", "Connection to SQL server closed")


    async def sql_execute(self, query: str, *args) -> List[Tuple]:
        """
        Executes the given SQL query and returns the result

        Args:
            query (str): The SQL query to execute
            *args: Optional arguments to pass to the query

        Returns:
            List of tuples containing the result of the query,
            or None if the query returns no result
        """
        colorized_print("DEBUG", "Execute SQL query")
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                result: List[Tuple] = await cur.fetchall()
                if result:
                    colorized_print("DEBUG", f"   SQL query result {result}")
                    return result
                else:
                    colorized_print("DEBUG", f"   SQL query result None")
                    return None
