import requests

API_PATCH_URL_USER = "https://insects_api-1-q3217764.deta.app/user/update/{}"
API_PATCH_URL_MICRO_STATUS = "https://insects_api-1-q3217764.deta.app/microcontroller/update_status/{}"
API_PATCH_URL_MICRO = "https://insects_api-1-q3217764.deta.app/microcontroller/update/{}"

def test_1():

    data_user = {
        "chat_id": 4235,
    }

    response = requests.patch(API_PATCH_URL_USER.format(10), json=data_user)

    print(response.status_code)
    print(response.json())

def test_2():

    data_micro = {
        "status": False,
    }

    response = requests.patch(API_PATCH_URL_MICRO_STATUS.format(16), json=data_micro)

    print(response.status_code)
    print(response.json())

def test_3():

    data_micro = {
        "lat": 44.630116088128766,
        "long": 10.860960713545573
    }

    response = requests.patch(API_PATCH_URL_MICRO.format(17), json=data_micro)

    print(response.status_code)
    print(response.json())

def test_4():

    data_user = {
        "name": "ahahahaha"
    }

    response = requests.patch(API_PATCH_URL_USER.format(21), json=data_user)
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    test_1()
    # test_2()
    # test_3()
    # test_4()