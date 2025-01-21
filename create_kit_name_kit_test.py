import sender_stand_request
import data
from data import created_kit


def get_kit_body(name):
    current_body = data.created_kit.copy()
    current_body["name"] = name
    return current_body

def get_new_user_token():
    user_body = data.user_body
    resp_user = sender_stand_request.post_new_user(user_body)
    return resp_user.json()["authToken"]

def positive_assert(kit_body):
    kit_body = get_kit_body(kit_body)
    kit_body_response = sender_stand_request.post_new_client_kit(kit_body)

    assert kit_body_response.status_code == 201
    assert kit_body_response.json()["authToken"] != ""

    str_kit = created_kit["name"] + kit_body_response.json()["authToken"]
    assert kit_body_response.text.count(str_kit) == 1

def negative_assert_code_400(kit_body):
    kit_body = get_kit_body(kit_body)
    kit_body_response = sender_stand_request.post_new_client_kit(kit_body)

    assert kit_body_response.status_code == 400
    assert kit_body_response.json()["code"] != 400
    assert kit_body_response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

def negative_assert_no_name(create_kit):
    response = sender_stand_request.post_new_client_kit(create_kit)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

def test1_create_kit_1_letter_in_kit_name_get_success_response():
    positive_assert("a")

def test2_create_kit_511_letters_in_kit_name_get_success_response():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

def test3_create_kit_special_characters_in_kit_name_get_success_response():
    positive_assert("\"№%@\",")

def test4_create_kit_has_spaces_in_kit_name_get_success_response():
    positive_assert("A Aaa")

def test5_create_kit_has_numbers_in_kit_name_get_success_response():
    positive_assert("123")

def test6_create_kit_0_characters_in_kit_name_get_error_response():
    create_kit = get_kit_body("")
    negative_assert_no_name(create_kit)

def test7_create_kit_512_letters_in_kit_name_get_error_response():
    negative_assert_code_400("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

def test8_create_kit_no_name_in_kit_name_get_error_response():
    create_kit = data.create_kit.copy()
    create_kit.pop("name")
    negative_assert_no_name(create_kit)

def test9_create_kit_number_inkit__name_get_error_response():
    create_kit = get_kit_body(123)
    response = sender_stand_request.post_new_client_kit(create_kit)

    assert response.status_code == 400