import pyautogui
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from nickname_generator import generate
import names
import random
import os
import csv
import requests
import json


token = '***'
country = 'russia'
operator = 'any'
product = 'steam'
id = 0


headers = {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/json',
}

pyautogui.PAUSE = 0


def create_driver(width, height, posx, posy):
    s = Service("chromedriver.exe")
    chrome_options = Options()
    chrome_options.Proxy = proxy
    chrome_options.add_argument("ignore-certificate-errors")
    chrome_options.add_extension('ext.crx')
    chrome_options.add_argument(r"--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data")
    chrome_options.add_argument(r"--profile-directory=Default")
    chrome_options.add_argument("--headless")
    dr = webdriver.Chrome(options=chrome_options, service=s)
    dr.maximize_window()
    dr.set_window_position(posx, posy)
    dr.set_window_size(width, height)
    dr.implicitly_wait(4)
    dr.delete_all_cookies()
    return dr


def gen_pass():
    alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    password = [''] * 10
    for i in range(10):
        password[i] = random.choice(alp)
    return "".join(password)


def enter_email(dr, mail, password):
    dr.execute_script('''window.open("https://mail.ru/inbox","_blank");''')
    dr.switch_to.window(dr.window_handles[1])
    dr.find_element(By.CSS_SELECTOR, '[data-testid="login-input"]').send_keys(mail)
    dr.find_element(By.CSS_SELECTOR, '[data-testid="enter-password"]').click()
    dr.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys(password)
    dr.find_element(By.CSS_SELECTOR, '[data-testid="login-to-mail"]').click()

    time.sleep(2)

    try:
        dr.find_element(By.XPATH, "/html/body/div[16]/div[2]/div/div/div[1]/svg").click()
    except:
        print("Добавить номер телефона не найден")

    try:
        dr.find_element(By.CSS_SELECTOR, '[data-test-id="onboarding-button-start"]').click()
        dr.find_element(By.CSS_SELECTOR, '[data-test-id="onboarding-button-complete"]').click()
    except:
        print("Приступить к работе не найден")

    try:
        dr.find_element(By.XPATH, '//*[@id="app-canvas"]/div/div[1]/div[1]/div/div[2]/span/div[2]/div/div/div/div/div[1]/div/div/div[1]/div/div/div/a[1]/div[4]/div/div[1]').click()
    except:
        print("Steam mail not found")

    try:
        dr.find_element(By.XPATH, "//a[@class='link_mr_css_attr c-grey4_mr_css_attr']").click()
    except:
        print("Verify не найден")

    # dr.switch_to.window(dr.window_handles[0])


def enter_steam(dr, mail, password):

    nick = mail[:-8]

    dr.get("https://store.steampowered.com/login")
    dr.find_element(By.ID, "input_username").send_keys(nick)
    dr.find_element(By.ID, "input_password").send_keys(password)
    dr.find_element(By.XPATH, "//button[@type='submit']").click()

    dr.find_element(By.ID, "account_pulldown").click()
    dr.find_element(By.XPATH, '//*[@id="account_dropdown"]/div/a[1]').click()
    try:
        dr.find_element(By.XPATH, "//a[@class='btn_green_white_innerfade btn_border_2px btn_medium']").click()
    except:
        print("Green button not found")
    try:
        dr.find_element(By.XPATH, "//a[@class='btn_profile_action btn_medium']").click()
    except:
        print("Edit profile not found")
        
    # PROFILE SETTINGS

    name = dr.find_element(By.XPATH, "//input[@name='real_name']")
    url = dr.find_element(By.XPATH, "//input[@name='customURL']")
    if name.get_attribute("value") == "":
        name.send_keys(names.get_first_name(gender='male'))
    if url.get_attribute("value") == "":
        url.send_keys(nick)

    dr.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
    time.sleep(2)
    dr.find_element(By.XPATH, '//*[@id="application_root"]/div[2]/div[1]/a[2]').click()
    time.sleep(2)
    dr.find_element(By.XPATH, '//div[4]//div[2]//div[1]//div[1]').click()
    time.sleep(2)
    dr.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
    dr.find_element(By.XPATH, '//*[@id="application_root"]/div[2]/div[2]/div/div[2]/button[1]').click()
    dr.find_element(By.XPATH, '//*[@id="application_root"]/div[2]/div[1]/a[5]').click()
    dr.find_element(By.XPATH, '//*[@id="application_root"]/div[2]/div[2]/div[3]/div/div[2]/div/div/div/div[5]/div[1]').click()
    dr.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()

    dr.get("https://steamcommunity.com/id/" + nick + "/tradeoffers/privacy")
    trade_link = dr.find_element(By.ID, "trade_offer_access_url").get_attribute("value")
    open("trade.txt", 'a').write(nick + ':' + trade_link + '\n')
    dr.get("https://steamcommunity.com/id/" + nick + "/edit/settings/")

    dr.find_element(By.XPATH, '//*[@id="application_root"]/div[2]/div[2]/div/div[6]/div[7]/div').click()
    dr.find_element(By.CLASS_NAME, "contextMenuItem").click()


