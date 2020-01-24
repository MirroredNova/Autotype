import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from threading import Thread


def run(box, words, speed):
    for word in words:
        box.send_keys(word.get_attribute('innerHTML'))
        box.send_keys(Keys.SPACE)
        time.sleep(speed)


def get_wpm():
    try:
        wpm = input("Enter number of WPM (360 max): ")
        num = float(wpm)

        if num > 360:
            raise ValueError

        speed = 60 / num
        return speed

    except ValueError:
        return get_wpm()


def main():
    speed = get_wpm()
    driver = webdriver.Firefox()
    driver.get('https://10fastfingers.com/typing-test/english')
    box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='inputfield']")))
    words = driver.find_elements_by_xpath("//div[@id='row1']/span")

    t = Thread(target=run, args=(box, words, speed))
    t.daemon = True
    t.start()
    time.sleep(60)

    print(WebDriverWait(driver, 10)
          .until(EC.presence_of_element_located((By.XPATH, "//td[@id='wpm']/strong"))).get_attribute('innerHTML'))
    driver.close()


main()
