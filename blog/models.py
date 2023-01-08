from datetime import datetime

from sqlalchemy import (
    create_engine,
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    func,
    PrimaryKeyConstraint,
)


from sqlalchemy.orm import (
    declarative_base,
    Session as SessionType,
    sessionmaker,
    scoped_session,
    relationship,
    backref,
)

DB_URL = "sqlite:///db.sqlite3"
DB_URL_TEST = "sqlite:///test_db.sqlite3"
DB_ECHO = False

def create_db_engine(url: str, echo: bool):
    engine = create_engine(url=url, echo=echo)
    return engine

engine = create_db_engine(DB_URL, DB_ECHO)

Base = declarative_base(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    age = Column(Integer, nullable=False)

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username!r}, age={self.age})"

    def __repr__(self) -> str:
        return f'From repr! {str(self)}'


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(32), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship(User, backref=backref("posts", lazy="dynamic"))


class Tag(Base):

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class PostTag(Base):

    __tablename__ = "post_tag"
    __table_args__ = (
        PrimaryKeyConstraint('post_id', 'tag_id'),
    )
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

