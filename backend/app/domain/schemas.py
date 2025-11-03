from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

PHONE_MSG = "Phone must start with 8 or 9 and be 8 digits (SG format)."

def validate_phone(v: str) -> str:
    import re
    if not re.fullmatch(r"[89]\d{7}", v):
        raise ValueError(PHONE_MSG)
    return v

def validate_emp_id(v: str) -> str:
    import re
    if not re.fullmatch(r"UI\d{7}", v):
        raise ValueError("Employee id must match UIXXXXXXX (U I + 7 digits).")
    return v

class CafeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    location: str

class CafeUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    location: Optional[str] = None

class CafeOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    logo_url: Optional[str]
    location: str
    employees: int

class EmployeeCreate(BaseModel):
    name: str
    email_address: EmailStr
    phone_number: str
    gender: str
    cafe_id: Optional[str] = None
    start_date: Optional[date] = None

    _v_phone = field_validator("phone_number")(validate_phone)

class EmployeeUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    email_address: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    cafe_id: Optional[str] = None
    start_date: Optional[date] = None

    _v_id = field_validator("id")(validate_emp_id)
    _v_phone = field_validator("phone_number")(validate_phone)

class EmployeeOut(BaseModel):
    id: str
    name: str
    email_address: EmailStr
    phone_number: str
    gender: str
    days_worked: int
    cafe: str | None
