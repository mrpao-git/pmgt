import mysql.connector

from typing import Any
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

connection: PooledMySQLConnection | MySQLConnectionAbstract | None = None

class InitializingFailure(Error, FileNotFoundError, PermissionError):
    pass

class TableFailure(Error):
    pass

class Object:
    def __init__(self) -> None:
        self.__name__ = self.__class__.__name__

    def __str__(self) -> str:
        return self.__name__

class Cell(Object):
    _column: str | None = None
    _value: str | int | None = None
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return str(self._value)

class Row(Object):
    _cells: list[Cell] = []
    def __init__(self) -> None:
        super().__init__()

    def get(self, name: str) -> Cell | None:
        for cell in self._cells:
            if cell._column == name:
                return cell
        return None
        
    def hasAccount(self, account: str) -> bool:
        for cell in self._cells:
            if cell._column == 'Account' and cell._value == account:
                return True
        return False

class Table(Object):
    _rows: list[Row] = []
    def __init__(self) -> None:
        super().__init__()

    def who(self, account: str) -> Row | None:
        for row in self._rows:
            if row.hasAccount(account):
                return row

def init() -> None:
    global connection
    try:
        connection = mysql.connector.connect(
            host     = 'localhost',
            user     = 'root',
            password = None,
            database = 'pmgt'
        )
        with open('tables.sql', 'r') as sql:
            for query in sql.read().split(';'):
                if connection is not None:
                    connection.cursor().execute(query.strip())
        connection.commit()
    except Error as error:
        raise InitializingFailure(
            msg      = error.msg,
            errno    = error.errno,
            sqlstate = error.sqlstate
        )
    except (FileNotFoundError, PermissionError) as error:
        raise InitializingFailure(errno=error.errno)

def table(__table__) -> type[Table]:
    name: str = __table__.__name__
    try:
        init()
        columns: list[Any] = []
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {name}')
            if cursor.description is not None:
                columns.extend([description[0] for description in cursor.description])
            for row in cursor.fetchall():
                rows = Row()
                for column, value in zip(columns, row):
                    cell = Cell()
                    cell._column = column
                    cell._value  = value.__str__()
                    rows._cells.append(cell)
                __table__._rows.append(rows)
    except InitializingFailure as error:
        raise TableFailure(
            msg      = error.msg,
            errno    = error.errno,
            sqlstate = error.sqlstate
        )
    return __table__
