from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

from config import config
from logger import Logger

Base = declarative_base()
logger = Logger(__name__)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    user_age = Column(Integer)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String(512), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="messages")

class IgnoreUser(Base):
    __tablename__ = "ignore_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)

class IgnoreGroup(Base):
    __tablename__ = "ignore_groups"
    id = Column(Integer, primary_key=True)
    group_id = Column(String(50), nullable=False)

User.messages = relationship("Message", order_by=Message.id, back_populates="user")

class Database:
    def __init__(self):
        self.engine = create_engine(config.get_database_uri())
        self.metadata = MetaData()
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def __del__(self):
        self.Session.remove()

    def _drop_all_tables(self):
        self.metadata.drop_all(self.engine)
        logger.info("All tables have been dropped.")

    def create_all_tables(self):
        self._drop_all_tables()
        Base.metadata.create_all(self.engine)
        logger.info("All tables have been created.")

    def add_user(self, username, user_age=None):
        session = self.Session()
        user = User(username=username, user_age=user_age)
        session.add(user)
        session.commit()
        user_id = user.id  # 追加されたユーザーの ID を取得
        session.close()
        logger.info("Add user : {} : {}.".format(username,user_id))

    def add_message(self, content, user_id):
        session = self.Session()
        message = Message(content=content, user_id=user_id)
        session.add(message)
        session.commit()
        session.close()

    def get_all_users(self):
        session = self.Session()
        users = session.query(User).all()
        session.close()
        return users

    def get_all_messages(self):
        session = self.Session()
        messages = session.query(Message).all()
        session.close()
        return messages

    def get_user_by_id(self, user_id):
        session = self.Session()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        return user

    def get_messages_by_user_id(self, user_id):
        session = self.Session()
        messages = session.query(Message).filter(Message.user_id == user_id).all()
        session.close()
        return messages

    def delete_user_by_id(self, user_id):
        session = self.Session()
        user = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()
        session.close()
        logger.info("Delete user_id : {}.".format(user_id))

    def delete_message_by_id(self, message_id):
        session = self.Session()
        message = session.query(Message).filter(Message.id == message_id).first()
        session.delete(message)
        session.commit()
        session.close()

    def get_ignore_list_from_db():
        with session_scope() as session:
            ignore_users = session.query(IgnoreUser).all()
            ignore_groups = session.query(IgnoreGroup).all()
            return ignore_users, ignore_groups
    
    def add_user_to_db_ignore_list(user_id):
        with session_scope() as session:
            ignore_user = IgnoreUser(user_id=user_id)
            session.add(ignore_user)

    def add_group_to_db_ignore_list(group_id):
        with session_scope() as session:
            ignore_group = IgnoreGroup(group_id=group_id)
            session.add(ignore_group)


db = Database()
