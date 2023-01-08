from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.common.action_chains import ActionChains


def start_driver():
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data")
    chrome_options.add_argument(r'--profile-directory=Profile 4')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


def try_load(driver, link, tries):
    if tries == 6:
        print("FAILED TO LOAD VIDEO")
        return
    driver.get(link)
    time.sleep(7)
    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")

    logo = soup.find_all("a", "leftMenu__logo-link")
    if len(logo) == 0:
        return try_load(driver, link, tries + 1)

    youtube = soup.find_all("iframe")
    if len(youtube) != 0:
        print("YOUTUBE VIDEO")
        return
    vids = soup.find_all("div", class_="clappr-player")
    if len(vids) == 0:
        return try_load(driver, link, tries + 1)

    try:
        driver.find_element(By.CLASS_NAME, "player-poster").click()
    except:
        pass

    try:
        duration = soup.find_all("div", class_="media-control-indicator")[1].text
        if len(duration) == 5:
            duration = "00:" + duration
        print(duration)
        h = int(duration[:2])
        m = int(duration[3:5])
        s = int(duration[6:8])
        secs = h * 3600 + m * 60 + s
        print(secs)
        cast_time = secs // 3 + 5 * 60
    except:
        return try_load(driver, link, tries + 1)

    fullscr = driver.find_element(By.XPATH, "//button[@aria-label='fullscreen']")
    ActionChains(driver).move_to_element(fullscr).perform()
    time.sleep(1)
    fullscr.click()

    speed = driver.find_element(By.XPATH, "//button[normalize-space()='1x']")
    ActionChains(driver).move_to_element(speed).perform()
    time.sleep(1)
    speed.click()

    rate = driver.find_element(By.XPATH, "//a[normalize-space()='3x']")
    ActionChains(driver).move_to_element(rate).perform()
    time.sleep(1)
    rate.click()

    time.sleep(cast_time)


def main():
    f = open("links.csv", encoding="cp1251")
    reader = csv.reader(f)
    driver = start_driver()
    for row in reader:
        name, link = row
        c = link.count('/')
        print(name, link)
        if c != 6:
            continue
        try_load(driver, link, 0)
        print("VIDEO WAS LOADED")

    driver.quit()


if __name__ == "__main__":
    main()

