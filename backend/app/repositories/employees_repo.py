from typing import List, Optional, Tuple
from sqlalchemy import select, func, literal_column, Integer
from sqlalchemy.orm import Session
from app.domain.models import Employee, Cafe, EmployeeCafe

class EmployeesRepo:
    def __init__(self, db: Session):
        self.db = db

    def list_with_days_and_cafe(self, cafe_id: Optional[str]) -> List[Tuple[Employee, int, Optional[str]]]:
        days_expr = func.cast(func.coalesce(func.extract("day", func.age(func.current_date(), EmployeeCafe.start_date)),0),Integer)
        stmt = (
            select(
                Employee,
                days_expr.label("days_worked"),
                Cafe.name.label("cafe_name"),
            )
            .join(EmployeeCafe, EmployeeCafe.employee_id == Employee.id, isouter=True)
            .join(Cafe, Cafe.id == EmployeeCafe.cafe_id, isouter=True)
            .order_by(days_expr.desc())
)
        if cafe_id:
            stmt = stmt.where(Cafe.id == cafe_id)
        return list(self.db.execute(stmt).all())

    def get(self, emp_id: str):
        return self.db.get(Employee, emp_id)

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        return employee

    def upsert_mapping(self, emp_id: str, cafe_id: Optional[str], start_date):
        # remove mapping if cafe_id is None
        current = self.db.get(EmployeeCafe, emp_id)
        if cafe_id is None:
            if current:
                self.db.delete(current)
            return None
        if current:
            current.cafe_id = cafe_id
            if start_date:
                current.start_date = start_date
            return current
        mapping = EmployeeCafe(employee_id=emp_id, cafe_id=cafe_id, start_date=start_date)
        self.db.add(mapping)
        return mapping

    def delete(self, employee: Employee):
        self.db.delete(employee)

    def delete_mapping(self, employee_id: str):
        self.db.query(EmployeeCafe).filter(
            EmployeeCafe.employee_id == employee_id
        ).delete()