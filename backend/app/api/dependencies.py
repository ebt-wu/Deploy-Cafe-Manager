from app.db.session import SessionLocal
from app.services.unit_of_work import UnitOfWork
def uow_factory():
    return UnitOfWork(SessionLocal)
