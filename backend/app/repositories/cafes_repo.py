from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.domain.models import Cafe, EmployeeCafe

class CafesRepo:
    def __init__(self, db: Session):
        self.db = db

    def list_with_counts(self, location: Optional[str]) -> List[Tuple[Cafe, int]]:
        stmt = (
            select(Cafe, func.count(EmployeeCafe.employee_id).label("emp_count"))
            .join(EmployeeCafe, EmployeeCafe.cafe_id == Cafe.id, isouter=True)
            .group_by(Cafe.id)
            .order_by(func.count(EmployeeCafe.employee_id).desc())
        )
        if location:
            stmt = stmt.where(Cafe.location == location)
        return list(self.db.execute(stmt).all())

    def get(self, cafe_id):
        return self.db.get(Cafe, cafe_id)

    def create(self, cafe: Cafe) -> Cafe:
        self.db.add(cafe)
        return cafe

    def update_fields(self, cafe: Cafe, data: dict) -> Cafe:
        for k, v in data.items():
            if v is not None and hasattr(cafe, k):
                setattr(cafe, k, v)
        return cafe

    def delete(self, cafe: Cafe):
        self.db.delete(cafe)
