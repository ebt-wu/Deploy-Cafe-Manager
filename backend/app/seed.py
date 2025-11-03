from app.domain.models import Cafe, Employee, EmployeeCafe
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def seed_database(db):
    """Seed database with sample data"""
    
    try:
        # Check if already seeded
        from sqlalchemy import select
        existing = db.execute(select(Cafe)).scalars().first()
        
        if existing:
            logger.info("✅ Database already seeded, skipping...")
            return
        
        logger.info("🌱 Starting database seeding...")
        
        # Create 7 Cafés
        cafes = [
            Cafe(id=str(uuid.uuid4()), name="Morning Brew", description="Cozy café with artisan coffee", location="Orchard Road", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Java Junction", description="Hip café with live music", location="Marina Bay", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Espresso Express", description="Quick service café", location="Raffles Place", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Bean & Leaf", description="Specialty coffee and tea", location="Clarke Quay", logo=None),
            Cafe(id=str(uuid.uuid4()), name="The Daily Grind", description="Neighborhood café", location="Bukit Timah", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Brew Haven", description="Modern minimalist café", location="Tiong Bahru", logo=None),
            Cafe(id=str(uuid.uuid4()), name="Cappuccino Corner", description="Italian-inspired café", location="Kampong Glam", logo=None),
        ]
        
        for cafe in cafes:
            db.add(cafe)
        db.commit()
        
        # Create 21 Employees
        employees = [
            Employee(id="UI0000001", name="Alice Wong", email_address="alice.wong@email.com", phone_number="91234567", gender="Female", start_date=datetime(2023, 11, 15)),
            Employee(id="UI0000002", name="Bob Tan", email_address="bob.tan@email.com", phone_number="98765432", gender="Male", start_date=datetime(2024, 1, 1)),
            Employee(id="UI0000003", name="Charlie Lim", email_address="charlie.lim@email.com", phone_number="92345678", gender="Male", start_date=datetime(2024, 2, 10)),
            Employee(id="UI0000004", name="Diana Lee", email_address="diana.lee@email.com", phone_number="93456789", gender="Female", start_date=datetime(2024, 3, 5)),
            Employee(id="UI0000005", name="Edward Ng", email_address="edward.ng@email.com", phone_number="94567890", gender="Male", start_date=datetime(2024, 4, 12)),
            Employee(id="UI0000006", name="Fiona Chen", email_address="fiona.chen@email.com", phone_number="95678901", gender="Female", start_date=datetime(2024, 5, 20)),
            Employee(id="UI0000007", name="George Ong", email_address="george.ong@email.com", phone_number="96789012", gender="Male", start_date=datetime(2024, 6, 8)),
            Employee(id="UI0000008", name="Hannah Sim", email_address="hannah.sim@email.com", phone_number="97890123", gender="Female", start_date=datetime(2024, 7, 15)),
            Employee(id="UI0000009", name="Ivan Koh", email_address="ivan.koh@email.com", phone_number="98901234", gender="Male", start_date=datetime(2024, 8, 1)),
            Employee(id="UI0000010", name="Julie Teo", email_address="julie.teo@email.com", phone_number="99012345", gender="Female", start_date=datetime(2024, 8, 22)),
            Employee(id="UI0000011", name="Kevin Loh", email_address="kevin.loh@email.com", phone_number="90123456", gender="Male", start_date=datetime(2024, 9, 5)),
            Employee(id="UI0000012", name="Linda Tay", email_address="linda.tay@email.com", phone_number="91123456", gender="Female", start_date=datetime(2024, 9, 18)),
            Employee(id="UI0000013", name="Marcus Goh", email_address="marcus.goh@email.com", phone_number="92123456", gender="Male", start_date=datetime(2024, 10, 1)),
            Employee(id="UI0000014", name="Nicole Chia", email_address="nicole.chia@email.com", phone_number="93123456", gender="Female", start_date=datetime(2024, 10, 10)),
            Employee(id="UI0000015", name="Oliver Tan", email_address="oliver.tan@email.com", phone_number="94123456", gender="Male", start_date=datetime(2024, 10, 20)),
            Employee(id="UI0000016", name="Pamela Ng", email_address="pamela.ng@email.com", phone_number="95123456", gender="Female", start_date=datetime(2024, 10, 25)),
            Employee(id="UI0000017", name="Quincy Lee", email_address="quincy.lee@email.com", phone_number="96123456", gender="Male", start_date=datetime(2024, 10, 28)),
            Employee(id="UI0000018", name="Rachel Chua", email_address="rachel.chua@email.com", phone_number="97123456", gender="Female", start_date=datetime(2024, 11, 1)),
            Employee(id="UI0000019", name="Steven Ooi", email_address="steven.ooi@email.com", phone_number="98123456", gender="Male", start_date=datetime(2024, 11, 2)),
            Employee(id="UI0000020", name="Tanya Kwan", email_address="tanya.kwan@email.com", phone_number="99123456", gender="Female", start_date=datetime(2024, 11, 3)),
            Employee(id="UI0000021", name="Usha Patel", email_address="usha.patel@email.com", phone_number="91234568", gender="Female", start_date=datetime(2024, 11, 4)),
        ]
        
        for emp in employees:
            db.add(emp)
        db.commit()
        
        # Link employees to cafés
        cafe_list = db.execute(select(Cafe)).scalars().all()
        emp_list = db.execute(select(Employee)).scalars().all()
        
        for i, emp in enumerate(emp_list):
            cafe = cafe_list[i % len(cafe_list)]
            link = EmployeeCafe(employee_id=emp.id, cafe_id=cafe.id)
            db.add(link)
        
        db.commit()
        
        logger.info(f"✅ Seeded {len(cafes)} cafés and {len(employees)} employees!")
        
    except Exception as e:
        logger.error(f"❌ Seeding error: {e}", exc_info=True)
        db.rollback()
