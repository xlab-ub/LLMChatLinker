# llmchatlinker/units/database_manage_unit.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, joinedload
import datetime

DATABASE_URI = 'postgresql://myuser:mypassword@localhost:5433/mydatabase'

Base = declarative_base()

# Association table for many-to-many relationship between users and chats
user_chats = Table('user_chats', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('chat_id', Integer, ForeignKey('chats.chat_id'))
)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    profile = Column(Text, nullable=True)
    record_instructions = Column(Integer, default=0)
    chats = relationship('Chat', secondary=user_chats, back_populates='users')

class Provider(Base):
    __tablename__ = 'providers'
    provider_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    api_endpoint = Column(String(255), nullable=False)

class LLM(Base):
    __tablename__ = 'llms'
    llm_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    provider_id = Column(Integer, ForeignKey('providers.provider_id'), nullable=False)
    provider = relationship(Provider)

class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    users = relationship('User', secondary=user_chats, back_populates='chats')

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    llm_id = Column(Integer, ForeignKey('llms.llm_id'), nullable=True)
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    timestamp = Column(DateTime, default=datetime.datetime.now)
    user = relationship(User)
    chat = relationship(Chat)
    llm = relationship(LLM)

class InstructionRecord(Base):
    __tablename__ = 'instruction_records'
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    instruction = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    user = relationship(User)
    chat = relationship(Chat)

class DatabaseManageUnit:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def init_db(self):
        connection = self.engine.connect()
        connection.execute(text("DROP TABLE IF EXISTS user_chats CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS instruction_records CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS messages CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS chats CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS llms CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS providers CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        connection.close()
        Base.metadata.create_all(self.engine)

    def reset_db(self):
        self.init_db()

    def query_user_by_username(self, username):
        session = self.Session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            self.Session.remove()

    def query_user_by_id(self, user_id):
        session = self.Session()
        try:
            return session.query(User).get(user_id)
        finally:
            self.Session.remove()

    def query_all_users(self):
        session = self.Session()
        try:
            return session.query(User).all()
        finally:
            self.Session.remove()

    def add_user(self, username, profile):
        session = self.Session()
        try:
            new_user = User(username=username, profile=profile)
            session.add(new_user)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def update_user(self, user):
        session = self.Session()
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def delete_user(self, user):
        session = self.Session()
        try:
            session.delete(user)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def add_chat(self, title):
        session = self.Session()
        try:
            new_chat = Chat(title=title)
            session.add(new_chat)
            session.commit()
            return new_chat.chat_id
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def query_chat_by_id(self, chat_id):
        session = self.Session()
        try:
            return session.query(Chat).get(chat_id)
        finally:
            self.Session.remove()

    def query_all_chats(self):
        session = self.Session()
        try:
            return session.query(Chat).options(joinedload(Chat.users)).all()
        finally:
            self.Session.remove()

    def add_users_to_chat(self, chat_id, usernames):
        session = self.Session()
        try:
            chat = session.query(Chat).get(chat_id)
            users = session.query(User).filter(User.username.in_(usernames)).all()
            for user in users:
                chat.users.append(user)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def update_chat(self, chat):
        session = self.Session()
        try:
            session.add(chat)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def delete_chat(self, chat):
        session = self.Session()
        try:
            session.delete(chat)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def add_provider(self, name, api_endpoint):
        session = self.Session()
        try:
            new_provider = Provider(name=name, api_endpoint=api_endpoint)
            session.add(new_provider)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def query_provider_by_id(self, provider_id):
        session = self.Session()
        try:
            return session.query(Provider).get(provider_id)
        finally:
            self.Session.remove()

    def query_provider_by_name(self, name):
        session = self.Session()
        try:
            return session.query(Provider).filter_by(name=name).first()
        finally:
            self.Session.remove()

    def query_all_providers(self):
        session = self.Session()
        try:
            return session.query(Provider).all()
        finally:
            self.Session.remove()

    def update_provider(self, provider):
        session = self.Session()
        try:
            session.add(provider)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def delete_provider(self, provider):
        session = self.Session()
        try:
            session.delete(provider)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def add_llm(self, name, provider_id):
        session = self.Session()
        try:
            new_llm = LLM(name=name, provider_id=provider_id)
            session.add(new_llm)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def query_llm_by_id(self, llm_id):
        session = self.Session()
        try:
            return session.query(LLM).get(llm_id)
        finally:
            self.Session.remove()

    def query_llm_by_name_and_provider(self, name, provider_id):
        session = self.Session()
        try:
            return session.query(LLM).filter_by(name=name, provider_id=provider_id).first()
        finally:
            self.Session.remove()

    def query_all_llms(self):
        session = self.Session()
        try:
            return session.query(LLM).all()
        finally:
            self.Session.remove()

    def update_llm(self, llm):
        session = self.Session()
        try:
            session.add(llm)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def delete_llm(self, llm):
        session = self.Session()
        try:
            session.delete(llm)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()
    
    def query_message_by_id(self, message_id):
        session = self.Session()
        try:
            return session.query(Message).options(joinedload(Message.llm).joinedload(LLM.provider)).get(message_id)
        finally:
            self.Session.remove()

    def add_message(self, chat_id, user_id, content, role, llm_id=None):
        session = self.Session()
        try:
            new_message = Message(chat_id=chat_id, user_id=user_id, content=content, role=role, llm_id=llm_id)
            session.add(new_message)
            session.commit()
            return new_message.message_id  # Return ID instead of the object
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def enable_instruction_recording(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).get(user_id)
            user.record_instructions = 1
            session.commit()
            return {"status": "success", "message": "Instruction recording enabled."}
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def disable_instruction_recording(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).get(user_id)
            user.record_instructions = 0
            session.commit()
            return {"status": "success", "message": "Instruction recording disabled."}
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def record_instruction(self, user_id, chat_id, instruction):
        session = self.Session()
        try:
            new_record = InstructionRecord(user_id=user_id, chat_id=chat_id, instruction=instruction)
            session.add(new_record)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def delete_instruction_records(self, user_id):
        session = self.Session()
        try:
            session.query(InstructionRecord).filter_by(user_id=user_id).delete()
            session.commit()
            return {"status": "success", "message": "Instruction records deleted."}
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def list_instruction_records(self, user_id):
        session = self.Session()
        try:
            records = session.query(InstructionRecord).filter_by(user_id=user_id).all()
            return [{"record_id": record.record_id, "chat_id": record.chat_id, "instruction": record.instruction, "timestamp": record.timestamp} for record in records]
        finally:
            self.Session.remove()

    def handle_instruction(self, instruction_type, data):
        if instruction_type == 'USER_INSTRUCTION_RECORDING_ENABLE':
            return self.enable_instruction_recording(data['user_id'])
        elif instruction_type == 'USER_INSTRUCTION_RECORDING_DISABLE':
            return self.disable_instruction_recording(data['user_id'])
        elif instruction_type == 'USER_INSTRUCTION_RECORDS_DELETE':
            return self.delete_instruction_records(data['user_id'])
        elif instruction_type == 'USER_INSTRUCTION_RECORDS_LIST':
            return self.list_instruction_records(data['user_id'])
        # Handle other instruction-related operations here...

    def commit_session(self):
        session = self.Session()
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            self.Session.remove()