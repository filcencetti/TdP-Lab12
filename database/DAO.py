from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getRetailers():
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM go_retailers"""
        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year,country):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor()
        query = """select distinct 
                        gds1.Retailer_code, 
                        gds2.Retailer_code, 
                        count(distinct gds1.Product_number)
                    from go_daily_sales gds1, go_daily_sales gds2, go_retailers gr1, go_retailers gr2
                    where 
                        year(gds1.Date) = %s and year(gds2.Date) = %s 
                        and gds1.Product_number = gds2.Product_number 
                        and gds1.Retailer_code != gds2.Retailer_code
                        and gds1.Retailer_code = gr1.Retailer_code
                        and gds2.Retailer_code = gr2.Retailer_code
                        and gr1.Country = %s and gr2.Country = %s
                    group by gds1.Retailer_code, gds2.Retailer_code"""
        cursor.execute(query,(year,year,country,country))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result


