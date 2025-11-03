import uuid
from typing import Optional, List, Dict, Any
from app.domain.models import Cafe, Employee
from app.services.unit_of_work import UnitOfWork

class CafesService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def list(self, location: Optional[str]):
        with self._uow_factory() as uow:
            rows = uow.cafes.list_with_counts(location)
            return [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "description": c.description,
                    "logo_url": c.logo_url,
                    "location": c.location,
                    "employees": int(count),
                }
                for c, count in rows
            ]

    def create(self, data: Dict[str, Any]):
        print("A")
        with self._uow_factory() as uow:
            cafe = Cafe(
                id=uuid.uuid4(),
                name=data["name"],
                description=data.get("description"),
                logo_url=data.get("logo_url"),
                location=data["location"],
            )
            uow.cafes.create(cafe)
            return str(cafe.id)

    def update(self, data: Dict[str, Any]):
        print("A")
        with self._uow_factory() as uow:
            cafe = uow.cafes.get(data["id"])
            if not cafe:
                raise ValueError("Cafe not found")
            uow.cafes.update_fields(cafe, {
                "name": data.get("name"),
                "description": data.get("description"),
                "logo_url": data.get("logo_url"),
                "location": data.get("location"),
            })
            return True

    def delete(self, cafe_id: str):
        with self._uow_factory() as uow:
            cafe = uow.cafes.get(cafe_id)
            if not cafe:
                return False
            for rel in list(cafe.employees): uow.employees.delete(rel.employee) # delete all employees in the cafe
            uow.cafes.delete(cafe)
            return True