def steam_guard(dr, mail, password, phone):
    nick = mail[:-8]

    dr.get("https://store.steampowered.com/login")
    dr.find_element(By.ID, "input_username").send_keys(nick)
    dr.find_element(By.ID, "input_password").send_keys(password)
    dr.find_element(By.XPATH, "//button[@type='submit']").click()

    dr.find_element(By.XPATH, '//*[@id="account_pulldown"]').click()
    dr.find_element(By.XPATH, '//*[@id="account_dropdown"]/div/a[2]').click()
    dr.find_element(By.XPATH, '//*[@id="main_content"]/div[2]/div[4]/div[2]/div/div/a').click()

    dr.find_element(By.ID, "tel_entry").send_keys(phone[2:])
    time.sleep(1)
    dr.find_element(By.XPATH, '//*[@id="next_button"]/a/span').click()

def reg_email(dr, nick, password):

    dr.delete_all_cookies()
    dr.get("https://account.mail.ru/signup")

    dr.find_element(By.ID, "fname").send_keys(nick)
    dr.find_element(By.ID, "lname").send_keys(random.choice('ABDDEYXVPRTF'))
    dr.find_element(By.XPATH, "//label[@data-test-id='gender-male']//div[@class='radio-0-2-141']").click()
    dr.find_element(By.XPATH, "//div[@class='select-0-2-123 daySelect-0-2-124']//div[@class='base-0-2-102 first-0-2-108']").click()
    for i in range(random.randrange(0, 15)):
        pyautogui.press('down')
    pyautogui.press('enter')

    dr.find_element(By.XPATH, "//div[@data-test-id='birth-date__month']//div[@class='select-0-2-127 auto-0-2-130 css-2b097c-container']").click()

    for i in range(random.randrange(0, 11)):
        pyautogui.press('down')
    pyautogui.press('enter')

    dr.find_element(By.XPATH, "//div[@data-test-id='birth-date__year']//div[@class='select-0-2-127 auto-0-2-130 css-2b097c-container']").click()

    for i in range(random.randrange(20, 40)):
        pyautogui.press('down')
    pyautogui.press('enter')

    dr.find_element(By.ID, "aaa__input").send_keys(nick)
    dr.find_element(By.ID, "password").send_keys(password)
    dr.find_element(By.ID, "repeatPassword").send_keys(password)
    dr.find_element(By.XPATH, "//button[@type='submit']").click()

    input("Solve email captcha...")


