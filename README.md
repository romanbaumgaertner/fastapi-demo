# FastAPI demo 

The following application implements to REST endpoints using the Python FastAPI web framework. The following APIs are implemented

- create employee: creates an employee where the format of DOB follows the pattern MM/DD/YYYY
- get employee: returns an employee with age instead DOB

## Tech Stack used

The FastAPI demo uses

- FastAPI framework
- PostgreSQL
- Pydantic for input data validation
- Pscyogp for PostgreSQL access


## How too Run

To run the application you need to 

1. clone the project
2. create a virtual environment
3. execute pip install -r requirements.txt
   

### Locally

To run the application locally do

1. run PostgreSQL from a docker container
2. run the application with fastapi dev main.py or  uvicorn main:app --reload
3. use curl or Postman to send REST APIs 

#### Using FastAPI dev

#### Running from Container

1. Set environment variable APP_ENV=dev or prod
2. Containerize the app with
   ```
    docker build -f Dockerfile.prod -t fastapi-prod .
   ```
3. Run docker container
   ```
    docker run -d  -p 8000:8000 fastapi-prod:latest
   ```

#### Running on EKS

1. Create EKS cluster using AWS EKS console
2. Create nodegroup using console or CLI
3. Create pod or deployment
4. Create LoadBalancer service

   
