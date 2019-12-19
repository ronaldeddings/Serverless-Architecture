import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PWD = os.path.dirname(os.path.abspath(__file__))
CHROME_PATH = f"{PWD}/headless-chromium"
CHROMEDRIVER_PATH = f"{PWD}/chromedriver"

def render(event, context):
    queryStringParameters = event.get("queryStringParameters")
    if not queryStringParameters or not queryStringParameters.get("target"):
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": "Missing URI Parameters. append <b>?target=hxxp://URLTOQUERY</b>"
        }

    target = queryStringParameters.get("target")

    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    except Exception as e:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": f"Oops something went wrong with executing Chromium<br><br> {str(e)}"
        }

    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.get(target)

    title = driver.title
    image = driver.get_screenshot_as_base64()
    driver.close()
    driver.quit()

    htmlBody = f"""
    <p>{title}</p><br>
    <img src="data:image/png;base64,{image}" alt="{title}"/>"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": htmlBody
    }
