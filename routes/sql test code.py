from DATABASE import connection

con = connection.SQL_CONN

query = ('select SaleLedger.SaleInvCode, SaleLedger.date, Saledetail.Icode, Saledetail.SalePrice from Saledetail'
         ' inner join SaleLedger on Saledetail.SaleInvCode = SaleLedger.SaleInvCode where SaleLedger.date > ? and Saledetail.ICode = ?;')

data =  con.execute_query(query, ('2025-03-15 00:00:00', '101012'))

for row in data:
    print(row)