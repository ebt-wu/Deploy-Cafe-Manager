from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domain.models import Cafe, Employee, EmployeeCafe
import uuid
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Cafe).first():
            print("✅ Database already seeded")
            return
        
        # Create cafés
        cafe1 = Cafe(id=str(uuid.uuid4()), name="Morning Brew", description="Best coffee in town", location="Orchard Road", logo=None)
        cafe2 = Cafe(id=str(uuid.uuid4()), name="Java Junction", description="Hip café with live music", location="Marina Bay", logo=None)
        cafe3 = Cafe(id=str(uuid.uuid4()), name="Espresso Express", description="Quick service", location="Raffles Place", logo=None)
        
        db.add_all([cafe1, cafe2, cafe3])
        db.commit()
        
        # Create employees
        emp1 = Employee(id="UI0000001", name="Alice Wong", email_address="alice@email.com", phone_number="91234567", gender="Female", start_date=datetime.now() - timedelta(days=300))
        emp2 = Employee(id="UI0000002", name="Bob Tan", email_address="bob@email.com", phone_number="98765432", gender="Male", start_date=datetime.now() - timedelta(days=270))
        emp3 = Employee(id="UI0000003", name="Charlie Lim", email_address="charlie@email.com", phone_number="92345678", gender="Male", start_date=datetime.now() - timedelta(days=400))
        
        db.add_all([emp1, emp2, emp3])
        db.commit()
        
        # Link employees to cafés
        db.add_all([
            EmployeeCafe(employee_id="UI0000001", cafe_id=cafe1.id),
            EmployeeCafe(employee_id="UI0000002", cafe_id=cafe1.id),
            EmployeeCafe(employee_id="UI0000003", cafe_id=cafe2.id)
        ])
        db.commit()
        
        print("✅ Database seeded successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()
