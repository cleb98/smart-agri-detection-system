# Create Pydantic models (schemas) that will be used when creating, reading, updating, deleting data

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Union

#-----------------------------------------images schemas---------------------------------------#

class read_images_schema(BaseModel):
    """
    schema containing images from microcontrollers
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    datetime: datetime
    contents: str
    species: str
    binaryimage: str
    checked: bool
    micro_id: int


class create_images_schema(BaseModel):
    """
    schema for adding a new image taken by a microcontroller
    """
    model_config = ConfigDict(from_attributes=True)

    datetime: datetime
    contents: str
    species: str
    binaryimage: str
    checked: bool = False
    micro_id: int


class update_images_checked_schema(BaseModel):
    """
    schema for updating images checked field
    """
    model_config = ConfigDict(from_attributes=True)

    checked: bool

#-----------------------------------microcontrollers schemas-----------------------------------#

class read_microcontrollers_schema(BaseModel):
    """
    schema containing microcontrollers 
    """ 
    model_config = ConfigDict(from_attributes=True)

    id: int
    lat: float
    long: float
    status: bool
    user_id: int
    images: list[read_images_schema] = []


class create_microcontrollers_schema(BaseModel):
    """
    schema for adding a new microcontroller owned by a user
    """
    model_config = ConfigDict(from_attributes=True)

    lat: float
    long: float
    status: bool = False
    user_id: int


class update_microcontrollers_status_schema(BaseModel):
    """
    schema for updating microcontroller status
    """
    model_config = ConfigDict(from_attributes=True)

    status: bool

class update_microcontroller_schema(BaseModel):
    """
    schema for updating a microcontroller
    """
    model_config = ConfigDict(from_attributes=True)

    lat: float
    long: float
    status: Optional[bool] = False


#---------------------------------------users schemas------------------------------------------#

class read_users_schema(BaseModel):
    """
    schema containing users
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    chat_id: Optional[int] = None
    microcontrollers: list[read_microcontrollers_schema] = []


class create_users_schema(BaseModel):
    """
    schema for adding a new user
    """
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str
    chat_id: Optional[int] = None


class update_users_schema(BaseModel):
    """
    schema for updating an existing user
    """
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = None
    email: Optional[str] = None
    chat_id: Optional[int] = None

