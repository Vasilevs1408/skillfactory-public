from tests.api import PetFriends
from tests.settings import valid_email, valid_pass, invalid_email, invalid_pass
import os


pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_pass):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_get_api_key_invalid_user(email=invalid_email, password=valid_pass):
    """ Проверяем что запрос api ключа от несуществующего пользователя не возвращает статус 200"""

    status, result = pf.get_api_key(email, password)
    assert status != 200

def test_get_api_key_invalid_pass(email=valid_email, password=invalid_pass):
    """ Проверяем что запрос api ключа при введении некорректного пароля не возвращает статус 200"""

    status, result = pf.get_api_key(email, password)
    assert status != 200

def test_add_new_pet_with_invalid_pet_name(name='1234', animal_type='двортерьер', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с именем содержащим цифры вместо букв"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['name'] != name

def test_add_new_pet_with_invalid_pet_type(name='Барбоскин', animal_type='1234', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с породой содержащим цифры вместо букв"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['animal_type'] != animal_type

def test_add_new_pet_with_invalid_pet_age(name='Барбоскин', animal_type='двортерьер', age='пять', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с возастом содержащим буквы вместо цифр"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['age'] != age

def test_add_new_pet_with_valid_pet_without_photo(name='No_photo_pet', animal_type='двортерьер', age='5'):
    """Проверяем что можно добавить питомца без фото c корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.pet_information_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''

def test_successful_update_self_pet_photo(pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления фото к питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "No_photo_pet", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_photo_of_pets(auth_key, pet_id, pet_photo)

    assert status == 200
    assert pet_id not in my_pets.values()

def test_get_api_key_not_email_and_pass(email="", password=""):
    """ Проверяем что запрос api ключа без ввода имени и пароля не возвращает статус 200"""

    status, result = pf.get_api_key(email, password)
    assert status != 200

def test_add_new_pet_with_not_parameters(name='', animal_type='', age='', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца без указанных параметров"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['name'] != name
    assert result['animal_type'] != animal_type
    assert result['age'] != age

def test_add_new_pet_with_not_parameters_and_pet_photo(name='', animal_type='', age='', pet_photo=''):
    """Проверяем что нельзя добавить питомца без указанных параметров"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['name'] != name
    assert result['animal_type'] != animal_type
    assert result['age'] != age
    assert result['pet_photo'] != pet_photo
