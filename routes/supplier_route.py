from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from DATABASE import connection
from pydantic import BaseModel
from routes.auth.auth_handler import verify_token
router = APIRouter()
con = connection.SQL_CONN

@router.get("/")
def supplier_list(user_data: dict = Depends(verify_token)):
    try:
        query = 'select Name from Accounts where Active =? and  SubCode = ?'
        datas = con.execute_query(query, ('Y',7))
        data = [{'supplierName':row[0] } for row in datas]
        return {'message':'supplier route here', 'suppliername': data}

    except Exception as e:
        return {"status": "error", "message": str(e)}





@router.get('/search')
def search_suppler(s_query:  str, user_data: dict = Depends(verify_token)):
    try:
        # need to call a function to verify if the token is epired or not
        s_query = s_query.upper()
        query = 'select Name from Accounts where Active =? and  SubCode = ? and Name like ?'
        datas = con.execute_query(query, ('Y', 7, f'%{s_query}%'))
        data = [{'supplierName':row[0] } for row in datas]
        print(datas)
        return {'message':'supplier route here', 'suppliername': data}

    except Exception as e:
        return {"status": "error", "message": str(e)}
