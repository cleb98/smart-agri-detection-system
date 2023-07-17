import requests

API_PATCH_URL_USER = "https://insects_api-1-q3217764.deta.app/user/update/{}"
API_PATCH_URL_MICRO = "https://insects_api-1-q3217764.deta.app/microcontroller/update_status/{}"

USER_ID = 4

def test_1():

    print(API_PATCH_URL_USER.format(4))
    


    data_user = {
        "chat_id": 123456789,
    }

    response = requests.patch(API_PATCH_URL_USER.format(4), json=data_user)

    print(response.status_code)
    print(response.json())

def test_2():

    data_micro = {
        "status": True,
    }

    response = requests.patch(API_PATCH_URL_MICRO.format(16), json=data_micro)

    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    test_1()
    test_2()