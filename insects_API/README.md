# RESTful API

## Database

### Tools Used

- **[Supabase](https://supabase.com/)** is an open source PostgreSQL-based platform for building web and mobile applications and developing back-end applications using SQL and JavaScript.
- It offers features such as authentication, authorization, data management and real-time notifications.
- It can run on cloud infrastructure such as AWS, GCP and DigitalOcean or locally.

### Schema

![Database Schema](/insect-detection-iot-system/insects_API/API/assets/database_structure.png)

- **Three tables:** 
    - **"users"** contains information about users, such as their name, email address, and chat id used by the telegram bot.
    - **"microcontrollers"** contains information about the microcontrollers, such as location and status.
    - **"images"** contains information about the images captured by the microcontrollers, such as the date and time of capture, the species detected, and the image itself in binary format.
- Foreign keys establish a link between information about users, their microcontrollers, and images acquired by microcontrollers.

## API

### Tools Used

- **[FastAPI](https://fastapi.tiangolo.com/)** is a modern, high-performance web framework for creating APIs in Python.
- It is compatible with open standards for APIs, such as OpenAPI and JSON Schema, making it an excellent choice for creating RESTful APIs and other web services.
- The API has been deployed through **[Deta Space](https://deta.space/)**, a customizable cloud computing platform that offers complete control over users' data and applications.

### HTTP methods

- The methods used allow creating, reading, updating and deleting users, microcontrollers and images in the application.
- The HTTP methods of the API are used by:
    - Arduino
    - Telegram bots
    - Web Application

- #### **POST**
|route|description|
|-------|------------|
|`/user/add/`|create user|
|`/microcontroller/add/`|create microcontroller|
|`/image/add/`|create image|

- #### **GET**
|route|description|
|----|----|
|`/user/{user_id}/`|read user|
|`/users/`|read users|
|`/user/microcontroller/{micro_id}/`|read user by microcontroller|
|`/microcontroller/{micro_id}/`|read microcontroller|
|`/microcontrollers/`|read microcontrollers|
|`/microcontrollers/user/{user_id}/`|read microcontrollers by user|
|`/image/{image_id}/`|read image|
|`/images/`|read images|
|`/images/microcontroller/{micro_id}/`|read images by microcontroller|
|`/images/checked/`|read images by checked|

- #### **PATCH**
|route|description|
|-|-|
|`/user/update/{user_id}/`|update user|
|`/microcontroller/update_status/{micro_id}/`|update microcontroller status|
|`/microcontroller/update/{micro_id}/`|update microcontroller|
|`/images/update_checked/`|update image cheked|

- #### **DELETE**
|route|description|
|-|-|
|`/user/delete/{user_id}/`|delete user|
|`/users/delete/`|delete all users|
|`/microcontroller/delete/{micro_id}/`|delete microcontrollers|
|`/microcontrollers/delete/{user_id}/`|delete microcontrollers by user|
|`/microcontrollers/delete/`|delete all microcontrollers|
|`/image/delete/{image_id}/`|delete image|
|`/images/delete/{micro_id}/`|delete all images by microcontroller|
|`/images/delete/`|delete all images|
### Install Dependencies

```console
insect-detection-iot-system/insects_API/API pip install -r requirements.txt
```
---
### Run API
```console
insect-detection-iot-system/insects_API/API uvicorn main:app --reload
```

### API Documentation

- The FastAPI framework provides automatic documentation for API exploration and understanding.
- Due to its integration with the OpenAPI standard, two different options are available:
    - [Swagger UI](https://swagger.io/tools/swagger-ui/)
    - [ReDoc](https://redocly.com/redoc/)

> Go to http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc


