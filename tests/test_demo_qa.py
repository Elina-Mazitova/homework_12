import os
import allure
from selene import have, be


@allure.title("Successful fill form")
def test_demo_qa(setup_browser):
    browser = setup_browser
    with allure.step("Открываем форму"):
        browser.open('https://demoqa.com/automation-practice-form')
        browser.element('#fixedban').perform(lambda _: None)
        if browser.element('#close-fixedban').matching(be.visible):
            browser.element('#close-fixedban').click()

    with allure.step("Заполняем поля имени и имейла"):
        browser.element('#firstName').type('Elina')
        browser.element('#lastName').type('QA')
        browser.element('#userEmail').type('elina.qa@example.com')

    with allure.step("Выбираем женский пол"):
        el_gender = browser.element("label[for='gender-radio-2']").locate()
        browser.driver.execute_script("arguments[0].click();", el_gender)

    with allure.step("Заполняем телефон и дату рождения"):
        browser.element('#userNumber').type('9991111111')
        el_date = browser.element('#dateOfBirthInput').locate()
        browser.driver.execute_script("arguments[0].click();", el_date)
        browser.element('.react-datepicker__year-select').type('1996').press_enter()
        browser.element('.react-datepicker__month-select').type('June').press_enter()
        browser.element('.react-datepicker__day--014:not(.react-datepicker__day--outside-month)').click()

    with allure.step("Выбираем предметы и хобби"):
        browser.element('#subjectsInput').type('Math').press_enter()
        browser.element('#subjectsInput').type('Computer Science').press_enter()
        el = browser.element("label[for='hobbies-checkbox-1']").locate()
        browser.driver.execute_script("arguments[0].click();", el)
        el2 = browser.element("label[for='hobbies-checkbox-3']").locate()
        browser.driver.execute_script("arguments[0].click();", el2)

    with allure.step("Загружаем файл и вводим адрес"):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'file_resource.jpg'))
        browser.element('#uploadPicture').set_value(file_path)
        browser.element('#currentAddress').type('Oakton, VA')

    with allure.step("Выбираем штат и город"):
        el_state = browser.element('#state').locate()
        browser.driver.execute_script("arguments[0].click();", el_state)
        browser.element('#react-select-3-input').type('NCR').press_enter()
        el_city = browser.element('#city').locate()
        browser.driver.execute_script("arguments[0].click();", el_city)
        browser.element('#react-select-4-input').type('Delhi').press_enter()

    with allure.step("Отправляем форму"):
        el_submit = browser.element('#submit').locate()
        browser.driver.execute_script("arguments[0].click();", el_submit)

    with allure.step("Проверяем модальное окно"):
        browser.element('.modal-content').should(be.visible)
        browser.element('.modal-title').should(have.text('Thanks for submitting the form'))
        browser.element('.table-responsive').should(have.text('Elina QA'))
        browser.element('.table-responsive').should(have.text('elina.qa@example.com'))
        browser.element('.table-responsive').should(have.text('Female'))
        browser.element('.table-responsive').should(have.text('9991111111'))
        browser.element('.table-responsive').should(have.text('14 June,1996'))
        browser.element('.table-responsive').should(have.text('Maths, Computer Science'))
        browser.element('.table-responsive').should(have.text('Sports, Music'))
        browser.element('.table-responsive').should(have.text('file_resource.jpg'))
        browser.element('.table-responsive').should(have.text('Oakton, VA'))
        browser.element('.table-responsive').should(have.text('NCR Delhi'))