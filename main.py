from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from db import db_util
from models import employee
from psycopg2 import Error,IntegrityError
#from dotenv import load_dotenv
from dotenv import dotenv_values
import os
import helper

app = FastAPI()
app.mount("/imgs", StaticFiles(directory="static/images"), name='images')

@app.get("/")
async def get_root():
    html_fastapi = """
    <html>
        <head>
            <title>FastAPI - demo</title>
        </head>
        <body>
            <h1>Cloud Setup of FastAPI-Demo</h1>
            <!--img src="imgs/fastapi.jpg"-->
        </body>
    </html>
    """
    return HTMLResponse(content=html_fastapi)

@app.get("/api/employees")
async def get_all():
    return {"get all - not implemented"}


@app.get("/api/employees/{id}")
async def get_employee(id: int):
    try:

        entry = db_util.get_employee(id)

        print( type(entry) )
    except (Exception, Error):
        raise HTTPException(status_code=404, detail="Not found")
    return entry


# Alternatively, using Pydantic model for JSON payload
@app.post("/api/employees")
async def create_employee_json(employee: employee.Employee):

    try: 
        # age check
        if db_util.calculate_age(employee.dob) < 18:
            raise HTTPException(status_code=400, detail="Employee too young")

        employee_id = db_util.create_employee(employee)
        return  {"id": employee_id}
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Duplicate employee")
    except (Exception, Error):
        raise HTTPException(status_code=400, detail="Not creatted")

    return HTTPException(status_code=201)

@app.delete("/api/employees/{id}")
async def delete_employee(id: int):
    try:

        db_util.delete_employee(id)

    except (Exception, Error):
        raise HTTPException(status_code=404, detail="Not found")
    return "deleted resource"


'''
Bootstrap only gets executed when table does not exist.
In production code we can seperate bootstrapping from regular appplication start/restart
'''
db_util.bootstap()



