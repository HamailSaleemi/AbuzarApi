from pkg_resources import resource_listdir

from DATABASE import connection
SQL_CONN = connection.SQL_CONN
from decimal import Decimal
from datetime import datetime, timedelta

def get_date_for_month():
    now = datetime.now()
    day30 = now.strftime('%Y-%m-%d 23:59:59')
    # Subtract 30 days
    date_30_days_ago = now - timedelta(days=30)
    # Format as 'YYYY-MM-DD 00:00:00'
    day1 = date_30_days_ago.strftime('%Y-%m-%d 00:00:00')
    return day1, day30
def get_item_detail_by_aliasname(aliasname):
    query = ("""
    SELECT i.ICode, i.CustomICode, i.Name, i.SalePrice, ISNULL(g.CurrQty, 0) AS CurrQty
    FROM Item i
    LEFT JOIN GodownDetail g ON i.ICode = g.ICode
    WHERE i.CustomICode = ?

    UNION

    SELECT i.ICode, a.CustomICode, i.Name, i.SalePrice, ISNULL(g.CurrQty, 0) AS CurrQty
    FROM AlternateItemAlias a
    JOIN Item i ON a.ICode = i.ICode
    LEFT JOIN GodownDetail g ON i.ICode = g.ICode
    WHERE a.CustomICode = ?;
    """)
    # print(query)
    params = (aliasname, aliasname)
    result = SQL_CONN.execute_query(query, params)
    return result


def get_item_sale(ICode):

    con = connection.SQL_CONN
    d1, d2 = get_date_for_month()
    query = ('select SaleLedger.SaleInvCode, SaleLedger.date, Saledetail.Icode, Saledetail.SalePrice, Saledetail.PackUnits, Saledetail.LooseQty from Saledetail'
             ' inner join SaleLedger on Saledetail.SaleInvCode = SaleLedger.SaleInvCode where SaleLedger.date > ? and SaleLedger.date < ? and Saledetail.ICode = ?;')

    data = con.execute_query(query, (d1, d2, ICode))
    result = []
    totalSold = 0
    print(d1)
    print(d2)
    for row in data:
        totalSold = int(row[4]) * int(row[5]) + totalSold
        result.append({
            'SaleInvCode': row[0],
            'date': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'Icode': row[2],
            'SalePrice': str(row[3]),
            'PackUnits': row[4],
            'QtySold':str(row[5])
        })
    return result, totalSold



def item_purchase(ICode):
    print('Alis code is', ICode)
    con = connection.SQL_CONN
    d1, d2 = get_date_for_month()
    query = """SELECT 
    purledger.purinvcode as PurchaseInvoice,
    accounts.name as SuppliserName,
    CONVERT(VARCHAR(10), purledger.date, 120) AS Date,  -- Convert to 'YYYY-MM-DD' format
    item.customicode as AliasName,
    AlternateItemAlias.customicode as AlterAliasName,
    item.name as  ItemName,
    AlternateItemAlias.qty AlterPack,
    purdetail.purprice As PurchasePrice,
    item.saleprice as SalePrice
    FROM purdetail  
    LEFT JOIN purledger ON purledger.purinvcode = purdetail.purinvcode
    LEFT JOIN accounts ON accounts.acccode = purledger.suppcode
    LEFT JOIN item ON item.icode = purdetail.icode
    LEFT JOIN AlternateItemAlias ON AlternateItemAlias.icode = item.icode
    WHERE 
        (item.customicode = ? OR AlternateItemAlias.customicode = ?) order by Date desc;"""

    data = con.execute_query(query, (ICode, ICode))
    result = []
    print(d1)
    print(d2)
    for row in data:
        result.append({
        'PurchaseInvoice': row[0],
        'SuppliserName': row[1],
        'Date': row[2],
        'AliasName': row[3],
        'AlterAliasName': row[4],
        'ItemName': row[5],
        'AlterPack': row[6],
        'PurchasePrice': float(row[7]),
        'SalePrice': float(row[8])
        })
    print(result)
    return result


def Get_Supplier_Name():

    con = connection.SQL_CONN
    # d1, d2 = get_date_for_month()
    query = ("select Acccode,AliasName, Name from accounts where subcode=7 and active='Y'")
    data = con.execute_query(query)
    result = []
    for row in data:
        result.append({
            'Acccode': row[0],
            'AliasName': row[1],
            'Name': row[2]
        })
    return result


