import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser


@pytest.fixture(scope='function')
def setup_browser():
    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "128.0")
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    # browser.config.driver = webdriver.Chrome()
    browser.config.driver = driver
    browser.config.base_url = "https://demoqa.com"
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    # артефакты для Allure
    # скриншот
    allure.attach(
        driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=AttachmentType.PNG
    )

    # HTML страницы
    allure.attach(
        driver.page_source,
        name="page_source",
        attachment_type=AttachmentType.HTML
    )

    # логи браузера
    try:
        logs = driver.get_log("browser")
        text = "\n".join([f"{l['level']}: {l['message']}" for l in logs])
        allure.attach(text, "browser_logs", AttachmentType.TEXT, ".log")
    except Exception:
        pass

    # видео
    video_url = f"https://selenoid.autotests.cloud/video/{driver.session_id}.mp4"
    allure.attach(
        f"<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'></video></body></html>",
        name="video",
        attachment_type=AttachmentType.HTML
    )

    driver.quit()
