from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from app.repositories.cafes_repo import CafesRepo
from app.repositories.employees_repo import EmployeesRepo

class UnitOfWork(AbstractContextManager):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory
        self.db: Session | None = None
        self.cafes: CafesRepo | None = None
        self.employees: EmployeesRepo | None = None

    def __enter__(self):
        self.db = self._session_factory()
        self.cafes = CafesRepo(self.db)
        self.employees = EmployeesRepo(self.db)
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()
