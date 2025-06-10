from logging import Logger
from src.utils.logger import logging_config
from src.utils.database.database import Database
from typing import Sequence, Mapping, Type, Optional
from psycopg.rows import dict_row, Row

class BaseDAO:
    def __init__(self, db=None):
        self.logger: Logger = logging_config.get_logger(__name__)
        self.db = db
        if not db:
            self.logger.warning("No database connection provided, using default.")
            self.db = Database()

    def query(
            self, 
            query: str, 
            params: Sequence[any] | Mapping[str,any] = (), 
            row_factory: Type[Row | None] = dict_row
    ) -> list[Row]:
        """
        execute a SELECT query and return the results as a list of rows.
        """
        rows: list[Row] = []
        conn = None
        try:
            conn = self.db.get_connection()
            with conn.cursor(row_factory=row_factory) as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            if conn:
                conn.rollback()
                raise e
        finally:
            if conn:
                conn.close()
        return rows

    def update(
            self,
            query: str,
            params: Sequence[any] | Mapping[str, any] = ()
    ) -> Row | None:
        """
        execute an UPDATE | INSERT | DELETE query and return the updated row.
        """
        result : Optional[Row] = None
        conn = None
        try:
            conn = self.db.get_connection()
            with conn.cursor(row_factory=dict_row) as cursor:
                self.logger.debug(f"Executing update query: {query} with params: {params}")
                cursor.execute(query, params)
                if query.strip().upper().startswith("INSERT") or "RETURNING" in query.upper():
                        result = cursor.fetchone()
                conn.commit()
        except Exception as e:
            self.logger.error(f"Error executing update: {e}")
            if conn:
                conn.rollback()
                raise e
        finally:
            if conn:
                conn.close()
        return result