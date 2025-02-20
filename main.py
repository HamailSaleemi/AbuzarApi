import SQL  # Ensure SQL.py is in the same directory
from fastapi import FastAPI
conn = SQL.conn
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# try:
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Users')
#     for row in cursor.fetchall():
#         for col in row:
#             print(col, end='\t')
#         print('')
# except Exception as e:
#     print(f"Error executing query: {e}")
# finally:
#     cursor.close()
#     conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)