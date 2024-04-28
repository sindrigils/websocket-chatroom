from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    servers = relationship("Server", back_populates="admin_user")

    def __repr__(self):
        return f"<Client(username={self.username}>"


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    port = Column(Integer, unique=True, nullable=False)
    admin = Column(Integer, ForeignKey("clients.id"), nullable=False)

    admin_user = relationship("Client", back_populates="servers")

    def __repr__(self):
        return f"<Server(name={self.name}, admin={self.admin_user})>"
