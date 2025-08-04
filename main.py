from fastapi import FastAPI
from router import router, fill_table
from database import create_tables


app = FastAPI()
create_tables()

app.include_router(router)
fill_table() # использовать только для создания пробной базы


@app.get("/")
def read_root():
    return {"message": "Hello world!"}