def Get_Supplier_wise_item(params1:str,params2:str):

    con = connection.SQL_CONN
    # d1, d2 = get_date_for_month()
    query = ("""SELECT 
                    ISNULL(s.icode, r.icode) AS icode,
                    ISNULL(s.customicode, r.customicode) AS customicode,
                    ISNULL(s.Name, r.Name) AS Name,

                    ISNULL(s.Sale_Till_15_Days_Ago, 0) - ISNULL(r.Sale_Till_15_Days_Ago, 0) AS Net_Sale_Till_15_Days_Ago,
                    ISNULL(s.Sale_Last_15_Days, 0) - ISNULL(r.Sale_Last_15_Days, 0) AS Net_Sale_Last_15_Days,
                    ISNULL(s.Total_30_Days_Sale, 0) AS Net_sale_30_day,

                    ISNULL(r.Sale_Till_15_Days_Ago, 0) AS Return_Till_15_Days_Ago,
                    ISNULL(r.Sale_Last_15_Days, 0) AS Return_Last_15_Days,
                ISNULL(r.Total_30_Days_Sale, 0) AS Net_Return_30_day,
                    ISNULL(s.Total_30_Days_Sale, 0) - ISNULL(r.Total_30_Days_Sale, 0) AS Net_Total_30_Days_Sale

                FROM 
                (
                    SELECT 
                        saledetail.icode,
                        customicode,
                        item.Name,
                        SUM(CASE 
                                WHEN saleledger.date >= DATEADD(day, -30, GETDATE()) 
                                    AND saleledger.date < DATEADD(day, -15, GETDATE()) 
                                THEN saledetail.looseqty ELSE 0 END) AS Sale_Till_15_Days_Ago,
                        SUM(CASE 
                                WHEN saleledger.date >= DATEADD(day, -15, GETDATE()) 
                                    AND saleledger.date <= GETDATE()
                                THEN saledetail.looseqty ELSE 0 END) AS Sale_Last_15_Days,
                        SUM(saledetail.looseqty) AS Total_30_Days_Sale
                    FROM saledetail
                    INNER JOIN item ON item.icode = saledetail.icode
                    INNER JOIN saleledger ON saleledger.saleinvcode = saledetail.saleinvcode
                    INNER JOIN itemsuppliers ON itemsuppliers.icode = item.icode
                    INNER JOIN Accounts ON Accounts.acccode = itemsuppliers.suppcode
                    WHERE saleledger.date >= DATEADD(day, -30, GETDATE())
                    AND saleledger.date <= GETDATE()
                    AND itemsuppliers.suppcode = (
                        SELECT acccode FROM Accounts WHERE Name = ?
                    )
                    GROUP BY saledetail.icode, customicode, item.Name
                ) AS s

                FULL OUTER JOIN
                (
                    SELECT 
                        srdetail.icode,
                        customicode,
                        item.Name,
                        SUM(CASE 
                                WHEN srledger.date >= DATEADD(day, -30, GETDATE()) 
                                    AND srledger.date < DATEADD(day, -15, GETDATE()) 
                                THEN srdetail.looseqty ELSE 0 END) AS Sale_Till_15_Days_Ago,
                        SUM(CASE 
                                WHEN srledger.date >= DATEADD(day, -15, GETDATE()) 
                                    AND srledger.date <= GETDATE()
                                THEN srdetail.looseqty ELSE 0 END) AS Sale_Last_15_Days,
                        SUM(srdetail.looseqty) AS Total_30_Days_Sale
                    FROM srdetail
                    INNER JOIN item ON item.icode = srdetail.icode
                    INNER JOIN srledger ON srledger.srinvcode = srdetail.srinvcode
                    INNER JOIN itemsuppliers ON itemsuppliers.icode = item.icode
                    INNER JOIN Accounts ON Accounts.acccode = itemsuppliers.suppcode
                    WHERE srledger.date >= DATEADD(day, -30, GETDATE())
                    AND srledger.date <= GETDATE()
                    AND itemsuppliers.suppcode = (
                        SELECT acccode FROM Accounts WHERE Name = ?
                    )
                    GROUP BY srdetail.icode, customicode, item.Name
                ) AS r

                ON s.icode = r.icode AND s.customicode = r.customicode

                ORDER BY Name ASC;


                                                                        """)
    
    data = con.execute_query(query,(params1,params2))
    result = []
    for row in data:
        print(row)
        result.append({
            'icode': row[0],
            'customicode': row[1],
            'Name': row[2],
            'Net_Sale_Till_15_Days_Ago': float(row[3]),
            'Net_Sale_Last_15_Days': float(row[4]),
            'Net_sale_30_day': float(row[5]),
            'Return_Till_15_Days_Ago': float(row[6]),
            'Return_Last_15_Days': float(row[7]),
            'Net_Return_30_day': float(row[8]),
            'Net_Total_30_Days_Sale': float(row[9])
        })
    return result