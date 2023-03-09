# Create SQLAlchemy models from the Base class

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base


class users_model(Base):
    """
    model containing users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, unique=True, nullable=True)

    microcontrollers = relationship("microcontrollers_model", back_populates="user", cascade="all, delete")

class microcontrollers_model(Base):
    """
    model containing microcontrollers
    """
    __tablename__ = "microcontrollers"

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("users_model", back_populates="microcontrollers")

    images = relationship("images_model", back_populates="micro", cascade="all, delete")

class images_model(Base):
    """
    model containing images from microcontrollers
    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    contents = Column(String, nullable=False)
    species = Column(String, nullable=False)
    binaryimage = Column(String, nullable=False)

    micro_id = Column(Integer, ForeignKey('microcontrollers.id'))

    micro = relationship("microcontrollers_model", back_populates="images")
