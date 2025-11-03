from typing import Any
from sqlalchemy.orm import Session

class BaseRepo:
    def __init__(self, db: Session):
        self.db = db

    def add(self, obj: Any):
        self.db.add(obj)
        return obj

    def delete(self, obj: Any):
        self.db.delete(obj)
