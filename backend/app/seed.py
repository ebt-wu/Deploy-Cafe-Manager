import os
import sys
from datetime import date, timedelta
from uuid import uuid4

# Add backend to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.domain.models import Base, Cafe, Employee, EmployeeCafe

def seed_database():
    """Seed the database with 7 cafes and 20+ employees."""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(EmployeeCafe).delete()
        db.query(Employee).delete()
        db.query(Cafe).delete()
        db.commit()
        
        # 7 Cafes across different locations
        cafes = [
            Cafe(
                id=str(uuid4()),
                name="Brew & Bean",
                description="Cozy corner cafe with specialty coffee and pastries",
                location="Singapore"
            ),
            Cafe(
                id=str(uuid4()),
                name="The Daily Grind",
                description="Fast-paced cafe perfect for business meetings and work",
                location="Singapore"
            ),
            Cafe(
                id=str(uuid4()),
                name="Artisan Roasters",
                description="Premium single-origin coffee and freshly baked goods",
                location="Jakarta"

            ),
            Cafe(
                id=str(uuid4()),
                name="Cafe Serenity",
                description="Quiet study-friendly environment with WiFi",
                location="Bangkok"
            ),
            Cafe(
                id=str(uuid4()),
                name="Urban Espresso",
                description="Modern minimalist cafe in the business district",
                location="Singapore"
            ),
            Cafe(
                id=str(uuid4()),
                name="Kedai Kopi Tradisional",
                description="Traditional Indonesian coffee shop with local charm",
                location="Jakarta"
            ),
            Cafe(
                id=str(uuid4()),
                name="River Cafe",
                description="Riverside cafe with scenic views and relaxing ambiance",
                location="Bangkok"
            ),
        ]
        
        for cafe in cafes:
            db.add(cafe)
        db.commit()
        
        print(f"✓ Seeded {len(cafes)} cafes")
        
        # 20+ Employees with varied start dates and distribution across cafes
        employees_data = [
            # Brew & Bean (4 employees)
            ("UI1000001", "Alice Johnson", "alice.j@example.com", "81234567", "Female", cafes[0].id, date.today() - timedelta(days=365)),
            ("UI1000002", "Bob Chen", "bob.chen@example.com", "82345678", "Male", cafes[0].id, date.today() - timedelta(days=200)),
            ("UI1000003", "Carol Martinez", "carol.m@example.com", "83456789", "Female", cafes[0].id, date.today() - timedelta(days=120)),
            ("UI1000004", "David Lee", "david.lee@example.com", "84567890", "Male", cafes[0].id, date.today() - timedelta(days=45)),
            
            # The Daily Grind (4 employees)
            ("UI1000005", "Eva Patel", "eva.patel@example.com", "85678901", "Female", cafes[1].id, date.today() - timedelta(days=280)),
            ("UI1000006", "Frank Wong", "frank.w@example.com", "86789012", "Male", cafes[1].id, date.today() - timedelta(days=150)),
            ("UI1000007", "Grace Kim", "grace.kim@example.com", "87890123", "Female", cafes[1].id, date.today() - timedelta(days=90)),
            ("UI1000008", "Henry Tan", "henry.tan@example.com", "88901234", "Male", cafes[1].id, date.today() - timedelta(days=30)),
            
            # Artisan Roasters (3 employees)
            ("UI1000009", "Isabella Rodriguez", "isabella.r@example.com", "89012345", "Female", cafes[2].id, date.today() - timedelta(days=240)),
            ("UI1000010", "Jack Anderson", "jack.a@example.com", "80123456", "Male", cafes[2].id, date.today() - timedelta(days=110)),
            ("UI1000011", "Julia Thompson", "julia.t@example.com", "81234567", "Female", cafes[2].id, date.today() - timedelta(days=60)),
            
            # Cafe Serenity (3 employees)
            ("UI1000012", "Kevin Brown", "kevin.b@example.com", "82345678", "Male", cafes[3].id, date.today() - timedelta(days=310)),
            ("UI1000013", "Laura Garcia", "laura.g@example.com", "83456789", "Female", cafes[3].id, date.today() - timedelta(days=170)),
            ("UI1000014", "Michael Torres", "michael.t@example.com", "84567890", "Male", cafes[3].id, date.today() - timedelta(days=80)),
            
            # Urban Espresso (4 employees)
            ("UI1000015", "Nina Khanna", "nina.k@example.com", "85678901", "Female", cafes[4].id, date.today() - timedelta(days=220)),
            ("UI1000016", "Oscar Lopez", "oscar.l@example.com", "86789012", "Male", cafes[4].id, date.today() - timedelta(days=135)),
            ("UI1000017", "Patricia Smith", "patricia.s@example.com", "87890123", "Female", cafes[4].id, date.today() - timedelta(days=75)),
            ("UI1000018", "Quincy Adams", "quincy.a@example.com", "88901234", "Male", cafes[4].id, date.today() - timedelta(days=20)),
            
            # Kedai Kopi Tradisional (2 employees)
            ("UI1000019", "Rachel Chen", "rachel.c@example.com", "89012345", "Female", cafes[5].id, date.today() - timedelta(days=190)),
            ("UI1000020", "Steven Hartley", "steven.h@example.com", "80123456", "Male", cafes[5].id, date.today() - timedelta(days=100)),
            
            # River Cafe (3 employees)
            ("UI1000021", "Tanya Okonkwo", "tanya.o@example.com", "81234567", "Female", cafes[6].id, date.today() - timedelta(days=340)),
            ("UI1000022", "Ulysses Grant", "ulysses.g@example.com", "82345678", "Male", cafes[6].id, date.today() - timedelta(days=160)),
            ("UI1000023", "Victoria Nelson", "victoria.n@example.com", "83456789", "Female", cafes[6].id, date.today() - timedelta(days=55)),
        ]
        
        for emp_id, name, email, phone, gender, cafe_id, start_date in employees_data:
            employee = Employee(
                id=emp_id,
                name=name,
                email_address=email,
                phone_number=phone,
                gender=gender
            )
            db.add(employee)
            db.flush()  # Ensure employee is inserted before creating mapping
            
            # Create employee-cafe mapping
            mapping = EmployeeCafe(
                employee_id=emp_id,
                cafe_id=cafe_id,
                start_date=start_date
            )
            db.add(mapping)
        
        db.commit()
        print(f"✓ Seeded {len(employees_data)} employees with cafe assignments")
        print("✓ Database seeded successfully!")
        
        # Print summary
        print("\n--- Seed Data Summary ---")
        print(f"Cafes seeded: {len(cafes)}")
        print(f"Employees seeded: {len(employees_data)}")
        for i, cafe in enumerate(cafes, 1):
            emp_count = sum(1 for _, _, _, _, _, cafe_id, _ in employees_data if cafe_id == cafe.id)
            print(f"  {cafe.name} ({cafe.location}): {emp_count} employees")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
