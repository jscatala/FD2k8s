"""
Example of api for python
"""
from fastapi import FastAPI, Form, HTTPException

from json import dumps as jdps
from socket import gethostname as sgh
from threading import Thread

from producer import OPTS, add_vote
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    for i in OPTS:
        print(i)

@app.get("/")
async def root():
    return {"text": "Hello World!!"}

@app.get("/results")
async def get_results():
    return {"text": "Not implemented yet"}

@app.get("/healthcheck")
async def healthcheck():
    data = dict()
    data['hostname'] = sgh()
    return data

@app.post("/vote/")
async def vote(option: str = Form('option')):
    try:
        if option in OPTS:
            x = Thread(target=add_vote, args=(option,))
            x.start()
        else:
            #raise ValueError("{} not a valid option".format(option))
            raise HTTPException(status_code=404, detail="{} not a valid option".format(option))
    except ValueError as e :
        print(e)
    finally:
        print("API [DONE]: vote with option {}".format(option))
