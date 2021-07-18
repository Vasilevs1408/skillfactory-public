import pytest
from settings import valid_email, valid_pass
from selenium import webdriver


@pytest.fixture(scope='session')
def testing():
    driver = webdriver.Chrome('//Chrome/chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('http://petfriends1.herokuapp.com/login')


    yield driver

    driver.quit()


def test_show_my_pets(testing):
   testing.find_element_by_id('email').send_keys(valid_email)
   testing.find_element_by_id('pass').send_keys(valid_pass)
   testing.find_element_by_css_selector('button[type="submit"]').click()
   assert testing.find_element_by_tag_name('h1').text == "PetFriends"

   images = testing.find_elements_by_css_selector('.card-deck .card-img-top')
   names = testing.find_elements_by_css_selector('.card-deck .card-img-top')
   descriptions = testing.find_elements_by_css_selector('.card-deck .card-img-top')

   for i in range(len(names)):
       assert images[i].get_attribute('src') != ''
       assert names[i].text != ''
       assert descriptions[i].text != ''
       assert ', ' in descriptions[i]
       parts = descriptions[i].text.split(", ")
       assert len(parts[0]) > 0
       assert len(parts[1]) > 0