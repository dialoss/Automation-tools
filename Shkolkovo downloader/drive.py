from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r'--profile-directory=Profile')
driver = webdriver.Chrome(options=chrome_options)

base_url = "https://2.shkolkovo.online"
driver.maximize_window()
writer = None

save_dz = True
save_files = True
cur = ""


def clear_name(name):
    d = '"?:<>|*/.'
    for i in d:
        if i in name:
            name = name.replace(i, "").strip()
    return name

#  Windows cannot create files, whose path length more than 255 symbols
def shrink_name(name):
    if len(name) > 40:
       name = name[:40].strip()
    return name


def save_attachments(soup, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_links = soup.find_all("a", class_="homework-page__attachment-link")
    temp = soup.find_all("div", class_="homework-page__attachment-content")
    file_names = []
    for t in temp:
        if t.find("span") is not None:
            file_names.append(t.find("span"))
    f = open(f"{folder}/{len(file_links)}links, {len(file_names)}names", 'w')
    f.close()
    for i in range(len(file_links)):
        name = file_names[i].text
        if len(name) > 40:
            name = name[:40].strip()
            name += ".pdf"
        link = base_url + (file_links[i].get("href")).strip()
        try:
            response = requests.get(link)
            pdf = open(folder + "/" + name, 'wb')
            pdf.write(response.content)
            pdf.close()
        except:
            print(f"FAILED TO WRITE PDF {link}")
        time.sleep(0.5)

    images = driver.find_elements(By.CLASS_NAME, "exercise")
    i = 1
    f = open(f"{folder}/{len(images)}images", 'w')
    f.close()
    for img in images:
        driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", img)
        driver.get_screenshot_as_file(f"{folder}/homework{i}.png")
        i += 1


def get_homework(folder):
    try:
        driver.find_element(By.CLASS_NAME, "pagination-homework__btn-done").click()
    except:
        pass
    time.sleep(4)
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    save_attachments(soup, folder)


def deep(url, folder, dir):
    c = url.count('/')
    if c == 6 and not save_files:
        return
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    btn_buy = soup.find_all("a", class_="btn-blue")
    for btn in btn_buy:
        if "Купить" in btn.text:
            return True

    if save_files:
        try:
            if not os.path.exists(folder + '/' + dir):
                os.makedirs(folder + '/' + dir)
            folder += '/' + dir
        except:
            dir = clear_name(dir)
            if not os.path.exists(folder + '/' + dir):
                os.makedirs(folder + '/' + dir)
            folder += '/' + dir


    if c == 6 and save_files:
        save_attachments(soup, folder)
        if save_dz:
            ok = False
            if cur == "Информатика":
                hw = soup.find_all("a")
                for link in hw:
                    if "ДЗ" in link.text:
                        q = link.get("href")
                        if q is not None:
                            try:
                                if base_url in q:
                                    driver.get(q.strip())
                                else:
                                    driver.get(base_url + q.strip())
                                ok = True
                                get_homework(folder)
                            except:
                                pass
            if not ok:
                try:
                    driver.find_element(By.CLASS_NAME, "accordion__title-wrap").click()
                    time.sleep(0.5)
                    dz_items = driver.find_elements(By.CLASS_NAME, "homeworks__col-btn")
                    n = len(dz_items)
                    for i in range(n):
                        dz_items = driver.find_elements(By.CLASS_NAME, "homeworks__col-btn")
                        item = dz_items[i]
                        item.click()
                        time.sleep(4)
                        title = driver.find_element(By.CLASS_NAME, "homework-page__title").text
                        title = clear_name(title)
                        title = shrink_name(title)
                        get_homework(f"{folder}/{title}")
                        driver.get(url)
                        time.sleep(2)
                        driver.find_element(By.CLASS_NAME, "accordion__title-wrap").click()
                        time.sleep(0.5)
                except:
                    pass


    blocks = soup.find_all("a", class_="video__list-title")
    status = soup.find_all("div", {"class": ["ended", "planned"]})
    for i in range(len(blocks)):
        link = blocks[i]
        if len(status) == len(blocks) and ("Заплан" in status[i].text):
            continue

        cur_url = base_url + (link.get("href")).strip()
        cur_dir = link.text.strip()
        if "Линейный план" in cur_dir:
            continue
        writer.writerow([cur_dir, cur_url])
        cur_dir = shrink_name(cur_dir)
        print(cur_dir, cur_url, sep=' ')
        to_buy = deep(cur_url, folder, cur_dir)
        if to_buy:
            time.sleep(1)
            break


def start():
    global writer, save_dz, save_files, cur
    save_dz = True
    save_files = True
    driver.get("https://2.shkolkovo.online/my")
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    time.sleep(5)
    subjects = soup.find_all("div", class_="subject-main__catalog-item")
    links = soup.find_all("a", class_="subject-main__catalog-fon")
    for i in range(3, len(subjects)):
        name = subjects[i].text.strip()
        cur = name
        output = open(f"{name}links.csv", 'w', newline='')
        writer = csv.writer(output)
        st = base_url + links[i].get("href").strip()
        deep(st, "Папка", name)
        output.close()
    driver.quit()


def save_links():
    global writer, save_dz, save_files
    save_dz = True
    save_files = True
    st = "https://2.shkolkovo.online/courses/7/1315/9482"
    output = open("Переченьlinks.csv", 'w', newline='')
    writer = csv.writer(output)
    deep(st, "Новый", "Тест")
    output.close()
    driver.quit()


if __name__ == "__main__":
    start()
