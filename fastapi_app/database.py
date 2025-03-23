from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = "diabetes.db"
DATABASE_URL = f"sqlite:///./{DATABASE_NAME}"

# Creating an engine puru
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


'''
Q) Why Use yield Instead of return?
Keeps the database session open only as long as needed
Automatically closes the session when the request is done
Prevents memory leaks & unnecessary open connections

'''