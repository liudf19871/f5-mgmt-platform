from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.config import settings
from app.models import users, device, cluster
from app.core.security import get_password_hash

engine = create_engine(settings.DATABASE_URL.replace("+pymysql", "+mysqlconnector"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        from app.models.users import User
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            hashed_password = get_password_hash("admin")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                role="admin",
                status="active"
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created successfully")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Database tables created successfully")

if __name__ == "__main__":
    init_db()