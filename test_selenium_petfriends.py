import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Настраиваем неявные ожидания:
    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

def test_show_all_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')

    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR,'card-deck, card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR,'card-deck, card-text')

    # Проверяем, что на странице есть фотографии питомцев, имена, порода (вид) и возраст питомцев не пустые строки:
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_show_my_pets(driver):
    # Вводим email, пароль, открываем главную страницу сайта
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    driver.find_element(By.ID, 'pass').send_keys('12345')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Нажимаем на кнопку Мои питомцы
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # Настраиваем явное ожидание
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "all_my_pets"))
    )


    # Проверяем, что мы оказались на странице "Мои питомцы"
    assert driver.find_element(By.TAG_NAME, 'h2').text == "Vasya"



    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)


