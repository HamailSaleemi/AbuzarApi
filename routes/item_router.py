from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from routes import helper

# Create an APIRouter instance
router = APIRouter()

@router.get("/stock")
def item_stock(aliasname: str):
    try:
        # query to get item name by
        result = helper.get_item_detail_by_aliasname(aliasname)
        # print(result)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert result to a list of dictionaries
        item = [{"ICode": row[0], "Aliasname":row[1], "Name": row[2], "Qty":int(row[4]), "SalePrice":int(row[3])} for row in result]
        # print(item)
        return {"status": "success", "users": item}

    except Exception as e:
        return {"status": "error", "message": str(e)}

        return {"status": "error", "message": str(e)}


@router.get("/stock/sale")
def item_stck_and_sale(aliasname: str):
    try:
        # get item info
        result = helper.get_item_detail_by_aliasname(aliasname)
        # print(result)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        print(result)
        # Convert result to a list of dictionaries
        result = result[0]
        item = {"ICode": result[0],
                "Aliasname":result[1], "Name": result[2], "Qty":int(result[4]), "SalePrice":str(result[3])}
        # print(item)
        # Convert result to a list of dictionaries
        print(item)
        item_sale, totalSold = helper.get_item_sale(item['ICode'])
        print({"status": "success", "item": item, 'sale':item_sale})
        return JSONResponse(content= {"status": "success", "item": item, 'sale':item_sale, 'totalSold':totalSold})

    except Exception as e:
        return {"status": "error", "message": str(e)}