def reg_steam(dr, mail, password):
    dr.delete_all_cookies()
    dr.get("https://store.steampowered.com/join/")
    dr.find_element(By.ID, "email").send_keys(mail)
    dr.find_element(By.ID, "reenter_email").send_keys(mail)
    dr.find_element(By.ID, "i_agree_check").click()

    input("Solve steam captcha...")

    dr.execute_script('''window.open("https://mail.ru/inbox","_blank");''')
    dr.switch_to.window(dr.window_handles[1])
    dr.find_element(By.CSS_SELECTOR, '[data-testid="login-input"]').send_keys(mail)
    dr.find_element(By.CSS_SELECTOR, '[data-testid="enter-password"]').click()
    dr.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys(password)
    dr.find_element(By.CSS_SELECTOR, '[data-testid="login-to-mail"]').click()

    time.sleep(2)

    try:
        dr.find_element(By.CSS_SELECTOR, '[data-test-id="onboarding-button-start"]').click()
        dr.find_element(By.CSS_SELECTOR, '[data-test-id="onboarding-button-complete"]').click()
    except:
        print("Приступить к работе не найден")

    try:
        dr.find_element(By.CLASS_NAME, "ll-crpt").click()
    except:
        print("Стим не найден")

    try:
        dr.find_element(By.XPATH, "//a[text()='Подтвердить адрес эл. почты   ']").click()
    except:
        print("Verify не найден")

    dr.switch_to.window(dr.window_handles[0])

    input("Waiting for email verification...")


def clear_console():
    os.system('cls')


def write_time(filename, data):
    now = datetime.now()
    f = open(filename, 'a')
    f.write(data + ':' + str(now.year) + '-' + str(now.month) + '-' + \
            str(now.day) + ' ' + str(now.hour) + '-' + str(now.minute) + '-' + \
            str(now.second) + '\n')
    f.close()


def reg_emails(i):
    nick = generate()
    mail = nick + "@mail.ru"
    password = gen_pass()
    dr = create_driver(1000, 500, 0, 640)
    reg_email(dr, nick, password)

    open("new.txt", 'a').write(mail + ':' + password + '\n')
    write_time("mail_creation.txt", mail)


def reg_steams(i):
    global dr
    f = open("new.txt", 'r')
    mail, password = f.readlines()[i].strip().split(":")
    f.close()

    input("Register steam on your browser\n" + mail + '\n' + mail[:-8] + ':' + password)

    dr = create_driver(1000, 500, 0, 640)
    enter_email(dr, mail, password)

    input("Waiting for steam registration...")
    write_time("steam_creation.txt", mail[:-8])


def enter_steams(i):
    f = open("new.txt", 'r')
    mail, password = f.readlines()[i].strip().split(":")
    f.close()
    dr = create_driver(1000, 500, 0, 640)
    enter_steam(dr, mail, password)


def add_guards(i, num):
    f = open("new.txt", 'r')
    mail, password = f.readlines()[i].strip().split(':')
    f.close()

    dr = create_driver(1000, 500, 0, 500)
    print("Adjusting account " + mail[:-8] + ":" + password)
    steam_guard(dr, mail, password, num)
    enter_email(dr, mail, password)
    code = input("Recovery code ")

    open("recovery.txt", 'a').write(mail[:-8] + ":" + code + '\n')
    open("number.txt", 'a').write(mail[:-8] + ":" + num + '\n')

    write_time("guard.txt", mail[:-8])


def reg_gmail(dr, nick, password, phone):
    dr.get("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp")
    dr.find_element(By.ID, "firstName").send_keys(nick)
    dr.find_element(By.ID, "lastName").send_keys(random.choice("ABCDFGYXTOP"))
    dr.find_element(By.ID, "username").send_keys(nick)
    dr.find_element(By.NAME, "Passwd").send_keys(password)
    dr.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
    dr.find_element(By.XPATH, "//span[normalize-space()='Далее']").click()
    dr.find_element(By.ID, "phoneNumberId").send_keys(phone)
    try:
        dr.find_element(By.XPATH, "//span[normalize-space()='Далее']").click()
    except:
        time.sleep(1)
        dr.find_element(By.XPATH, "//span[normalize-space()='Далее']").click()
    input("Enter verification code...")
    dr.find_element(By.ID, "day").send_keys(random.randint(1, 28))
    Select(dr.find_element(By.ID, "month")).select_by_visible_text("Май")
    dr.find_element(By.ID, "year").send_keys(random.randint(1970, 1994))
    Select(dr.find_element(By.ID, "gender")).select_by_visible_text("Мужской")
    dr.find_element(By.XPATH, "//span[normalize-space()='Далее']").click()
    time.sleep(1)
    dr.find_element(By.XPATH, "//span[normalize-space()='Добавить номер']").click()
    time.sleep(1)
    dr.find_element(By.XPATH, "//span[normalize-space()='Принимаю']").click()


