from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Insect Detection API', description='A simple API that monitors the status of crops based on the presence of pests', version='0.1')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#---------------------------------------------create----------------------------------------------------------#

@app.post("/user/add/", response_model=schemas.read_users_schema)
def create_user(item: schemas.create_users_schema, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item)

@app.post("/microcontroller/add/", response_model=schemas.read_microcontrollers_schema)
def create_microcontroller(item: schemas.create_microcontrollers_schema, db: Session = Depends(get_db)):
    return crud.create_microcontroller_item(db=db, item=item)

@app.post("/image/add/", response_model=schemas.read_images_schema)
def create_image(item: schemas.create_images_schema, db: Session = Depends(get_db)):
    return crud.create_image_item(db=db, item=item)

#---------------------------------------------read-----------------------------------------------------------#

@app.get("/user/{user_id}", response_model=schemas.read_users_schema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    route that retrieves a single user
    """
    item = crud.get_user(db=db, user_id=user_id)
    if item is None:
        raise HTTPException(status_code=404, detail='user not found')
    return item

@app.get("/users/", response_model=List[schemas.read_users_schema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    route that retrieves all users
    """
    items = crud.get_users(db=db, skip=skip, limit=limit)
    if items is None:
        raise HTTPException(status_code=404, detail='users not found')
    return items

@app.get("/user/microcontroller/{micro_id}", response_model=schemas.read_users_schema)
def read_user_by_microcontroller(micro_id: int, db: Session = Depends(get_db)):
    """
    route that retrieves the owner of a single microcontroller
    """
    item = crud.get_user_by_microcontroller(db=db, micro_id=micro_id)
    if item is None:
        raise HTTPException(status_code=404, detail='user associated to microcontroller not found')
    return item


@app.get("/microcontroller/{micro_id}", response_model=schemas.read_microcontrollers_schema)
def read_microcontroller(micro_id: int, db: Session = Depends(get_db)):
    """
    route that retrieves a single microcontroller
    """
    item = crud.get_microcontroller(db=db, micro_id=micro_id)
    if item is None:
        raise HTTPException(status_code=404, detail='microcontroller not found')
    return item

@app.get("/microcontrollers/", response_model=List[schemas.read_microcontrollers_schema])
def read_microcontrollers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    route that retrieves all microcontrollers
    """
    items = crud.get_microcontrollers(db=db, skip=skip, limit=limit)
    if items is None:
        raise HTTPException(status_code=404, detail='microcontrollers not found')
    return items

@app.get("/microcontrollers/user/{user_id}", response_model=List[schemas.read_microcontrollers_schema])
def read_microcontrollers_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    route that retrieves all microcontrollers owned by a single user
    """
    items = crud.get_microcontrollers_by_user(db=db, user_id=user_id)
    if not items:
        raise HTTPException(status_code=404, detail='microcontrollers owned by the user not found')
    return items


@app.get("/image/{image_id}", response_model=schemas.read_images_schema)
def read_image(image_id: int, db: Session = Depends(get_db)):
    """
    route that retrieves a single image
    """
    item = crud.get_image(db=db, image_id=image_id)
    if item is None:
        raise HTTPException(status_code=404, detail='image not found')
    return item

@app.get("/images/", response_model=List[schemas.read_images_schema])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    route that retrieves all images
    """
    items = crud.get_images(db=db, skip=skip, limit=limit)
    if items is None:
        raise HTTPException(status_code=404, detail='images not found')
    return items

@app.get("/images/microcontroller/{micro_id}", response_model=List[schemas.read_images_schema])
def read_images_by_microcontroller(micro_id: int, db: Session = Depends(get_db)):
    """
    route that retrieves all images taken by a single microcontroller
    """
    items = crud.get_images_by_microcontroller(db=db, micro_id=micro_id)
    if not items:
        raise HTTPException(status_code=404, detail='images taken by the microcontroller not found')
    return items

#---------------------------------------------update----------------------------------------------------------#

@app.patch("/user/update/{user_id}", response_model=schemas.read_users_schema)
def update_user(user_id: int, item: schemas.update_users_schema, db: Session = Depends(get_db)):
    """
    route that update a single user
    """
    try:
        return crud.update_user_item(db=db, item=item, user_id=user_id)
    except:
        raise HTTPException(status_code=404, detail='user not found')

@app.patch("/microcontroller/update_status/{micro_id}", response_model=schemas.read_microcontrollers_schema)
def update_microcontroller_status(micro_id: int, item: schemas.update_microcontrollers_status_schema, db: Session = Depends(get_db)):
    """
    route that update status' microcontroller
    """
    try:
        return crud.update_microcontroller_status_item(db=db, item=item, micro_id=micro_id)
    except:
        raise HTTPException(status_code=404, detail='microcontroller not found')

@app.patch("/microcontroller/update/{micro_id}", response_model=schemas.read_microcontrollers_schema)
def update_microcontroller(micro_id: int, item: schemas.update_microcontroller_schema, db: Session = Depends(get_db)):
    """
    route that update a single microcontroller
    """
    try:
        return crud.update_microcontroller_item(db=db, item=item, micro_id=micro_id)
    except:
        raise HTTPException(status_code=404, detail='microcontroller not found')

#---------------------------------------------delete----------------------------------------------------------#

@app.delete("/user/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    route that deletes a single user
    """
    try:
        item = crud.delete_user_item(db=db, user_id=user_id)
        return {"message": f"user {item.name} deleted"}
    except:
        raise HTTPException(status_code=404, detail='user not found')

@app.delete("/users/delete/")
def delete_all_users(db: Session = Depends(get_db)):
    """
    route that deletes all users
    """
    items = crud.delete_users_items(db=db)
    if not items:
        raise HTTPException(status_code=404, detail='users not found')
    return {"messages": "users deleted"}


@app.delete("/microcontroller/delete/{micro_id}")
def delete_microcontroller(micro_id: int, db: Session = Depends(get_db)):
    """
    route that deletes a single microcontroller
    """
    try:
        item = crud.delete_microcontroller_item(db=db, micro_id=micro_id)
        return {"message": f"micro {item.id} deleted"}
    except:
        raise HTTPException(status_code=404, detail='microcontroller not found')

@app.delete("/microcontrollers/delete/{user_id}")
def delete_microcontrollers_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    route that deletes all microcontrollers owned by a user
    """
    items = crud.delete_microcontrollers_items_by_user(db=db, user_id=user_id)
    if not items:
        raise HTTPException(status_code=404, detail='microcontrollers owned by user not found')
    return {"messages": f"microcontrollers owned by user {str(user_id)} deleted"}

@app.delete("/microcontrollers/delete/")
def delete_all_microcontrollers(db: Session = Depends(get_db)):
    """
    route that deletes all microcontrollers
    """
    items = crud.delete_microcontrollers_items(db=db)
    if not items:
        raise HTTPException(status_code=404, detail='microcontrollers not found')
    return {"messages": "microcontrollers deleted"}


@app.delete("/image/delete/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    """
    route that deletes a single image
    """
    try:
        item = crud.delete_image_item(db=db, image_id=image_id)
        return {"message": f"image {item.id} deleted"}
    except:
        raise HTTPException(status_code=404, detail='image not found')

@app.delete("/images/delete/{micro_id}")
def delete_all_images_by_microcontroller(micro_id: int, db: Session = Depends(get_db)):
    """
    route that deletes all images taken by a single microcontroller
    """
    items = crud.delete_images_items_by_microcontrollers(db=db, micro_id=micro_id)
    if not items:
        raise HTTPException(status_code=404, detail='images taken by the microcontroller not found')
    return {"messages": f"images taken by microcontroller {str(micro_id)} deleted"}

@app.delete("/images/delete/")
def delete_all_images(db: Session = Depends(get_db)):
    """
    route that deletes all images
    """
    items = crud.delete_images_items(db=db)
    if not items:
        raise HTTPException(status_code=404, detail='images not found')
    return {"messages": "images deleted"}
