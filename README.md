# Proyecto Urban Grocers 

La automatización del proyecto es para comprobar la lista de comprobación para agregar un kit dentro de un usuario ya registrado, solo se toma en cuenta el nombre del kit.

Como primer punto, se tiene que hacer una solicitud de creación de nuevo usuario y obtener así tu Token de autenticación. 
Como segundo paso, se debe crear un kit para el usuario ya registrado.

La automatización y ejecución de la lista de comprobación fue realizada en PyCharm.




DATOS

- data.py

headers = {
    "Content-Type": "application/json",
    }

user_body = {
    "firstName": "Max",
    "phone": "+10005553535",
    "address": "8042 Lancaster Ave.Hamburg, NY"
}

created_kit = {
       "name": "Mi colección"
       }


ENVIO DE LAS SOLICITUDES

- sender_stand_request.py

import configuration
import requests
import data


def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)


response = post_new_user(data.user_body)
print(response.status_code)
print(response.json())

def post_new_client_kit(kit_body, auth_token):
    current_headers = data.headers.copy()
    current_headers["Authorization"] = "Bearer " + auth_token

    return requests.post(configuration.URL_SERVICE + configuration.KITS_PATH,
                         json=kit_body,
                         headers=current_headers)

print(response.status_code)


PRUEBAS

- create_kit_name_kit_test.py

import sender_stand_request
import data


def get_kit_body(name):
    current_kit_body = data.created_kit.copy()
    current_kit_body["name"] = name
    return current_kit_body

def get_new_user_token():
    user_body = data.user_body
    resp_user = sender_stand_request.post_new_user(user_body)
    return resp_user.json()["authToken"]

def positive_assert(kit_body):
    response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


def negative_assert_code_400(kit_body):
    response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

def test1_create_kit_1_letter_in_kit_name_get_success_response():
    current_kit_body = get_kit_body("a")
    positive_assert(current_kit_body)

def test2_create_kit_511_letters_in_kit_name_get_success_response():
    current_kit_body = get_kit_body ("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")
    positive_assert(current_kit_body)

def test3_create_kit_0_characters_in_kit_name_get_error_response():
    current_kit_body = get_kit_body("")
    negative_assert_code_400(current_kit_body)

def test4_create_kit_512_letters_in_kit_name_get_error_response():
    current_kit_body = get_kit_body("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
    negative_assert_code_400(current_kit_body)

def test5_create_kit_special_characters_in_kit_name_get_success_response():
    current_kit_body = get_kit_body("\"№%@\",")
    positive_assert(current_kit_body)

def test6_create_kit_has_spaces_in_kit_name_get_success_response():
    current_kit_body = get_kit_body("A Aaa")
    positive_assert(current_kit_body)

def test7_create_kit_has_numbers_in_kit_name_get_success_response():
    current_kit_body = get_kit_body("123")
    positive_assert(current_kit_body)

def test8_create_kit_no_name_in_kit_name_get_error_response():
    create_kit = data.created_kit.copy()
    create_kit.pop("name")
    negative_assert_code_400(create_kit)

def test9_create_kit_number_in_kit_name_get_error_response():
    current_kit_body = get_kit_body(123)
    negative_assert_code_400(current_kit_body)