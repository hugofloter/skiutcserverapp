from config import DB_NAME, DB_USER, DB_PWD, DB_HOST
import pymysql
from pymysql.cursors import Cursor
from pymysql.connections import Connection


class CustomConnection(Connection):
    def cursor(self, cursor=None, Model=None):
        """
        custom method to implement model in cursorclass
        """
        if cursor:
            return cursor(self)
        if Model is None:
            return self.cursorclass(self)
        return self.cursorclass(self, Model=Model)


class CustomCursor(Cursor):
    def __init__(self, connection, Model=None):
        self.connection = connection
        self.description = None
        self.rownumber = 0
        self.rowcount = -1
        self.arraysize = 1
        self._executed = None
        self._result = None
        self._rows = None
        self.Model = Model

    def fetchone(self):
        """Fetch the next row"""
        self._check_executed()
        if self._rows is None or self.rownumber >= len(self._rows):
            return None
        result = self._rows[self.rownumber]
        self.rownumber += 1
        if self.Model:
            description = self.description
            if description:
                dict_result = { description[i][0]: attr for i, attr in enumerate(result) }
                return self.Model(dict_result)
            return self.Model(result)
        return result

    def fetchall(self):
        """Fetch all the rows"""
        self._check_executed()
        if self._rows is None:
            return ()
        if self.rownumber:
            if self.Model:
                description = self.description
                if description:
                    list_values = [{description[i][0]: attr for i, attr in enumerate(value)} for value in self._rows[self.rownumber:]]
                    result = [self.Model(value) for value in list_values]
                else:
                    result = [self.Model(value) for value in self._rows[self.rownumber:]]
            else:
                result = self._rows[self.rownumber:]
        else:
            if self.Model:
                description = self.description
                if description:
                    list_values = [{description[i][0]: attr for i, attr in enumerate(value)} for value in self._rows]
                    result = [self.Model(value) for value in list_values]
                else:
                    result = [self.Model(value) for value in self._rows]
            else:
                result = self._rows

        self.rownumber = len(self._rows)
        return result


def dbskiutc_con():
    con = CustomConnection(
        host=DB_HOST,
        db=DB_NAME,
        user=DB_USER,
        password=DB_PWD,
        charset='utf8mb4',
        cursorclass=CustomCursor
    )

    return con


if __name__ == '__main__':
    _main(sys.argv)
