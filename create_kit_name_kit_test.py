import sender_stand_request
import data
import requests
import configuration


# Получение токена пользователя
def get_user_token():
    return requests.post(configuration.URL_SERVICE+configuration.CREATE_USER_PATH,
                         json=data.user_body,
                         headers=data.headers
                         )
response_token=get_user_token()
data.auth_token["Authorization"] = "Bearer" + response_token.json()["authToken"]



# Функция для изменения значения в параметре name в теле запроса
def get_kit_body(name):
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body


# Функция для позитивной проверки
def positive_assert(name):
    kit_body = get_kit_body(name)
    kit_response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert kit_response.status_code == 201

    assert kit_response.json()["name"] == name



def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert("a")


def test_create_kit_511_letter_in_name_get_success_response():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


def test_create_kit_english_letter_in_name_get_success_response():
    positive_assert("QWErty")


def test_create_kit_russian_letter_in_name_get_success_response():
    positive_assert("Мария")


def test_create_kit_has_special_symbol_in_name_get_success_response():
    positive_assert("\"№%@\",")


def test_create_kit_has_space_in_name_get_success_response():
    positive_assert("Человек и Ко")


def test_create_kit_has_number_in_name_get_success_response():
    positive_assert("123")



# Функция для негативной проверки
def negative_assert_code_400(kit_body):
    response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert response.status_code == 400


def test_create_kit_512_letter_in_name_get_error_response():
    kit_body = get_kit_body("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

    negative_assert_code_400(kit_body)


def test_create_kit_empty_name_get_error_response():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)


def test_create_kit_number_type_name_get_error_response():
    kit_body = get_kit_body(123)
    negative_assert_code_400(kit_body)


def test_create_kit_no_name_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    negative_assert_code_400(kit_body)



