from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255), nullable=False)
    server_name = Column(String(255), nullable=False)
    group_name = Column(String(255))

    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="conversations")
    summary = relationship("ConversationSummary", uselist=False, back_populates="conversation")


class ConversationSummary(Base):
    __tablename__ = 'conversation_summaries'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    summary = Column(Text, nullable=False)

    conversation = relationship("Conversation", back_populates="summary")

class IgnoreUser(Base):
    __tablename__ = "ignore_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)

class IgnoreGroup(Base):
    __tablename__ = "ignore_groups"
    id = Column(Integer, primary_key=True)
    group_id = Column(String(50), nullable=False)

def create_tables():
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")

    db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()