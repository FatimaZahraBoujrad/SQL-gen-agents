import sqlite3
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, TokenList
from sqlparse.tokens import Keyword, DML
from typing import Tuple, Union, List, Dict


class SQLValidationError(Exception):
    """Raised when an SQL query is deemed unsafe or invalid."""
    pass


def validate_sql_query(sql: str) -> str:
    """
    Validates the given SQL query to ensure it's a safe SELECT statement only.

    Returns the cleaned SQL string if valid. Raises SQLValidationError otherwise.
    """

    parsed = sqlparse.parse(sql)
    if not parsed or len(parsed) != 1:
        raise SQLValidationError("Only a single SQL statement is allowed.")

    statement = parsed[0]
    if statement.get_type() != "SELECT":
        raise SQLValidationError("Only SELECT queries are allowed.")

    # Detect presence of dangerous keywords
    forbidden_keywords = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "REPLACE", "EXEC", "ATTACH"}
    for token in statement.tokens:
        if token.ttype is Keyword and token.normalized.upper() in forbidden_keywords:
            raise SQLValidationError(f"Forbidden SQL keyword found: {token.normalized}")

    # Optional: enforce LIMIT clause to prevent large queries
    """if "limit" not in sql.lower():
        raise SQLValidationError("SELECT queries must include a LIMIT clause to avoid heavy loads.")"""

    return sql.strip()


def execute_safe_sql(sql: str, db_path: str) -> Dict:
    """
    Validates and executes a safe SQL SELECT query against a SQLite database.

    Parameters:
        sql (str): The SQL query (must be validated SELECT).
        db_path (str): Path to the SQLite database file.

    Returns:
        dict: Structured result or error message.
    """

    try:
        validated_sql = validate_sql_query(sql)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(validated_sql)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

        return {
            "status": "success",
            "columns": column_names,
            "rows": rows
        }

    except SQLValidationError as ve:
        return {
            "status": "error",
            "error_type": "validation",
            "message": str(ve)
        }

    except sqlite3.Error as db_err:
        return {
            "status": "error",
            "error_type": "database",
            "message": str(db_err)
        }

    except Exception as ex:
        return {
            "status": "error",
            "error_type": "internal",
            "message": str(ex)
        }
