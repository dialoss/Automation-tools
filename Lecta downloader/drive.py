from selenium import webdriver
import urllib.request
from selenium.webdriver.chrome.options import Options
import os
import time
from PIL import Image
from io import BytesIO


class Driver():
    def __init__(self, options, pathToLoad, name):
        self.options = options
        self.pathToLoad = pathToLoad
        self.name = name
        option = Options()
        option.add_argument(self.options)
        option.add_argument("--window-size=1400x900")
        self.driver = webdriver.Chrome(options=option)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

    def main_functions(self):
        self.driver.get("https://id.prosv.ru/oauth2/client/683b6476-155a-5403-97fb-32ae2d5f7d10")
        self.driver.find_element_by_name("email").click()
        self.driver.find_element_by_name("email").clear()
        self.driver.find_element_by_name("email").send_keys("number")
        self.driver.find_element_by_name("pass").click()
        self.driver.find_element_by_name("pass").clear()
        self.driver.find_element_by_name("pass").send_keys("password")
        self.driver.find_element_by_id("install_allow").click()
        self.driver.get('https://lecta.rosuchebnik.ru/mybooks')
        time.sleep(5)
        self.driver.refresh()
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()


    def save_images(self):
        for i in range(1, 500):
            s = "00" + str(i)
            s = s[-1:-4]
            self.driver.get(f'https://reader.lecta.rosuchebnik.ru/read/1017737-15/data/page-{s}.xhtml')
            self.driver.execute_script("document.body.style.zoom='90%'")
            elem = self.driver.find_element_by_class_name('pc ')
            location = elem.location
            size = elem.size
            png = self.driver.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            left = location['x'] - 0.04 * size['width']
            top = location['y']
            right = location['x'] + size['width'] - 0.2 * size['width']
            bottom = location['y'] + size['height'] - 0.11 * size['height']
            im = im.crop((left, top, right, bottom))
            im.save('{}/algeb{}.png'.format(self.pathToLoad, i))
            print('img saved')


def main():
    options = "--headless"
    path = 'algebra'
    name = 'algeb'
    driver = Driver(options, path, name)
    driver.main_functions()
    time.sleep(10)
    os.mkdir("{}".format(path))
    driver.save_images()


if __name__ == "__main__":
    main()
