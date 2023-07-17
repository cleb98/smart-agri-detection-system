# Create Pydantic models (schemas) that will be used when creating, reading, updating, deleting data

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union

#-----------------------------------------images schemas---------------------------------------#

class read_images_schema(BaseModel):
    """
    schema containing images from microcontrollers
    """
    id: int
    datetime: datetime
    contents: str
    species: str
    binaryimage: str
    checked: bool
    micro_id: int

    class Config:
        orm_mode = True

class create_images_schema(BaseModel):
    """
    schema for adding a new image taken by a microcontroller
    """
    datetime: datetime
    contents: str
    species: str
    binaryimage: str
    checked: bool = False
    micro_id: int

    class Config:
        orm_mode = True

class update_images_checked_schema(BaseModel):
    """
    schema for updating images checked field
    """
    checked: bool

#-----------------------------------microcontrollers schemas-----------------------------------#

class read_microcontrollers_schema(BaseModel):
    """
    schema containing microcontrollers 
    """ 
    id: int
    lat: float
    long: float
    status: bool
    user_id: int
    images: list[read_images_schema] = []

    class Config:
        orm_mode = True

class create_microcontrollers_schema(BaseModel):
    """
    schema for adding a new microcontroller owned by a user
    """
    lat: float
    long: float
    status: bool = False
    user_id: int

    class Config:
        orm_mode = True

class update_microcontrollers_status_schema(BaseModel):
    """
    schema for updating microcontroller status
    """
    status: bool

class update_microcontroller_schema(BaseModel):
    """
    schema for updating a microcontroller
    """
    lat: float
    long: float
    status: Optional[bool] = False

    class Config:
        orm_mode = True

#---------------------------------------users schemas------------------------------------------#

class read_users_schema(BaseModel):
    """
    schema containing users
    """
    id: int
    name: str
    email: str
    chat_id: Optional[int] = None
    microcontrollers: list[read_microcontrollers_schema] = []

    class Config:
        orm_mode = True

class create_users_schema(BaseModel):
    """
    schema for adding a new user
    """
    name: str
    email: str
    chat_id: Optional[int] = None

    class Config:
        orm_mode = True

class update_users_schema(BaseModel):
    """
    schema for updating an existing user
    """
    name: Optional[str] = None
    email: Optional[str] = None
    chat_id: Optional[int] = None

    class Config:
        orm_mode = True
