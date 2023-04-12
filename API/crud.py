# In this file we will have reusable functions to interact with the data in the database

from sqlalchemy.orm import Session
import models, schemas


#------------------------------------------------create------------------------------------------------------#

def create_user_item(db: Session, item: schemas.create_users_schema):
    """
    create a user
    """
    db_item = models.users_model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_microcontroller_item(db: Session, item: schemas.create_microcontrollers_schema):
    """
    create a microcontroller owned by a user
    """
    db_item = models.microcontrollers_model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_image_item(db: Session, item: schemas.create_images_schema):
    """
    create a image taken by a microcontroller
    """
    db_item = models.images_model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#-------------------------------------------------read-------------------------------------------------------#

def get_user(db: Session, user_id: int):
    """
    gets the user filtered by the id
    """
    return db.query(models.users_model).filter(models.users_model.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    gets all users
    """
    return db.query(models.users_model).offset(skip).limit(limit).all()

def get_user_by_microcontroller(db: Session, micro_id: int):
    """
    gets the user filtered by the micro id
    """
    microcontroller = db.query(models.microcontrollers_model).filter(models.microcontrollers_model.id == micro_id).first()
    if microcontroller is None:
        return None
    return db.query(models.users_model).filter(models.users_model.id == microcontroller.user_id).first()


def get_microcontroller(db: Session, micro_id: int):
    """
    gets the microcontroller filtered by the id
    """
    return db.query(models.microcontrollers_model).filter(models.microcontrollers_model.id == micro_id).first()

def get_microcontrollers(db: Session, skip: int = 0, limit: int = 100):
    """
    gets all microcontrollers
    """
    return db.query(models.microcontrollers_model).offset(skip).limit(limit).all()

# per prima cosa devo controllare che l'user_id esista
def get_microcontrollers_by_user(db: Session, user_id: int):
    """
    gets the microcontrollers filtered by the user id
    """
    return db.query(models.microcontrollers_model).filter(models.microcontrollers_model.user_id == user_id).all()


def get_image(db: Session, image_id: int):
    """
    get the image filtered by the id
    """
    return db.query(models.images_model).filter(models.images_model.id == image_id).first()

def get_images(db: Session, skip: int = 0, limit: int = 100):
    """
    get all images
    """
    return db.query(models.images_model).offset(skip).limit(limit).all()

def get_images_by_microcontroller(db: Session, micro_id: int):
    """
    get the images filtered by the the micro id
    """
    return db.query(models.images_model).filter(models.images_model.micro_id == micro_id).all()

def get_unchecked_images(db: Session):
    """
    get all images where checked is False
    """
    return db.query(models.images_model).filter(models.images_model.checked == False).all()

#------------------------------------------------update------------------------------------------------------#

def update_user_item(db: Session, item: schemas.update_users_schema, user_id: int):
    """
    update a user
    """
    stored_db_item = db.get(models.users_model, user_id)
    db_update_data = item.dict(exclude_unset=True)
    for key, value in db_update_data.items():
        setattr(stored_db_item, key, value)
    db.add(stored_db_item)
    db.commit()
    db.refresh(stored_db_item)
    return stored_db_item

def update_microcontroller_status_item(db: Session, item: schemas.update_microcontrollers_status_schema, micro_id: int):
    """
    update a status' microcontroller
    """
    stored_db_item = db.get(models.microcontrollers_model, micro_id)
    db_update_data = item.dict(exclude_unset=True)
    for key, value in db_update_data.items():
        setattr(stored_db_item, key, value)
    db.add(stored_db_item)
    db.commit()
    db.refresh(stored_db_item)
    return stored_db_item

def update_microcontroller_item(db: Session, item: schemas.update_microcontroller_schema, micro_id: int):
    """
    update a microcontroller
    """
    stored_db_item = db.get(models.microcontrollers_model, micro_id)
    db_update_data = item.dict(exclude_unset=True)
    for key, value in db_update_data.items():
        setattr(stored_db_item, key, value)
    db.add(stored_db_item)
    db.commit()
    db.refresh(stored_db_item)
    return stored_db_item

def update_images_unchecked_item(db: Session, item: schemas.update_images_checked_schema, image_id: int):
    """
    update images' checked field
    """
    stored_db_item = db.get(models.images_model, image_id)
    db_update_data = item.dict(exclude_unset=True)
    for key, value in db_update_data.items():
        setattr(stored_db_item, key, value)
    db.add(stored_db_item)
    db.commit()
    db.refresh(stored_db_item)
    return stored_db_item
#------------------------------------------------delete------------------------------------------------------#

def delete_user_item(db: Session, user_id: int):
    """
    delete a user
    """
    db_item = db.get(models.users_model, user_id)
    db.delete(db_item)
    db.commit()
    return db_item

def delete_users_items(db: Session):
    """
    delete all users
    """
    db_items = db.query(models.users_model).delete()
    db.commit()
    return db_items


def delete_microcontroller_item(db: Session, micro_id: int):
    """
    delete a microcontroller
    """
    db_item = db.get(models.microcontrollers_model, micro_id)
    db.delete(db_item)
    db.commit()
    return db_item

def delete_microcontrollers_items(db: Session):
    """
    delete all microcontrollers
    """
    db_items = db.query(models.microcontrollers_model).delete()
    db.commit()
    return db_items

def delete_microcontrollers_items_by_user(db: Session, user_id: int):
    """
    delete all microcontrollers filtered by user
    """

    db_items = db.query(models.microcontrollers_model).filter(models.microcontrollers_model.user_id == user_id).delete()
    db.commit()
    return db_items


def delete_image_item(db: Session, image_id: int):
    """
    delete an image
    """
    db_item = db.get(models.images_model, image_id)
    db.delete(db_item)
    db.commit()
    return db_item

def delete_images_items(db: Session):
    """
    delete all images
    """
    db_items = db.query(models.images_model).delete()
    db.commit()
    return db_items

def delete_images_items_by_microcontrollers(db: Session, micro_id: int):
    """
    delete all images taken by a microcontroller
    """
    db_items = db.query(models.images_model).filter(models.images_model.micro_id == micro_id).delete()
    db.commit()
    return db_items
