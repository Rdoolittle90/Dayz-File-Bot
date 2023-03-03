import aiomysql
from os import getenv
from typing import List, Tuple

from pymysql import err

class DBConnect:
    """
    Class for handling connection to MySQL database
    """

    def __init__(self) -> None:
        self.pool: aiomysql.Pool = None


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
                autocommit=True
            )
        except err.OperationalError:
            print(f"Failed to connect to SQL server")


    async def sql_disconnect(self) -> None:
        """
        Closes the connection to the MySQL database
        """
        self.pool.close()
        await self.pool.wait_closed()


    async def sql_execute(self, query: str, *args) -> List[Tuple]:
        """
        Executes the given SQL query and returns the result

        Args:
            query (str): The SQL query to execute
            *args: Optional arguments to pass to the query

        Returns:
            List of tuples containing the result of the query, or None if the query returns no result
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                result: List[Tuple] = await cur.fetchall()
                if result:
                    return result
                else:
                    return None