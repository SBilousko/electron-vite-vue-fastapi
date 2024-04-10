from typing import Union
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from db_model import *

import uvicorn
import sys
import os

# TODO, to make this flexible when Vite change their port#, i.e. auto track port allowed list
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:4242",
    "http://localhost:5173",
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:4242",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:80",
    "http://127.0.0.1:8080",
]

with open('pid.txt', 'w') as f:
    f.write(str(os.getpid()))

def setPort():
    p = 4242
    try:
        p = sys.argv[1] 
    except:
        print("error with sys.argv, assigned default port: 4242")   
    return p

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
port = setPort()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # return 
    files = db.query(File).all()
    return files


@app.get("/pid")
def read_root():
    return {"pid": str(os.getpid())}

@app.post("/upload/")
def read_root(data = Body(), db: Session = Depends(get_db)):
    file = File(
        name = data["filename"]
    )
    db.add(file)
    db.commit()
    return file["name"]

@app.delete("/delete/")
def delete_files(db: Session = Depends(get_db)):
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(bind = engine)
    db.execute('''TRUNCATE TABLE files''')
    db.commit()
    return {"Files deleted"}

if __name__ == "__main__":
    # with Session(engine) as db:
    #     statement = select(File.name)
    #     print(db.execute(statement).all())
    uvicorn.run(app, host='127.0.0.1', port=port)