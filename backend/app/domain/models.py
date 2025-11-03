import uuid
from datetime import date
from sqlalchemy import (
    Column, String, Date, Enum, ForeignKey, UniqueConstraint,
    CheckConstraint, Integer
)
from sqlalchemy.dialects.postgresql import UUID, CHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Cafe(Base):
    __tablename__ = "cafes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)           # UI enforces 6–10 length
    description = Column(String(256), nullable=True)
    logo_url = Column(String(512), nullable=True)
    location = Column(String(100), nullable=False)

    employees = relationship(
        "EmployeeCafe",
        back_populates="cafe",
        cascade="all, delete-orphan"
    )

class Employee(Base):
    __tablename__ = "employees"
    id = Column(CHAR(9), primary_key=True)               # e.g., UIXXXXXXX
    name = Column(String(100), nullable=False)
    email_address = Column(String(320), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False)
    gender = Column(Enum("Male", "Female", name="gender"), nullable=False)

    cafe_rel = relationship("EmployeeCafe", back_populates="employee", uselist=False)

    __table_args__ = (
        CheckConstraint("char_length(id)=9", name="employee_id_len_9"),
    )

class EmployeeCafe(Base):
    __tablename__ = "employee_cafe"
    employee_id = Column(CHAR(9), ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True)
    cafe_id = Column(UUID(as_uuid=True), ForeignKey("cafes.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False, default=date.today)

    employee = relationship("Employee", back_populates="cafe_rel")
    cafe = relationship("Cafe", back_populates="employees")

    __table_args__ = (
        UniqueConstraint("employee_id", name="uq_employee_one_cafe"),
    )
