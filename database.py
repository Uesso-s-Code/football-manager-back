from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./football.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db():
    print("Creating database and tables...")
    print(DATABASE_URL)
    
    SQLModel.metadata.create_all(engine)
