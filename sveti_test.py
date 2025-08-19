import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки для обхода блокировок
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url = "https://divan.ru/category/svet"
driver.get(url)

# Явное ожидание загрузки товаров
wait = WebDriverWait(driver, 15)
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._Ud0k")))
except:
    print("Не удалось загрузить товары")
    driver.quit()
    exit()

# Поиск карточек товаров
svets = driver.find_elements(By.CSS_SELECTOR, "div._Ud0k")
print(f"Найдено товаров: {len(svets)}")

parsed_data = []

for svet in svets:
    try:
        # Новые селекторы для актуальной структуры сайта
        title = svet.find_element(By.CSS_SELECTOR, "div.lsooF span").text.strip()
        price = svet.find_element(By.CSS_SELECTOR, "div.pY3d2 span").text.strip()
        link = svet.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        parsed_data.append([title, price, link])

    except Exception as e:
        print(f"Ошибка при парсинге: {str(e)[:100]}...")
        continue

driver.quit()

# Сохранение в CSV
with open("svetilniki.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название товара", "Цена товара", "Ссылка"])
    writer.writerows(parsed_data)

print("✅ Данные сохранены в svetilniki.csv")