from fastapi import APIRouter, HTTPException
from DATABASE.connection import SQL_CONN

# Create an APIRouter instance
router = APIRouter()

@router.get("/stock")
def item(aliasname: str):
    try:
        # query to get item name by
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
        print(query)
        params = (aliasname, aliasname)
        result = SQL_CONN.execute_query(query, params)
        print(result)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert result to a list of dictionaries
        item = [{"ICode": row[0], "Aliasname":row[1], "Name": row[2], "Qty":int(row[4]), "SalePrice":int(row[3])} for row in result]

        print(item)
        return {"status": "success", "users": item}

    except Exception as e:
        return {"status": "error", "message": str(e)}