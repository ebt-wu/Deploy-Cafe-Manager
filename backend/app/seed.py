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
        
        # Create 7 Cafés
        cafes = [
            Cafe(id=str(uuid.uuid4()), name="Morning Brew", description="Cozy café with artisan coffee and fresh pastries", location="Orchard Road", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Java Junction", description="Hip café with live music on weekends", location="Marina Bay", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Espresso Express", description="Quick service café for busy professionals", location="Raffles Place", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Bean & Leaf", description="Specialty coffee and tea house with organic pastries", location="Clarke Quay", logo=None),
            Cafe(id=str(uuid.uuid4()), name="The Daily Grind", description="Neighborhood café with excellent WiFi for remote workers", location="Bukit Timah", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Brew Haven", description="Modern minimalist café with premium coffee beans", location="Tiong Bahru", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Cappuccino Corner", description="Italian-inspired café with homemade desserts", location="Kampong Glam", logo=None),
        ]
        
        db.add_all(cafes)
        db.commit()
        
        # Create 20+ Employees
        employees = [
            Employee(id="UI0000001", name="Alice Wong", email_address="alice.wong@email.com", phone_number="91234567", gender="Female", start_date=datetime.now() - timedelta(days=365)),
            Employee(id="UI0000002", name="Bob Tan", email_address="bob.tan@email.com", phone_number="98765432", gender="Male", start_date=datetime.now() - timedelta(days=300)),
            Employee(id="UI0000003", name="Charlie Lim", email_address="charlie.lim@email.com", phone_number="92345678", gender="Male", start_date=datetime.now() - timedelta(days=250)),
            Employee(id="UI0000004", name="Diana Lee", email_address="diana.lee@email.com", phone_number="93456789", gender="Female", start_date=datetime.now() - timedelta(days=200)),
            Employee(id="UI0000005", name="Edward Ng", email_address="edward.ng@email.com", phone_number="94567890", gender="Male", start_date=datetime.now() - timedelta(days=180)),
            Employee(id="UI0000006", name="Fiona Chen", email_address="fiona.chen@email.com", phone_number="95678901", gender="Female", start_date=datetime.now() - timedelta(days=150)),
            Employee(id="UI0000007", name="George Ong", email_address="george.ong@email.com", phone_number="96789012", gender="Male", start_date=datetime.now() - timedelta(days=120)),
            Employee(id="UI0000008", name="Hannah Sim", email_address="hannah.sim@email.com", phone_number="97890123", gender="Female", start_date=datetime.now() - timedelta(days=100)),
            Employee(id="UI0000009", name="Ivan Koh", email_address="ivan.koh@email.com", phone_number="98901234", gender="Male", start_date=datetime.now() - timedelta(days=90)),
            Employee(id="UI0000010", name="Julie Teo", email_address="julie.teo@email.com", phone_number="99012345", gender="Female", start_date=datetime.now() - timedelta(days=75)),
            Employee(id="UI0000011", name="Kevin Loh", email_address="kevin.loh@email.com", phone_number="90123456", gender="Male", start_date=datetime.now() - timedelta(days=60)),
            Employee(id="UI0000012", name="Linda Tay", email_address="linda.tay@email.com", phone_number="91123456", gender="Female", start_date=datetime.now() - timedelta(days=50)),
            Employee(id="UI0000013", name="Marcus Goh", email_address="marcus.goh@email.com", phone_number="92123456", gender="Male", start_date=datetime.now() - timedelta(days=45)),
            Employee(id="UI0000014", name="Nicole Chia", email_address="nicole.chia@email.com", phone_number="93123456", gender="Female", start_date=datetime.now() - timedelta(days=40)),
            Employee(id="UI0000015", name="Oliver Tan", email_address="oliver.tan@email.com", phone_number="94123456", gender="Male", start_date=datetime.now() - timedelta(days=35)),
            Employee(id="UI0000016", name="Pamela Ng", email_address="pamela.ng@email.com", phone_number="95123456", gender="Female", start_date=datetime.now() - timedelta(days=30)),
            Employee(id="UI0000017", name="Quincy Lee", email_address="quincy.lee@email.com", phone_number="96123456", gender="Male", start_date=datetime.now() - timedelta(days=25)),
            Employee(id="UI0000018", name="Rachel Chua", email_address="rachel.chua@email.com", phone_number="97123456", gender="Female", start_date=datetime.now() - timedelta(days=20)),
            Employee(id="UI0000019", name="Steven Ooi", email_address="steven.ooi@email.com", phone_number="98123456", gender="Male", start_date=datetime.now() - timedelta(days=15)),
            Employee(id="UI0000020", name="Tanya Kwan", email_address="tanya.kwan@email.com", phone_number="99123456", gender="Female", start_date=datetime.now() - timedelta(days=10)),
            Employee(id="UI0000021", name="Usha Patel", email_address="usha.patel@email.com", phone_number="91234568", gender="Female", start_date=datetime.now() - timedelta(days=5)),
        ]
        
        db.add_all(employees)
        db.commit()
        
        # Link employees to cafés (distribute across all cafés)
        cafe_list = db.query(Cafe).all()
        emp_list = db.query(Employee).all()
        
        links = []
        # Distribute employees across cafés
        for i, emp in enumerate(emp_list):
            cafe = cafe_list[i % len(cafe_list)]
            links.append(EmployeeCafe(employee_id=emp.id, cafe_id=cafe.id))
        
        db.add_all(links)
        db.commit()
        
        print(f"✅ Database seeded successfully with {len(cafes)} cafés and {len(employees)} employees!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()
