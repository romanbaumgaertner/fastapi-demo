# FastAPI demo 

The following application implements to REST endpoints using the Python FastAPI web framework. The following APIs are implemented

- create employee: creates an employee where the format of DOB follows the pattern MM/DD/YYYY
- get employee: returns an employee with age instead DOB

## Tech Stack used

The FastAPI demo uses

- FastAPI framework
- PostgreSQL
- Pydantic for input data validation
- Psycogp for PostgreSQL access
- Docker for container
- AWS CLI and Kubectl for AWS EKS usage


## How to Run

### Setup project
To run the application you need to 

1. clone the project into your work directory
```
git clone https://github.com/romanbaumgaertner/fastapi-demo
```
2. create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

3. install packages
```
pip install -r requirements.txt
```

### Locally

To run the application locally do

1. Create a .env file in the project root
   ```
   POSTGRES_HOST=127.0.0.1
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_PORT=5432
   ```

2. run PostgreSQL from a docker container. Make sure that the POSTGRES settings match the configuration in .env
   ```
    docker run -d \
      --rm  \
      --name postgres \
      --env POSTGRES_PASSWORD=postgres \
      --publish 5432:5432 postgres:14.3-alpine
   ```
3. run the application with
   
   ```
    fastapi dev main.py 
   ```

   or

   ```
    uvicorn main:app --reload
   ```
   
5. To test the REST APIs use

   - curl
   - Postman
   - htttp://127.0.0.1:8000/docs

#### Running from Container

1. Set environment variable 
   ```
   export  APP_ENV=dev
   ```
3. Containerize the app with
   
   ```
    docker build -f Dockerfile -t fastapi-prod .
   ```
5. Run docker container
   
   ```
    docker run -d  -p 8000:8000 fastapi-prod:latest
   ```

#### Running on EKS

1. Create EKS cluster using AWS EKS console
2. Create nodegroup using console or CLI
3. Create pod or deployment
4. Create LoadBalancer service

   
