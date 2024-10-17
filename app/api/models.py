from sqlalchemy import Column, Integer, String, DateTime, Boolean

class User:
    __tablename__ = "users"

    uuid = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
