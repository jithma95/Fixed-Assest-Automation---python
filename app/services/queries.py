from .database import Database

class Query(object):
    _cnxn = None
    def __init__(self):
        db = Database()
        self._cnxn = db.conn()

    def bulkInsertToFact(self):
        cursor = self._cnxn.cursor()
        cursor.execute("INSERT INTO [DB_FACT_FAR_Tax_Maintenance] ([Entity], [Asset_ID], [Asset_Desc],[Asset_Ctgy], [Cap_Date], [Opening_Cost], [Increase/Decrease_cost_base], [Disposal_Date], [Effc_Life], [Dpn_Method], [Dpn_Rate], [Prior_Year_WDV]) \
                SELECT \
                    CAST( [Entity] AS NCHAR(10)) AS [Entity],\
                    CONVERT(INT,\
                            CASE\
                            WHEN IsNumeric(CONVERT(VARCHAR(12),  [Asset_ID])) = 1 THEN CONVERT(VARCHAR(12), [Asset_ID])\
                            ELSE 0 END)  as [Asset_ID],\
                    CAST( [Asset_Desc] AS NVARCHAR(MAX)) AS [Asset_Desc],\
                    CAST( [Asset_Ctgy] AS NVARCHAR(MAX)) AS [Asset_Ctgy],\
                    CONVERT(DATE,\
                            CASE\
                            WHEN IsDate([Cap_Date]) = 1 THEN CONVERT(DATE, [Cap_Date])\
                            ELSE GETDATE() END)  as [Cap_Date],\
                    CONVERT(NUMERIC(18,2),\
                            CASE\
                            WHEN IsNumeric(CONVERT(VARCHAR(MAX),  [Opening_Cost])) = 1 THEN CONVERT(NUMERIC(18,2), [Opening_Cost])\
                            ELSE 0.00 END) as [Opening_Cost],\
                    CONVERT(NUMERIC(18,2),\
                            CASE\
                            WHEN IsNumeric(CONVERT(VARCHAR(MAX),  [Increase/Decrease cost base])) = 1 THEN CONVERT(NUMERIC(18,2), [Increase/Decrease cost base])\
                            ELSE 0.00 END) as [Increase/Decrease cost base],\
                    CONVERT(DATE,\
                            CASE\
                            WHEN IsDate([Disposal_Date]) = 1 THEN CONVERT(DATE, [Disposal_Date])\
                            ELSE GETDATE() END)  as [Disposal_Date],\
                    CONVERT(NUMERIC(18,2),\
                            CASE\
                            WHEN IsNumeric(CONVERT(VARCHAR(MAX),  [Effc_Life])) = 1 THEN CONVERT(NUMERIC(18,2), [Effc_Life])\
                            ELSE 0.00 END) as [Effc_Life],\
                    CAST( [Dpn_Method] AS VARCHAR(50)) AS [Dpn_Method],\
                    CONVERT(NUMERIC(18,2),\
                            CASE\
                            WHEN IsNumeric(CONVERT(VARCHAR(MAX),  [Dpn_Rate])) = 1 THEN CONVERT(NUMERIC(18,2), [Dpn_Rate])\
                            ELSE 0.00 END) as [Dpn_Rate],\
                    CONVERT(NUMERIC(18,2),\
                            CASE\
                            WHEN IsNumeric(CONVERT(VARCHAR(MAX),  [Prior Year WDV])) = 1 THEN CONVERT(NUMERIC(18,2), [Prior Year WDV])\
                            ELSE 0.00 END) as [Prior Year WDV]\
                FROM [Dim_B_RAW_FAR_Tax_Maintenance] ;")

        self._cnxn.commit()
        return True


    def truncateRawTable(self):
        cursor = self._cnxn.cursor()
        cursor.execute("TRUNCATE TABLE [dbo].[Dim_B_RAW_FAR_Tax_Maintenance]")
        self._cnxn.commit()
        return True

    def truncateFactTable(self):
        cursor = self._cnxn.cursor()
        cursor.execute("TRUNCATE TABLE [dbo].[DB_FACT_FAR_Tax_Maintenance]")
        self._cnxn.commit()
        return True

    def fetchRecords(self):
        cursor = self._cnxn.cursor()
        cursor.execute("SELECT TOP 100 * FROM [DB_FACT_FAR_Tax_Maintenance]")
        data = cursor.fetchall()
        return data

    def getRowCount(self):
        cursor = self._cnxn.cursor()
        cursor.execute("SELECT COUNT(*) AS count FROM [DB_FACT_FAR_Tax_Maintenance]")
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

        return results

    def paginations(self, length, start):
        cursor = self._cnxn.cursor()
        cursor.execute("SELECT *\
                        FROM [dbo].[DB_FACT_FAR_Tax_Maintenance]\
                        ORDER BY Entity ASC\
                        OFFSET "+str(start)+" ROWS FETCH NEXT "+str(length)+" ROWS ONLY")
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

        return results