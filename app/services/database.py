import pyodbc

class Database(object):
    _cnxn = None

    def conn(self):
        password = 'P@ssword'
        self._cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:kpmg-poc.database.windows.net,1433;Database=kpmg-poc;Uid=jithma;Pwd=' +
                                password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        return self._cnxn