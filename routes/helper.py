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