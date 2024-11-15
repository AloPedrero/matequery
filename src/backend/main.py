from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

class Message(BaseModel):
    query: str

@app.post("/")
def echo_message(message: Message):
    db = mysql.connector.connect(
        host="db4free.net", 
        user="alo_pedrero", 
        password="kEznif-6pohji-wijruf", 
        database="act_cinco_alonso"
    )
    mySQLcursor = db.cursor()

    try:
        mySQLcursor.execute(message.query)
        
        db.commit()
        
        return {"status": 200, "message": "Query executed successfully"}

    except mysql.connector.Error as err:
        return {"status": 400, "error": str(err)}

    finally:
        mySQLcursor.close()
        db.close()
