from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.api.dependencies import uow_factory
from app.services.employees_service import EmployeesService
from app.domain.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut

router = APIRouter(prefix="/employees", tags=["employees"])
service = EmployeesService(uow_factory)

@router.get("", response_model=List[EmployeeOut])
def list_employees(cafe: Optional[str] = Query(default=None)):
    return service.list(cafe)

@router.post("", status_code=201)
def create_employee(payload: EmployeeCreate):
    try:
        print(payload)
        emp_id = service.create(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": emp_id}

@router.put("", status_code=200)
def update_employee(payload: EmployeeUpdate):
    try:
        print(payload)
        ok = service.update(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"success": ok}

@router.delete("", status_code=200)
def delete_employee(id: str):
    print(f"Deleting employee {id}")
    print(id)
    ok = service.delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"success": True}
