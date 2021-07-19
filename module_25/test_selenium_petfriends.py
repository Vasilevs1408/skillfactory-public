import pytest
from settings import valid_email, valid_pass, amount_pet_card
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope='session')
def testing():
    driver = webdriver.Chrome('C:/Users/vasha/PycharmProjects/module_25/Chrome/chromedriver.exe')
    driver.get('http://petfriends1.herokuapp.com/login')


    yield driver

    driver.quit()


def test_show_pets(testing):
    testing.find_element_by_id('email').send_keys(valid_email)
    testing.find_element_by_id('pass').send_keys(valid_pass)
    testing.find_element_by_css_selector('button[type="submit"]').click()
    testing.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[1]/a').click()
    assert testing.find_element_by_tag_name('h2').text == "Василий"

    images = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//th/img')))
    pet_card = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
    names = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//td[1]')))
    species = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//td[2]')))
    age = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//td[3]')))


    pet_photo = []


    # проверяем наличие всех питомцев
    assert len(pet_card) == amount_pet_card
    # проверяем наличие у всех питомцев имени, породы и возраста
    for i in range(len(pet_card)):
        assert names[i].text != ''
        assert species[i].text != ''
        assert age[i].text != ''
        # проверяем наличие фотографии хотя бы у половины питомцев
        if images[i].get_attribute('src') != '':
            pet_photo.append(i)
        return pet_photo
    assert len(pet_photo) >= amount_pet_card / 2


def test_pets_names(testing):
    testing.find_element_by_id('email').send_keys(valid_email)
    testing.find_element_by_id('pass').send_keys(valid_pass)
    testing.find_element_by_css_selector('button[type="submit"]').click()
    testing.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[1]/a').click()
    assert testing.find_element_by_tag_name('h2').text == "Василий"


    names = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//td[1]')))

    names_list = []
    # проверяем, нет ли в списке питомцев, с повторяющимися именами
    for name in names:
        name = name.text
        if name.isalpha():
            names_list.append(name)
        else: print('имя содержит недопутимые знаки')


    set_names_list = set(names_list)

    assert len(names) == len(set_names_list)


def test_duplicate_pets(testing):
    testing.find_element_by_id('email').send_keys(valid_email)
    testing.find_element_by_id('pass').send_keys(valid_pass)
    testing.find_element_by_css_selector('button[type="submit"]').click()
    testing.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[1]/a').click()
    assert testing.find_element_by_tag_name('h2').text == "Василий"


    pet_characters = WebDriverWait(testing, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.table.table-hover td')))

    k = 4

    del pet_characters[k - 1::k]
    # прверяем, нет ли в списке одинаковых питомцев
    characters_list = []
    for char in pet_characters:
        char = char.text
        characters_list.append(char)

    print(characters_list)



    characters_list = tuple(characters_list)



    char_tuple = tuple(characters_list[i:i + 3] for i in range(0, len(characters_list), 3))



    set_char_tuple = set(char_tuple)



    assert len(char_tuple) == len(set_char_tuple)