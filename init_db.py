from sqlalchemy import text

from app.db.models import Base
from app.db.session import engine
def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(engine)
    print("Database created successfully")
if __name__ == "__main__":
    init_db()