def reg_gmails(i, num):
    nick, password = generate() + random.choice("abgporx"), gen_pass()
    dr = create_driver(1000, 500, 0, 500)
    reg_gmail(dr, nick, password, num)
    open("gmails.txt", 'a').write(nick + "@gmail.com:" + password + ':' + num + '\n')


n_accounts = 20


def write_data_to_csv():
    accounts = dict([l.strip().split(':') for l in open("new.txt", 'r').readlines()])
    trade_links = dict([l.strip().split(':', 1) for l in open("trade.txt", 'r').readlines()])
    numbers = dict([l.strip().split(':') for l in open("number.txt", 'r').readlines()])
    steam_dates = dict([l.strip().split(':') for l in open("steam_creation.txt", 'r').readlines()])
    mail_dates = dict([l.strip().split(':') for l in open("mail_creation.txt", 'r').readlines()])
    recoveries = dict([l.strip().split(':') for l in open("recovery.txt", 'r').readlines()])
    guards = dict([l.strip().split(':') for l in open("guard.txt", 'r').readlines()])
    write_header = False

    with open("accounts.csv", 'w') as f:
        wr = csv.writer(f, lineterminator='\n')
        wr.writerow('')

    with open("accounts.csv", 'r') as f:
        wr = csv.reader(f)
        for r in wr:
            if len(r) == 0:
                write_header = True
        f.close()

    with open("accounts.csv", 'a') as f:
        wr = csv.writer(f, delimiter=',', lineterminator='\n')
        if write_header:
            wr.writerow(['mail', 'mailpass', 'mail_date', 'steam',
                         'steampass', 'steam_date', 'number',
                         'recovery', 'guard_date', 'tradelink'])

        for i in range(n_accounts):
            mail, password = list(accounts.keys())[i], accounts[list(accounts.keys())[i]]
            nick = mail[:-8]
            steam_date = steam_dates[nick] if nick in steam_dates.keys() else ' '
            mail_date = mail_dates[mail] if mail in mail_dates.keys() else ' '
            number = numbers[nick] if nick in numbers.keys() else ' '
            recovery = recoveries[nick] if nick in recoveries.keys() else ' '
            recovery_date = guards[nick] if nick in guards.keys() else ' '
            trade = trade_links[nick] if nick in trade_links.keys() else ' '

            wr.writerow([mail, password, mail_date, nick, password, steam_date,
                         number, recovery, recovery_date, trade])


def registration(email, register_steam, adjust_profile, guard, gmail):
    if email:
        for i in range(n_accounts):
            reg_emails(i)
    if register_steam:
        for i in range(n_accounts):
            reg_steams(i)
    if adjust_profile:
        for i in range(n_accounts):
            enter_steams(i)
    if guard:
        global id
        response = requests.get('https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + product, headers=headers)
        js = json.loads(response.text)
        id = js["id"]
        num = js["phone"]
        num = input("Input number ")

        for i in range(3, n_accounts):
            add_guards(i, num)
    if gmail:
        num = input("Input number ")
        for i in range(n_accounts):
            reg_gmails(i, num)

if __name__ == "__main__":
    registration(False, False, False, False, True)
    write_data_to_csv()