from pydantic import BaseModel, EmailStr, validator, ValidationError
from datetime import datetime

class Employee(BaseModel):
    employee_id: str 
    name: str
    department: str
    email: EmailStr 
    dob: str

    @validator('dob')
    def validate_dob(cls, value):
        try:
            # Parse the dob string to ensure it's in the correct format
            datetime.strptime(value, '%m/%d/%Y')
        except ValueError:
            raise ValueError('DOB must be in the format "MM/DD/YYYY"')
        

        return value

'''
Read class for Employee which contains 
    primary key id
    age member instead DOB
'''
class EmployeeAge(BaseModel):
    id: int
    employee_id: str 
    name: str
    department: str
    email: EmailStr 
    age: int
