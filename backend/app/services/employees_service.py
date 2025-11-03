from typing import Optional, Dict, Any, List
from app.domain.models import Employee
from app.services.unit_of_work import UnitOfWork
import string, random

class EmployeesService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def list(self, cafe_id: Optional[str] = None):
        with self._uow_factory() as uow:
            employees = uow.employees.list_with_days_and_cafe(cafe_id)
            return [
                {
                    "id": emp.id,
                    "name": emp.name,
                    "email_address": emp.email_address,
                    "phone_number": emp.phone_number,
                    "gender": emp.gender,
                    "days_worked": days,
                    "cafe": cafe_name
                }
                for emp, days, cafe_name in employees
            ]

    def create(self, data: Dict[str, Any]):
        print("In service create")
        with self._uow_factory() as uow:
            employee_id = self._generate_employee_id(uow)
            emp = Employee(
                id=employee_id,
                name=data["name"],
                email_address=data["email_address"],
                phone_number=data["phone_number"],
                gender=data["gender"],
            )
            print("B")
            uow.employees.create(emp)
            uow.employees.upsert_mapping(emp.id, data.get("cafe_id"), data.get("start_date"))
            return emp.id

    def update(self, data: Dict[str, Any]):
        with self._uow_factory() as uow:
            emp = uow.employees.get(data["id"])
            if not emp:
                raise ValueError("Employee not found")
            for f in ("name", "email_address", "phone_number", "gender"):
                if data.get(f) is not None:
                    setattr(emp, f, data[f])
            if "cafe_id" in data or "start_date" in data:
                uow.employees.upsert_mapping(emp.id, data.get("cafe_id"), data.get("start_date"))
            return True

    def delete(self, emp_id: str):
        print("In service delete start")
        with self._uow_factory() as uow:
            print("In service delete")
            emp = uow.employees.get(emp_id)
            print(emp)
            if not emp:
                return False
            uow.employees.delete_mapping(emp_id)
            uow.employees.delete(emp)
            return True


    def _generate_employee_id(self, uow) -> str:
        characters = string.digits
        max_attempts = 10
        
        for _ in range(max_attempts):
            random_part = ''.join(random.choices(characters, k=7))
            employee_id = f"UI{random_part}"
            
            if not uow.employees.get(employee_id):
                return employee_id
        
        raise ValueError("Unable to generate unique employee ID")