from sqlalchemy import create_engine
from app.core.database import Base
from app.core.config import settings
from app.models import user, device, cluster

engine = create_engine(settings.DATABASE_URL.replace("+pymysql", "+mysqlconnector"))

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

if __name__ == "__main__":
    init_db()